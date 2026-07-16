class InferenceEngine:
    """Pure Certainty Factor inference engine untuk NetMedix v2.0.0."""

    def __init__(self, knowledge_base):
        self.kb = knowledge_base

    @staticmethod
    def calculate_cf_evidence(cf_user, cf_pakar):
        """
        Hitung CF evidence: CF_evidence = CF_user x CF_pakar.

        Args:
            cf_user (float): Certainty factor dari user [0.1, 1.0]
            cf_pakar (float): Certainty factor dari pakar [0.1, 1.0]

        Returns:
            float: CF_evidence hasil perkalian
        """
        return cf_user * cf_pakar

    @staticmethod
    def combine_cf(cf1, cf2):
        """
        Kombinasi dua nilai CF: CF_combine = CF1 + CF2 x (1 - CF1).

        Args:
            cf1 (float): CF pertama [0.0, 1.0]
            cf2 (float): CF kedua [0.0, 1.0]

        Returns:
            float: CF hasil kombinasi
        """
        return cf1 + cf2 * (1 - cf1)

    def diagnose(self, selected_symptoms):
        """
        Jalankan diagnosis dengan pure CF dan filter "≥ 2 gejala relevan".

        Args:
            selected_symptoms (dict): {"G01": cf_user_value, "G02": cf_user_value, ...}

        Returns:
            list: [{
                "problem_code": str,
                "problem_name": str,
                "category": str,
                "rule_code": str,
                "rule_sources": list,
                "cf_final": float,
                "percentage": float,
                "label": str,
                "matched_count": int,
                "total_symptoms_in_rule": int,
                "details": {
                    "evidence_steps": list,
                    "combine_steps": list
                }
            }] sorted by CF descending, ALL candidates (no truncation).
        """
        results = []

        for rule in self.kb.rules:
            # Step 1: Identifikasi gejala relevan yang dipilih user
            rule_symptom_codes = {s["code"] for s in rule["symptoms"]}
            matched_codes = rule_symptom_codes & set(selected_symptoms.keys())

            # Step 2: FILTER — ≥ 2 gejala relevan dipilih
            if len(matched_codes) < 2:
                continue

            # Step 3: Hitung CF_evidence per matched gejala
            evidences = []
            for code in matched_codes:
                symptom_rule = next(s for s in rule["symptoms"] if s["code"] == code)
                cf_pakar = symptom_rule["cf_pakar"]
                cf_user = selected_symptoms[code]
                cf_ev = self.calculate_cf_evidence(cf_user, cf_pakar)
                evidences.append({
                    "symptom_code": code,
                    "cf_pakar": cf_pakar,
                    "evidence_note": symptom_rule.get("evidence", ""),
                    "cf_user": cf_user,
                    "cf_evidence": round(cf_ev, 4),
                })

            # Step 4: Combine sekuensial (fold left-to-right)
            cf_final, combine_steps = self._combine_cfs_with_trace(
                [e["cf_evidence"] for e in evidences]
            )

            # Step 5: Ambil problem info
            problem = self.kb.get_problem(rule["target_problem"])

            results.append({
                "problem_code": rule["target_problem"],
                "problem_name": problem["name"] if problem else "Unknown",
                "category": problem.get("category", "") if problem else "",
                "rule_code": rule["code"],
                "rule_sources": rule.get("sources", []),
                "cf_final": round(cf_final, 4),
                "percentage": round(cf_final * 100, 2),
                "label": self.interpret_cf(cf_final),
                "matched_count": len(matched_codes),
                "total_symptoms_in_rule": len(rule_symptom_codes),
                "details": {
                    "evidence_steps": evidences,
                    "combine_steps": combine_steps,
                },
            })

        # Sort desc, return ALL (no top-3 truncation)
        results.sort(key=lambda r: r["cf_final"], reverse=True)
        return results

    def _combine_cfs_with_trace(self, cf_list):
        """
        Kombinasikan list CF sekuensial, return (cf_final, trace_steps).

        Args:
            cf_list (list): List of CF values to combine

        Returns:
            tuple: (cf_final, list of combine trace steps)
        """
        if not cf_list:
            return 0.0, []

        combined = cf_list[0]
        steps = []
        for i, cf in enumerate(cf_list[1:], start=1):
            prev = combined
            combined = self.combine_cf(combined, cf)
            steps.append({
                "step": i,
                "cf_a": round(prev, 4),
                "cf_b": round(cf, 4),
                "result": round(combined, 4),
            })
        return combined, steps

    @staticmethod
    def interpret_cf(cf_value):
        """
        Return label string berdasarkan nilai CF.

        Args:
            cf_value (float): Nilai CF [0.0, 1.0]

        Returns:
            str: Label interpretasi
        """
        if cf_value >= 0.80:
            return "Sangat Yakin"
        elif cf_value >= 0.60:
            return "Cukup Yakin"
        elif cf_value >= 0.40:
            return "Kemungkinan"
        elif cf_value >= 0.20:
            return "Kurang Yakin"
        else:
            return "Hampir Tidak Yakin"
