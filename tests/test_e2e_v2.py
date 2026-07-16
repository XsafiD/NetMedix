#!/usr/bin/env python3
"""
E2E Test untuk NetMedix v2.0.0 - Programmatic Testing
Phase 7.B - Testing & QA

Test scenarios sesuai todo-rombak-v2.0.0-NetMedix.md Phase 7.B:
- E2E-1: User flow lengkap: home → symptoms → diagnose → result
- E2E-2: Tooltip/modal info (data availability check)
- E2E-3: Link tutorial (route availability check)
- E2E-4: Skenario P02 (Internet putus)
- E2E-5: Skenario P05 (DHCP failure)
- E2E-6: Edge case < 2 gejala
- E2E-7: Histori diagnosis (database & route check)
- E2E-8: Data integrity checks (symptoms, rules)

Note: This is a programmatic E2E test. Full UI/UX testing would require
browser automation tools (Selenium, Playwright) or Chrome DevTools MCP.
"""

import sys
import os
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, init_db
from inference.knowledge_base import KnowledgeBase
from inference.engine import InferenceEngine as EngineClass


class E2ETester:
    """E2E Test suite untuk NetMedix v2.0.0."""

    def __init__(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.kb = KnowledgeBase()
        self.engine = EngineClass(self.kb)
        self.passed = 0
        self.failed = 0

    def setup(self):
        """Setup test environment."""
        print("=" * 70)
        print("NetMedix v2.0.0 - E2E Programmatic Test")
        print("=" * 70)
        print()
        # Initialize database
        init_db()

    def teardown(self):
        """Print summary after all tests."""
        print()
        print("=" * 70)
        print(f"E2E Test Summary: {self.passed} passed, {self.failed} failed")
        print("=" * 70)

        if self.failed == 0:
            print("✅ All E2E tests PASSED!")
            return 0
        else:
            print(f"❌ {self.failed} E2E test(s) FAILED")
            return 1

    def assert_true(self, condition, test_name, description=""):
        """Assert helper - check if condition is True."""
        if condition:
            self.passed += 1
            print(f"✅ PASS: {test_name}")
            if description:
                print(f"   {description}")
        else:
            self.failed += 1
            print(f"❌ FAIL: {test_name}")
            if description:
                print(f"   {description}")
        print()

    def assert_equals(self, actual, expected, test_name, tolerance=0.01, description=""):
        """Assert helper - check if actual equals expected."""
        if isinstance(expected, float):
            condition = abs(actual - expected) <= tolerance
        else:
            condition = actual == expected

        if condition:
            self.passed += 1
            print(f"✅ PASS: {test_name}")
            if description:
                print(f"   {description}")
        else:
            self.failed += 1
            print(f"❌ FAIL: {test_name}")
            print(f"   Expected: {expected}")
            print(f"   Actual: {actual}")
            if description:
                print(f"   {description}")
        print()

    def test_e2e_1_user_flow_basic(self):
        """
        E2E-1 — User flow lengkap: home → symptoms → diagnose → result
        Verify all routes return 200 status code.
        """
        print("TEST E2E-1: User flow basic route checks")

        # Test home page
        response = self.client.get('/')
        self.assert_equals(
            response.status_code,
            200,
            "E2E-1.1 - Home page accessible",
            description="GET / returns 200"
        )

        # Test diagnose page (symptoms selection)
        response = self.client.get('/diagnose')
        self.assert_equals(
            response.status_code,
            200,
            "E2E-1.2 - Diagnose page accessible",
            description="GET /diagnose returns 200"
        )

        # Test about page
        response = self.client.get('/about')
        self.assert_equals(
            response.status_code,
            200,
            "E2E-1.3 - About page accessible",
            description="GET /about returns 200"
        )

        # Test history page
        response = self.client.get('/history')
        self.assert_equals(
            response.status_code,
            200,
            "E2E-1.4 - History page accessible",
            description="GET /history returns 200"
        )

    def test_e2e_2_symptom_data_availability(self):
        """
        E2E-2 — Tooltip/modal info data availability
        Verify symptoms have short_desc and how_to_check fields.
        """
        print("TEST E2E-2: Symptom data availability for modal info")

        symptoms = self.kb.load_symptoms()
        symptoms_with_info = self.kb.get_symptoms_with_info()

        # Check all symptoms have required fields
        missing_count = 0
        for s in symptoms_with_info:
            if not s.get('short_desc') or not s.get('how_to_check'):
                missing_count += 1

        self.assert_equals(
            missing_count,
            0,
            "E2E-2.1 - All symptoms have info fields",
            description=f"All {len(symptoms_with_info)} symptoms have short_desc and how_to_check"
        )

        # Verify symptoms_with_info returns same count as symptoms
        self.assert_equals(
            len(symptoms_with_info),
            len(symptoms),
            "E2E-2.2 - Symptoms with info count matches",
            description=f"Both have {len(symptoms)} symptoms"
        )

    def test_e2e_3_tutorial_route(self):
        """
        E2E-3 — Link tutorial route availability
        Verify /tutorial/<code> route works for valid codes and 404 for invalid.
        """
        print("TEST E2E-3: Tutorial route availability")

        # Test valid symptom code
        response = self.client.get('/tutorial/G01')
        self.assert_equals(
            response.status_code,
            200,
            "E2E-3.1 - Tutorial page G01 accessible",
            description="GET /tutorial/G01 returns 200"
        )

        # Test invalid symptom code (should 404)
        response = self.client.get('/tutorial/G99')
        self.assert_equals(
            response.status_code,
            404,
            "E2E-3.2 - Tutorial page G99 returns 404",
            description="GET /tutorial/G99 returns 404 (invalid code)"
        )

        # Test lowercase code normalization
        response = self.client.get('/tutorial/g01')
        self.assert_equals(
            response.status_code,
            200,
            "E2E-3.3 - Tutorial page lowercase g01 accessible",
            description="GET /tutorial/g01 returns 200 (case normalized)"
        )

    def test_e2e_4_scenario_p02(self):
        """
        E2E-4 — Skenario P02 (Internet putus)
        Centang G02, G03, G28 → CF tinggi → submit → top result P02
        """
        print("TEST E2E-4: Scenario P02 (Internet Terputus)")

        # Simulate form submission for P02 symptoms
        # P02 symptoms: G02 (Tidak bisa akses internet), G03 (Gateway reachable, 8.8.8.8 RTO), G28 (Lampu WAN router mati)
        selected_symptoms = {
            "G02": 1.0,
            "G03": 1.0,
            "G28": 0.8
        }

        # Run diagnosis
        results = self.engine.diagnose(selected_symptoms)

        # Assert: results must not be empty
        self.assert_true(
            len(results) > 0,
            "E2E-4.1 - P02 scenario returns results",
            description="3 gejala P02 menghasilkan diagnosis"
        )

        if len(results) > 0:
            # Assert: P02 must be in results
            p02_result = None
            for r in results:
                if r["problem_code"] == "P02":
                    p02_result = r
                    break

            self.assert_true(
                p02_result is not None,
                "E2E-4.2 - P02 found in results",
                description="Problem P02 (Koneksi Internet Terputus) terdeteksi"
            )

            if p02_result:
                # Assert: P02 should be top result (high CF)
                top_result = results[0]
                self.assert_equals(
                    top_result["problem_code"],
                    "P02",
                    "E2E-4.3 - P02 is top result",
                    description="P02 harus jadi kandidat utama"
                )

                # Assert: CF should be high (≥ 0.80 for "Sangat Yakin")
                self.assert_true(
                    p02_result["cf_final"] >= 0.80,
                    "E2E-4.4 - P02 CF is high",
                    description=f"P02 CF {p02_result['cf_final']:.4f} ≥ 0.80 (Sangat Yakin)"
                )

                # Assert: matched 3 symptoms
                self.assert_equals(
                    p02_result["matched_count"],
                    3,
                    "E2E-4.5 - P02 matched 3 symptoms",
                    description="G02, G03, G28 semua match"
                )

    def test_e2e_5_scenario_p05(self):
        """
        E2E-5 — Skenario P05 (DHCP Failure)
        Centang G05, G30, G40 → CF tinggi → submit → top result P05
        """
        print("TEST E2E-5: Scenario P05 (DHCP Failure)")

        # Simulate form submission for P05 symptoms
        # P05 symptoms: G05 (IP address 169.254.x.x), G30 (Tidak ada DHCP server), G40 (IP address 0.0.0.0)
        selected_symptoms = {
            "G05": 1.0,
            "G30": 0.9,
            "G40": 0.9
        }

        # Run diagnosis
        results = self.engine.diagnose(selected_symptoms)

        # Assert: results must not be empty
        self.assert_true(
            len(results) > 0,
            "E2E-5.1 - P05 scenario returns results",
            description="3 gejala P05 menghasilkan diagnosis"
        )

        if len(results) > 0:
            # Assert: P05 must be in results
            p05_result = None
            for r in results:
                if r["problem_code"] == "P05":
                    p05_result = r
                    break

            self.assert_true(
                p05_result is not None,
                "E2E-5.2 - P05 found in results",
                description="Problem P05 (DHCP Failure) terdeteksi"
            )

            if p05_result:
                # Assert: P05 should be top result
                top_result = results[0]
                self.assert_equals(
                    top_result["problem_code"],
                    "P05",
                    "E2E-5.3 - P05 is top result",
                    description="P05 harus jadi kandidat utama"
                )

                # Assert: CF should be high
                self.assert_true(
                    p05_result["cf_final"] >= 0.80,
                    "E2E-5.4 - P05 CF is high",
                    description=f"P05 CF {p05_result['cf_final']:.4f} ≥ 0.80 (Sangat Yakin)"
                )

                # Assert: matched 3 symptoms
                self.assert_equals(
                    p05_result["matched_count"],
                    3,
                    "E2E-5.5 - P05 matched 3 symptoms",
                    description="G05, G30, G40 semua match"
                )

    def test_e2e_6_edge_case_single_symptom(self):
        """
        E2E-6 — Edge case < 2 gejala relevan
        Centang hanya G02 → submit → result page tampilkan empty state (bukan error)
        """
        print("TEST E2E-6: Edge case single symptom (< 2 gejala)")

        # Simulate form submission with only 1 symptom
        selected_symptoms = {"G02": 0.7}

        # Run diagnosis
        results = self.engine.diagnose(selected_symptoms)

        # Assert: results must be empty (filter ≥ 2 gejala relevan)
        self.assert_equals(
            len(results),
            0,
            "E2E-6.1 - Single symptom returns empty result",
            description="Filter ≥ 2 gejala relevan memblok diagnosis"
        )

        # Test build_kesimpulan helper with empty results
        from app import build_kesimpulan
        kesimpulan = build_kesimpulan(results)

        # Assert: kesimpulan should have status "empty"
        self.assert_equals(
            kesimpulan["status"],
            "empty",
            "E2E-6.2 - Empty result has proper kesimpulan status",
            description="Kesimpulan status is 'empty' dengan pesan yang jelas"
        )

        # Assert: kesimpulan should have message
        self.assert_true(
            len(kesimpulan.get("message", "")) > 0,
            "E2E-6.3 - Empty result has user-friendly message",
            description="Pesan tidak boleh kosong"
        )

    def test_e2e_7_history_database(self):
        """
        E2E-7 — Histori diagnosis
        Lakukan diagnosis → buka halaman histori → entry tampil dengan format baru.
        """
        print("TEST E2E-7: History database & route")

        # Create a test diagnosis
        selected_symptoms = {"G02": 1.0, "G03": 0.9, "G28": 0.8}
        results = self.engine.diagnose(selected_symptoms)

        # Save to database via app function
        from app import save_session
        session_id = save_session(selected_symptoms, results)

        # Assert: session_id should be valid (positive integer)
        self.assert_true(
            session_id > 0,
            "E2E-7.1 - Session saved to database",
            description=f"Session ID {session_id} berhasil dibuat"
        )

        # Test history route
        response = self.client.get('/history')
        self.assert_equals(
            response.status_code,
            200,
            "E2E-7.2 - History page accessible",
            description="GET /history returns 200"
        )

        # Test history detail route
        response = self.client.get(f'/history/{session_id}')
        # Should redirect to result page
        self.assert_true(
            response.status_code in [200, 302],  # 200 or redirect
            "E2E-7.3 - History detail accessible",
            description=f"GET /history/{session_id} returns valid status"
        )

        # Test result route with session_id
        response = self.client.get(f'/result/{session_id}')
        self.assert_equals(
            response.status_code,
            200,
            "E2E-7.4 - Result page with session_id accessible",
            description=f"GET /result/{session_id} returns 200"
        )

        # Verify data in result page
        self.assert_true(
            len(response.data) > 0,
            "E2E-7.5 - Result page has content",
            description="Result page renders with diagnosis data"
        )

    def test_e2e_8_data_integrity(self):
        """
        E2E-8 — Data integrity checks
        Verify symptoms.json, rules.json, problems.json have valid v2 schema.
        """
        print("TEST E2E-8: Data integrity checks")

        # Test symptoms.json
        symptoms = self.kb.load_symptoms()

        # Assert: symptoms should not be empty
        self.assert_true(
            len(symptoms) > 0,
            "E2E-8.1 - Symptoms loaded successfully",
            description=f"{len(symptoms)} symptoms loaded"
        )

        # Check v2 schema fields (short_desc, how_to_check, tutorial)
        symptoms_with_tutorial = 0
        for s in symptoms:
            if s.get('short_desc') and s.get('how_to_check') and s.get('tutorial'):
                symptoms_with_tutorial += 1

        self.assert_true(
            symptoms_with_tutorial >= len(symptoms) - 2,  # Allow 2 stub (G31, G32)
            "E2E-8.2 - Symptoms have v2 schema fields",
            description=f"{symptoms_with_tutorial}/{len(symptoms)} symptoms have full v2 fields (allowing 2 VPN stubs)"
        )

        # Test rules.json
        rules = self.kb.load_rules()

        # Assert: rules should not be empty
        self.assert_true(
            len(rules) > 0,
            "E2E-8.3 - Rules loaded successfully",
            description=f"{len(rules)} rules loaded"
        )

        # Check v2 schema fields (cf_pakar, evidence, sources)
        rules_with_v2_fields = 0
        for r in rules:
            # Check if rule has sources
            if r.get('sources') and len(r['sources']) >= 2:
                # Check if all symptoms have cf_pakar and evidence
                all_symptoms_valid = True
                for s in r.get('symptoms', []):
                    if not (s.get('cf_pakar') and s.get('evidence')):
                        all_symptoms_valid = False
                        break
                if all_symptoms_valid:
                    rules_with_v2_fields += 1

        self.assert_equals(
            rules_with_v2_fields,
            len(rules),
            "E2E-8.4 - Rules have v2 schema fields",
            description=f"All {len(rules)} rules have sources (≥2) and symptoms with cf_pakar + evidence"
        )

        # Test problems.json
        problems = self.kb.load_problems()

        # Assert: problems should not be empty
        self.assert_true(
            len(problems) > 0,
            "E2E-8.5 - Problems loaded successfully",
            description=f"{len(problems)} problems loaded"
        )

    def run_all_tests(self):
        """Run all E2E test scenarios."""
        self.setup()

        # Run all tests
        self.test_e2e_1_user_flow_basic()
        self.test_e2e_2_symptom_data_availability()
        self.test_e2e_3_tutorial_route()
        self.test_e2e_4_scenario_p02()
        self.test_e2e_5_scenario_p05()
        self.test_e2e_6_edge_case_single_symptom()
        self.test_e2e_7_history_database()
        self.test_e2e_8_data_integrity()

        return self.teardown()


if __name__ == "__main__":
    tester = E2ETester()
    exit_code = tester.run_all_tests()
    sys.exit(exit_code)
