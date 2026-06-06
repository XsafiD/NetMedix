class InferenceEngine:
    """Forward Chaining + Certainty Factor inference engine."""

    def __init__(self, knowledge_base):
        self.kb = knowledge_base

    @staticmethod
    def calculate_cf_rule(mb, md):
        """Hitung CF rule: CF(H,E) = MB - MD."""
        return mb - md

    @staticmethod
    def calculate_cf_evidence(cf_user, cf_rule):
        """Hitung CF evidence: CF_evidence = CF_user x CF(H,E)."""
        return cf_user * cf_rule

    @staticmethod
    def combine_cf(cf1, cf2):
        """Kombinasi dua nilai CF: CF_combine = CF1 + CF2 x (1 - CF1)."""
        return cf1 + cf2 * (1 - cf1)

    def forward_chaining(self, selected_symptoms):
        """
        Run forward chaining on selected symptoms.

        selected_symptoms: dict { "G01": cf_user_value, "G02": cf_user_value, ... }
        Returns: list of {"problem_code": str, "cf_final": float, "details": dict}
                 sorted by CF descending, top 3.
        """
        results = []

        for rule in self.kb.rules:
            rule_symptom_codes = {s["code"] for s in rule["symptoms"]}

            # Cek apakah semua gejala rule ada di selected_symptoms
            if not rule_symptom_codes.issubset(set(selected_symptoms.keys())):
                continue

            # Hitung CF per gejala
            cf_evidences = []
            detail_steps = []
            for rs in rule["symptoms"]:
                cf_rule = self.calculate_cf_rule(rs["mb"], rs["md"])
                cf_user = selected_symptoms[rs["code"]]
                cf_evidence = self.calculate_cf_evidence(cf_user, cf_rule)
                cf_evidences.append(cf_evidence)
                detail_steps.append({
                    "symptom_code": rs["code"],
                    "mb": rs["mb"],
                    "md": rs["md"],
                    "cf_rule": round(cf_rule, 4),
                    "cf_user": cf_user,
                    "cf_evidence": round(cf_evidence, 4),
                })

            # Kombinasi CF secara bertahap
            cf_combined = self._combine_cfs(cf_evidences)

            # Detail kombinasi step-by-step
            combine_steps = []
            if len(cf_evidences) == 1:
                combine_steps.append({
                    "step": 1,
                    "cf_a": round(cf_evidences[0], 4),
                    "cf_b": None,
                    "result": round(cf_evidences[0], 4),
                })
            else:
                running = cf_evidences[0]
                for i, cf in enumerate(cf_evidences[1:], start=2):
                    new_running = self.combine_cf(running, cf)
                    combine_steps.append({
                        "step": i - 1,
                        "cf_a": round(running, 4),
                        "cf_b": round(cf, 4),
                        "result": round(new_running, 4),
                    })
                    running = new_running

            results.append({
                "problem_code": rule["target_problem"],
                "rule_code": rule["code"],
                "rule_name": rule.get("name", ""),
                "cf_final": round(cf_combined, 4),
                "details": {
                    "evidence_steps": detail_steps,
                    "combine_steps": combine_steps,
                },
            })

        results.sort(key=lambda x: x["cf_final"], reverse=True)
        return results[:3]

    def _combine_cfs(self, cf_list):
        """Kombinasikan list CF menggunakan rumus bertahap."""
        if not cf_list:
            return 0.0
        combined = cf_list[0]
        for cf in cf_list[1:]:
            combined = self.combine_cf(combined, cf)
        return combined

    @staticmethod
    def interpret_cf(cf_value):
        """Return label string berdasarkan nilai CF."""
        if cf_value >= 0.80:
            return "Sangat Yakin"
        elif cf_value >= 0.60:
            return "Cukup Yakin"
        elif cf_value >= 0.40:
            return "Kemungkinan"
        elif cf_value >= 0.20:
            return "Kurang Yakin"
        else:
            return "Tidak Yakin"
