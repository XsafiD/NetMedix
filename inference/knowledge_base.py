import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


class KnowledgeBase:
    def __init__(self):
        self.problems = self._load("problems.json")
        self.symptoms = self._load("symptoms.json")
        self.rules = self._load("rules.json")

    def _load(self, filename):
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

    def get_problem_by_code(self, code):
        """Cari problem berdasarkan kode (e.g. 'P01')."""
        for p in self.problems:
            if p["code"] == code:
                return p
        return None

    def get_symptom_by_code(self, code):
        """Cari symptom berdasarkan kode (e.g. 'G01')."""
        for s in self.symptoms:
            if s["code"] == code:
                return s
        return None

    def get_symptoms_by_category(self, category):
        """Filter symptoms berdasarkan kategori."""
        return [s for s in self.symptoms if s.get("category") == category]

    def get_categories(self):
        """Return list unik kategori gejala (preserve order)."""
        seen = []
        for s in self.symptoms:
            cat = s.get("category")
            if cat and cat not in seen:
                seen.append(cat)
        return seen

    def get_rules_for_symptoms(self, symptom_codes):
        """Cari rules yang relevant — semua gejala rule ada di symptom_codes."""
        symptom_set = set(symptom_codes)
        relevant = []
        for rule in self.rules:
            rule_symptom_codes = {s["code"] for s in rule["symptoms"]}
            if rule_symptom_codes.issubset(symptom_set):
                relevant.append(rule)
        return relevant
