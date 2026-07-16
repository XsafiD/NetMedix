import os
import json
import sqlite3
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify

__version__ = "2.0.0"

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "netmedix-dev-key-change-in-prod")

DATABASE = os.path.join(os.path.dirname(__file__), "database", "history.db")
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")


@app.context_processor
def inject_active_page():
    from flask import request
    endpoint = request.endpoint
    if endpoint == "index":
        active = "home"
    elif endpoint and endpoint.startswith("admin"):
        active = "admin"
    else:
        active = endpoint or ""
    return {"active_page": active}


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS diagnosis_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            symptoms_selected TEXT NOT NULL,
            results TEXT NOT NULL,
            top_diagnosis TEXT NOT NULL,
            top_cf REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_session(symptoms_cf, results_data):
    """Save a diagnosis session. Returns the session id."""
    top = results_data[0] if results_data else None
    conn = get_db()
    cursor = conn.execute(
        """INSERT INTO diagnosis_sessions (symptoms_selected, results, top_diagnosis, top_cf)
           VALUES (?, ?, ?, ?)""",
        (
            json.dumps(symptoms_cf, ensure_ascii=False),
            json.dumps({"symptoms": symptoms_cf, "results": results_data},
                       ensure_ascii=False, default=str),
            top["problem_code"] if top else "",
            top["cf_final"] if top else 0.0,
        ),
    )
    conn.commit()
    session_id = cursor.lastrowid
    conn.close()
    return session_id


def get_all_sessions():
    """Return all diagnosis sessions ordered by date descending."""
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM diagnosis_sessions ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return rows


def get_session_by_id(session_id):
    """Return a single diagnosis session by id."""
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM diagnosis_sessions WHERE id = ?", (session_id,)
    ).fetchone()
    conn.close()
    return row


def delete_session(session_id):
    """Delete a diagnosis session by id."""
    conn = get_db()
    conn.execute("DELETE FROM diagnosis_sessions WHERE id = ?", (session_id,))
    conn.commit()
    conn.close()


def build_kesimpulan(results):
    """
    Build narasi kesimpulan untuk result.html.

    Args:
        results (list): List of diagnosis results dari engine.diagnose()

    Returns:
        dict: {
            "status": "empty" | "found",
            "message": str (jika empty),
            "top_problem": dict (jika found),
            "alternatives": list (jika found),
            "total_candidates": int (jika found)
        }
    """
    if not results:
        return {
            "status": "empty",
            "message": "Tidak ada diagnosis yang memenuhi syarat (minimal 2 gejala relevan). "
                       "Coba pilih gejala tambahan yang lebih spesifik."
        }

    top = results[0]
    others = results[1:4]  # tampilkan maks 3 alternatif di narasi

    return {
        "status": "found",
        "top_problem": top,
        "alternatives": others,
        "total_candidates": len(results),
    }


# ── JSON file helpers ────────────────────────────────────

def _load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_json(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ── Auth Decorator ───────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            flash("Silakan login terlebih dahulu.", "warning")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated


# ── Public Routes ──────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/diagnose")
def diagnose():
    from inference.knowledge_base import KnowledgeBase
    kb = KnowledgeBase()
    symptoms = kb.load_symptoms()
    categories = kb.get_categories()
    # Group symptoms by category
    symptoms_by_category = {}
    for cat in categories:
        symptoms_by_category[cat] = kb.get_symptoms_by_category(cat)
    # Get symptoms with info for modal
    symptoms_with_info = kb.get_symptoms_with_info()
    return render_template("diagnose.html",
                           categories=categories,
                           symptoms_by_category=symptoms_by_category,
                           symptoms_with_info=symptoms_with_info)


@app.route("/diagnose/step2", methods=["POST"])
def diagnose_step2():
    selected = request.form.getlist("symptoms")
    if not selected:
        return redirect(url_for("diagnose"))
    from inference.knowledge_base import KnowledgeBase
    kb = KnowledgeBase()
    symptoms = []
    for code in selected:
        s = kb.get_symptom_by_code(code)
        if s:
            symptoms.append(s)
    return render_template("diagnose_step2.html",
                           symptoms=symptoms,
                           symptom_codes=selected)


@app.route("/diagnose/process", methods=["POST"])
def diagnose_process():
    """Process diagnosis: run inference engine, save to DB, redirect to result."""
    from inference.knowledge_base import KnowledgeBase
    from inference.engine import InferenceEngine

    # Collect CF user values from form: cf_{SYMP_CODE} = float value
    selected_symptoms = {}
    for key, value in request.form.items():
        if key.startswith("cf_"):
            code = key[3:]  # e.g. "G01"
            try:
                cf_val = float(value)
                cf_val = max(0.1, min(1.0, cf_val))
                selected_symptoms[code] = cf_val
            except (ValueError, TypeError):
                continue

    if not selected_symptoms:
        flash("Tidak ada gejala yang diproses. Silakan pilih gejala terlebih dahulu.", "warning")
        return redirect(url_for("diagnose"))

    # Run inference
    kb = KnowledgeBase()
    engine = InferenceEngine(kb)
    results = engine.diagnose(selected_symptoms)

    if not results:
        session_id = save_session(selected_symptoms, [])
        return redirect(url_for("result", session_id=session_id))

    # Build full result data with problem details
    full_results = []
    for r in results:
        problem = kb.get_problem_by_code(r["problem_code"])
        label = InferenceEngine.interpret_cf(r["cf_final"])
        full_results.append({
            "problem_code": r["problem_code"],
            "rule_code": r["rule_code"],
            "cf_final": r["cf_final"],
            "cf_label": label,
            "cf_percent": round(r["cf_final"] * 100, 2),
            "problem": problem,
            "details": r["details"],
        })

    session_id = save_session(selected_symptoms, full_results)
    return redirect(url_for("result", session_id=session_id))


@app.route("/result/<int:session_id>")
def result(session_id):
    row = get_session_by_id(session_id)
    if not row:
        flash("Hasil diagnosis tidak ditemukan.", "error")
        return redirect(url_for("diagnose"))

    data = json.loads(row["results"])
    symptoms_selected = data.get("symptoms", {})
    results = data.get("results", [])

    # Enrich results with problem data
    from inference.knowledge_base import KnowledgeBase
    from inference.engine import InferenceEngine
    kb = KnowledgeBase()
    for r in results:
        if r.get("problem") is None:
            r["problem"] = kb.get_problem_by_code(r["problem_code"])
        # Handle v1 vs v2 format
        if "cf_label" not in r:
            r["cf_label"] = InferenceEngine.interpret_cf(r["cf_final"])
        if "cf_percent" not in r and "percentage" not in r:
            r["cf_percent"] = round(r["cf_final"] * 100, 2)
        elif "percentage" in r:
            r["cf_percent"] = r["percentage"]
        if "label" in r:
            r["cf_label"] = r["label"]

    # Build kesimpulan narasi
    kesimpulan = build_kesimpulan(results)

    # Load symptom names
    symptom_map = {}
    for code in symptoms_selected:
        s = kb.get_symptom_by_code(code)
        if s:
            symptom_map[code] = s

    return render_template("result.html",
                           session_id=session_id,
                           created_at=row["created_at"],
                           results=results,
                           symptoms_selected=symptoms_selected,
                           symptom_map=symptom_map,
                           kesimpulan=kesimpulan,
                           has_results=len(results) > 0)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/tutorial/<code>")
def tutorial_page(code):
    """Halaman tutorial gejala per kode (G01-G40)."""
    from inference.knowledge_base import KnowledgeBase
    from flask import abort

    code = code.upper()
    kb = KnowledgeBase()
    symptom = kb.get_symptom(code)

    if not symptom:
        abort(404)

    # Resolve related_symptoms untuk link
    related = []
    tutorial_data = symptom.get("tutorial", {})
    for r_code in tutorial_data.get("related_symptoms", []):
        r_symptom = kb.get_symptom(r_code)
        if r_symptom:
            related.append({"code": r_code, "name": r_symptom["name"]})

    return render_template(
        "tutorial.html",
        symptom=symptom,
        related=related,
    )


@app.route("/history")
def history():
    sessions = get_all_sessions()
    # Enrich sessions with problem name and symptom count
    from inference.knowledge_base import KnowledgeBase
    from inference.engine import InferenceEngine
    kb = KnowledgeBase()
    enriched = []
    for row in sessions:
        data = json.loads(row["results"]) if row["results"] else {}
        symptoms_selected = data.get("symptoms", {})
        results = data.get("results", [])
        symptom_count = len(symptoms_selected)
        top_problem = kb.get_problem_by_code(row["top_diagnosis"]) if row["top_diagnosis"] else None
        top_cf = row["top_cf"]
        cf_label = InferenceEngine.interpret_cf(top_cf) if top_cf > 0 else "Tidak ada diagnosis"
        enriched.append({
            "id": row["id"],
            "created_at": row["created_at"],
            "symptom_count": symptom_count,
            "top_problem": top_problem,
            "top_cf": top_cf,
            "cf_label": cf_label,
            "cf_percent": round(top_cf * 100, 2) if top_cf else 0,
        })
    return render_template("history.html", sessions=enriched)


@app.route("/history/<int:session_id>")
def history_detail(session_id):
    row = get_session_by_id(session_id)
    if not row:
        flash("Riwayat diagnosis tidak ditemukan.", "error")
        return redirect(url_for("history"))
    return redirect(url_for("result", session_id=session_id))


@app.route("/history/<int:session_id>/delete", methods=["POST"])
def history_delete(session_id):
    delete_session(session_id)
    flash("Riwayat diagnosis berhasil dihapus.", "success")
    return redirect(url_for("history"))


# ── Admin Auth Routes ─────────────────────────────────────

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "GET":
        if session.get("admin_logged_in"):
            return redirect(url_for("admin_dashboard"))
        return render_template("admin/login.html")

    username = request.form.get("username", "")
    password = request.form.get("password", "")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session["admin_logged_in"] = True
        flash("Login berhasil!", "success")
        return redirect(url_for("admin_dashboard"))
    else:
        flash("Username atau password salah.", "error")
        return render_template("admin/login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    flash("Anda telah logout.", "info")
    return redirect(url_for("admin_login"))


# ── Admin Dashboard ───────────────────────────────────────

@app.route("/admin")
@login_required
def admin_dashboard():
    problems = _load_json("problems.json")
    symptoms = _load_json("symptoms.json")
    rules = _load_json("rules.json")
    return render_template("admin/dashboard.html",
                           problems=problems,
                           symptoms=symptoms,
                           rules=rules)


# ── Admin Problems CRUD ───────────────────────────────────

@app.route("/admin/problems")
@login_required
def admin_problems():
    problems = _load_json("problems.json")
    return render_template("admin/problems.html", problems=problems)


@app.route("/admin/problems/add", methods=["POST"])
@login_required
def admin_problems_add():
    problems = _load_json("problems.json")

    code = request.form.get("code", "").strip().upper()
    name = request.form.get("name", "").strip()
    name_en = request.form.get("name_en", "").strip()
    category = request.form.get("category", "").strip()
    description = request.form.get("description", "").strip()
    causes_raw = request.form.get("causes", "").strip()
    solutions_raw = request.form.get("solutions", "").strip()

    # Validation
    if not code or not name or not category or not description:
        flash("Kode, nama, kategori, dan deskripsi wajib diisi.", "error")
        return redirect(url_for("admin_problems"))

    # Check duplicate code
    if any(p["code"] == code for p in problems):
        flash(f"Kode {code} sudah digunakan.", "error")
        return redirect(url_for("admin_problems"))

    causes = [c.strip() for c in causes_raw.split("\n") if c.strip()]
    solutions = [s.strip() for s in solutions_raw.split("\n") if s.strip()]

    new_problem = {
        "code": code,
        "name": name,
        "name_en": name_en or name,
        "category": category,
        "description": description,
        "causes": causes,
        "solutions": solutions
    }

    problems.append(new_problem)
    _save_json("problems.json", problems)
    flash(f"Masalah {code} berhasil ditambahkan.", "success")
    return redirect(url_for("admin_problems"))


@app.route("/admin/problems/edit", methods=["POST"])
@login_required
def admin_problems_edit():
    problems = _load_json("problems.json")
    code = request.form.get("original_code", "")

    for i, p in enumerate(problems):
        if p["code"] == code:
            problems[i]["name"] = request.form.get("name", "").strip()
            problems[i]["name_en"] = request.form.get("name_en", "").strip() or problems[i]["name"]
            problems[i]["category"] = request.form.get("category", "").strip()
            problems[i]["description"] = request.form.get("description", "").strip()
            causes_raw = request.form.get("causes", "").strip()
            solutions_raw = request.form.get("solutions", "").strip()
            problems[i]["causes"] = [c.strip() for c in causes_raw.split("\n") if c.strip()]
            problems[i]["solutions"] = [s.strip() for s in solutions_raw.split("\n") if s.strip()]
            break

    _save_json("problems.json", problems)
    flash(f"Masalah {code} berhasil diperbarui.", "success")
    return redirect(url_for("admin_problems"))


@app.route("/admin/problems/delete", methods=["POST"])
@login_required
def admin_problems_delete():
    problems = _load_json("problems.json")
    code = request.form.get("code", "")
    problems = [p for p in problems if p["code"] != code]
    _save_json("problems.json", problems)
    flash(f"Masalah {code} berhasil dihapus.", "success")
    return redirect(url_for("admin_problems"))


# ── Admin Symptoms CRUD ───────────────────────────────────

@app.route("/admin/symptoms")
@login_required
def admin_symptoms():
    symptoms = _load_json("symptoms.json")
    categories = list(dict.fromkeys(s.get("category", "") for s in symptoms))
    return render_template("admin/symptoms.html",
                           symptoms=symptoms,
                           categories=categories)


@app.route("/admin/symptoms/add", methods=["POST"])
@login_required
def admin_symptoms_add():
    symptoms = _load_json("symptoms.json")

    code = request.form.get("code", "").strip().upper()
    name = request.form.get("name", "").strip()
    question = request.form.get("question", "").strip()
    category = request.form.get("category", "").strip()

    if not code or not name or not question or not category:
        flash("Semua field wajib diisi.", "error")
        return redirect(url_for("admin_symptoms"))

    if any(s["code"] == code for s in symptoms):
        flash(f"Kode {code} sudah digunakan.", "error")
        return redirect(url_for("admin_symptoms"))

    new_symptom = {
        "code": code,
        "name": name,
        "question": question,
        "category": category
    }

    symptoms.append(new_symptom)
    _save_json("symptoms.json", symptoms)
    flash(f"Gejala {code} berhasil ditambahkan.", "success")
    return redirect(url_for("admin_symptoms"))


@app.route("/admin/symptoms/edit", methods=["POST"])
@login_required
def admin_symptoms_edit():
    symptoms = _load_json("symptoms.json")
    code = request.form.get("original_code", "")

    for i, s in enumerate(symptoms):
        if s["code"] == code:
            symptoms[i]["name"] = request.form.get("name", "").strip()
            symptoms[i]["question"] = request.form.get("question", "").strip()
            symptoms[i]["category"] = request.form.get("category", "").strip()
            break

    _save_json("symptoms.json", symptoms)
    flash(f"Gejala {code} berhasil diperbarui.", "success")
    return redirect(url_for("admin_symptoms"))


@app.route("/admin/symptoms/delete", methods=["POST"])
@login_required
def admin_symptoms_delete():
    symptoms = _load_json("symptoms.json")
    code = request.form.get("code", "")
    symptoms = [s for s in symptoms if s["code"] != code]
    _save_json("symptoms.json", symptoms)
    flash(f"Gejala {code} berhasil dihapus.", "success")
    return redirect(url_for("admin_symptoms"))


# ── Admin Rules CRUD ──────────────────────────────────────

@app.route("/admin/rules")
@login_required
def admin_rules():
    rules = _load_json("rules.json")
    problems = _load_json("problems.json")
    symptoms = _load_json("symptoms.json")
    return render_template("admin/rules.html",
                           rules=rules,
                           problems=problems,
                           symptoms=symptoms)


@app.route("/admin/rules/add", methods=["POST"])
@login_required
def admin_rules_add():
    rules = _load_json("rules.json")

    code = request.form.get("code", "").strip().upper()
    name = request.form.get("name", "").strip()
    target_problem = request.form.get("target_problem", "").strip()

    if not code or not name or not target_problem:
        flash("Kode, nama, dan target masalah wajib diisi.", "error")
        return redirect(url_for("admin_rules"))

    if any(r["code"] == code for r in rules):
        flash(f"Kode aturan {code} sudah digunakan.", "error")
        return redirect(url_for("admin_rules"))

    # Parse symptom entries from form
    symptom_codes = request.form.getlist("symptom_code[]")
    symptom_mbs = request.form.getlist("symptom_mb[]")
    symptom_mds = request.form.getlist("symptom_md[]")

    rule_symptoms = []
    for sc, smb, smd in zip(symptom_codes, symptom_mbs, symptom_mds):
        sc = sc.strip()
        if sc:
            try:
                mb = float(smb)
                md = float(smd)
            except ValueError:
                mb = 0.5
                md = 0.1
            mb = max(0.0, min(1.0, mb))
            md = max(0.0, min(1.0, md))
            rule_symptoms.append({"code": sc, "mb": mb, "md": md})

    if not rule_symptoms:
        flash("Aturan harus memiliki minimal 1 gejala.", "error")
        return redirect(url_for("admin_rules"))

    new_rule = {
        "code": code,
        "name": name,
        "target_problem": target_problem,
        "symptoms": rule_symptoms
    }

    rules.append(new_rule)
    _save_json("rules.json", rules)
    flash(f"Aturan {code} berhasil ditambahkan.", "success")
    return redirect(url_for("admin_rules"))


@app.route("/admin/rules/edit", methods=["POST"])
@login_required
def admin_rules_edit():
    rules = _load_json("rules.json")
    code = request.form.get("original_code", "")

    for i, r in enumerate(rules):
        if r["code"] == code:
            rules[i]["name"] = request.form.get("name", "").strip()
            rules[i]["target_problem"] = request.form.get("target_problem", "").strip()

            symptom_codes = request.form.getlist("symptom_code[]")
            symptom_mbs = request.form.getlist("symptom_mb[]")
            symptom_mds = request.form.getlist("symptom_md[]")

            rule_symptoms = []
            for sc, smb, smd in zip(symptom_codes, symptom_mbs, symptom_mds):
                sc = sc.strip()
                if sc:
                    try:
                        mb = float(smb)
                        md = float(smd)
                    except ValueError:
                        mb = 0.5
                        md = 0.1
                    mb = max(0.0, min(1.0, mb))
                    md = max(0.0, min(1.0, md))
                    rule_symptoms.append({"code": sc, "mb": mb, "md": md})

            rules[i]["symptoms"] = rule_symptoms
            break

    _save_json("rules.json", rules)
    flash(f"Aturan {code} berhasil diperbarui.", "success")
    return redirect(url_for("admin_rules"))


@app.route("/admin/rules/delete", methods=["POST"])
@login_required
def admin_rules_delete():
    rules = _load_json("rules.json")
    code = request.form.get("code", "")
    rules = [r for r in rules if r["code"] != code]
    _save_json("rules.json", rules)
    flash(f"Aturan {code} berhasil dihapus.", "success")
    return redirect(url_for("admin_rules"))


# ── Error Handlers ─────────────────────────────────────────

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500


# ── Entry Point ────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
