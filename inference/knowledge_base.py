import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


class KnowledgeBase:
    """Knowledge base untuk NetMedix v2.0.0 dengan schema baru (cf_pakar, evidence, sources, tutorial)."""

    def __init__(self):
        self.problems = self._load("problems.json")
        self.symptoms = self._load("symptoms.json")
        self.rules = self._load("rules.json")

    def _load(self, filename):
        """Load JSON file dari data directory."""
        path = os.path.join(DATA_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_problems(self):
        """Return list dari problems.json."""
        return self.problems

    def load_symptoms(self):
        """Return list dari symptoms.json."""
        return self.symptoms

    def load_rules(self):
        """Return list dari rules.json."""
        return self.rules

    def get_problem(self, code):
        """
        Cari problem berdasarkan kode (e.g. 'P01').

        Args:
            code (str): Kode problem (P01-P15)

        Returns:
            dict or None: Problem object jika ditemukan
        """
        for p in self.problems:
            if p["code"] == code:
                return p
        return None

    def get_problem_by_code(self, code):
        """Alias untuk get_problem(). Untuk backward compatibility."""
        return self.get_problem(code)

    def get_symptom(self, code):
        """
        Cari symptom berdasarkan kode (e.g. 'G01').
        Method ini untuk route /tutorial/<code>.

        Args:
            code (str): Kode gejala (G01-G40)

        Returns:
            dict or None: Symptom object jika ditemukan
        """
        for s in self.symptoms:
            if s["code"] == code:
                return s
        return None

    def get_symptom_by_code(self, code):
        """Alias untuk get_symptom(). Untuk backward compatibility."""
        return self.get_symptom(code)

    def get_symptoms_with_info(self):
        """
        Return list symptoms dengan fields info tambahan.
        Method ini untuk modal info di symptoms.html.

        Returns:
            list: List of symptom dicts dengan short_desc dan how_to_check
        """
        return [
            {
                "code": s["code"],
                "name": s["name"],
                "category": s.get("category", ""),
                "short_desc": s.get("short_desc", ""),
                "how_to_check": s.get("how_to_check", ""),
            }
            for s in self.symptoms
        ]

    def get_symptoms_by_category(self, category):
        """
        Filter symptoms berdasarkan kategori.

        Args:
            category (str): Kategori gejala

        Returns:
            list: List of symptoms dalam kategori tersebut
        """
        return [s for s in self.symptoms if s.get("category") == category]

    def get_categories(self):
        """
        Return list unik kategori gejala (preserve order).

        Returns:
            list: List of unique categories
        """
        seen = []
        for s in self.symptoms:
            cat = s.get("category")
            if cat and cat not in seen:
                seen.append(cat)
        return seen

    def get_rules_for_symptoms(self, symptom_codes):
        """
        Cari rules yang relevant — semua gejala rule ada di symptom_codes.
        Method ini DEPRECATED di v2.0.0 karena AND-strict sudah tidak dipakai.
        Disimpan untuk backward compatibility.

        Args:
            symptom_codes (list): List of symptom codes

        Returns:
            list: List of relevant rules (AND-strict)
        """
        symptom_set = set(symptom_codes)
        relevant = []
        for rule in self.rules:
            rule_symptom_codes = {s["code"] for s in rule["symptoms"]}
            if rule_symptom_codes.issubset(symptom_set):
                relevant.append(rule)
        return relevant
