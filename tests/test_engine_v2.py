#!/usr/bin/env python3
"""
Unit Test untuk NetMedix v2.0.0 - Pure CF Inference Engine
Phase 7.A - Testing & QA

Test scenarios sesuai todo-rombak-v2.0.0-NetMedix.md Phase 7.A:
- T1: Single symptom P12 → empty (filter ≥ 2)
- T2: Multi-symptom P15 → verify CF calculation
- T3: Single symptom relevant (P02) → empty
- T4: 0 gejala → empty
- T5: Orphan gejala (G31) → empty
- T6: Cross-cutting symptoms → P11 & P14 muncul

Manual calc reference dari tabel CF_pakar di docs-NetMedix/tabel-cf-pakar-riset.md
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.knowledge_base import KnowledgeBase
from inference.engine import InferenceEngine


class TestEngineV2:
    """Test suite untuk NetMedix v2.0.0 Inference Engine."""

    def __init__(self):
        self.kb = KnowledgeBase()
        self.engine = InferenceEngine(self.kb)
        self.results = []
        self.passed = 0
        self.failed = 0

    def setup(self):
        """Setup test environment."""
        print("=" * 70)
        print("NetMedix v2.0.0 - Inference Engine Unit Test")
        print("=" * 70)
        print()

    def teardown(self):
        """Print summary after all tests."""
        print()
        print("=" * 70)
        print(f"Test Summary: {self.passed} passed, {self.failed} failed")
        print("=" * 70)

        if self.failed == 0:
            print("✅ All tests PASSED!")
            return 0
        else:
            print(f"❌ {self.failed} test(s) FAILED")
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
        """Assert helper - check if actual equals expected (with tolerance for floats)."""
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

    def test_t1_single_symptom_p12(self):
        """
        T1 — Single symptom P12: Input {G15: 0.7} → expected: empty result
        P12 "Latensi Tinggi/Jitter" butuh ≥ 2 gejala, jadi harus return empty.
        """
        print("TEST T1: Single symptom P12 (should return empty)")

        # Input: hanya G15 (Ping latensi tinggi) dengan CF_user 0.7
        selected_symptoms = {"G15": 0.7}

        # Run diagnosis
        results = self.engine.diagnose(selected_symptoms)

        # Assert: results harus empty (karena < 2 gejala relevan)
        self.assert_equals(
            len(results),
            0,
            "T1 - Single symptom P12 returns empty result",
            description="Filter ≥ 2 gejala relevan harus memblok P12"
        )

    def test_t2_multi_symptom_p15(self):
        """
        T2 — Multi-symptom P15: Input {G19: 1.0, G27: 0.8, G34: 1.0}
        Expected: P15 muncul dengan CF sesuai manual calc dari tabel riset.

        Manual calc reference (dari rules.json aktual):
        P15 (Kerusakan Router/Switch) symptoms:
        - G19: Lampu router mati/tidak normal → CF_pakar 0.9
        - G27: Ping ke gateway IP RTO → CF_pakar 0.7
        - G34: Switch port/link LED off → CF_pakar 0.9

        Step 1: Hitung CF_evidence per gejala
        - G19: CF_evidence = 1.0 × 0.9 = 0.9
        - G27: CF_evidence = 0.8 × 0.7 = 0.56
        - G34: CF_evidence = 1.0 × 0.9 = 0.9

        Step 2: Combine sekuensial
        - CF₁ = 0.9 (G19)
        - CF₂ = 0.9 + 0.56 × (1 - 0.9) = 0.9 + 0.56 × 0.1 = 0.9 + 0.056 = 0.956
        - CF₃ = 0.956 + 0.9 × (1 - 0.956) = 0.956 + 0.9 × 0.044 = 0.956 + 0.0396 = 0.9956

        Expected CF_final ≈ 0.996 (round to 4 decimals)
        """
        print("TEST T2: Multi-symptom P15 (should return P15 with high CF)")

        # Input: G19, G27, G34 dengan CF_user tinggi
        selected_symptoms = {"G19": 1.0, "G27": 0.8, "G34": 1.0}

        # Run diagnosis
        results = self.engine.diagnose(selected_symptoms)

        # Assert: results harus tidak empty
        self.assert_true(
            len(results) > 0,
            "T2 - P15 returns non-empty result",
            description="P15 punya 3 gejala relevan (G19, G27, G34)"
        )

        # Assert: P15 harus ada di results
        p15_result = None
        for r in results:
            if r["problem_code"] == "P15":
                p15_result = r
                break

        self.assert_true(
            p15_result is not None,
            "T2 - P15 found in results",
            description="Problem P15 (Kerusakan Router/Switch) terdeteksi"
        )

        if p15_result:
            # Assert: CF_final harus mendekati 0.996 (manual calc)
            expected_cf = 0.9956
            actual_cf = p15_result["cf_final"]

            self.assert_equals(
                actual_cf,
                expected_cf,
                "T2 - P15 CF calculation correct",
                tolerance=0.01,
                description=f"Manual calc: {expected_cf:.4f}, Engine: {actual_cf:.4f}"
            )

            # Assert: matched_count harus 3 (semua gejala P15 match)
            self.assert_equals(
                p15_result["matched_count"],
                3,
                "T2 - P15 matched 3 symptoms",
                description="G19, G27, G34 semua match"
            )

            # Assert: percentage harus CF × 100
            # Note: percentage is calculated from rounded CF, so use expected_cf rounded to 4 decimals first
            expected_percentage = round(0.9956 * 100, 2)  # 99.56
            actual_percentage = p15_result["percentage"]

            self.assert_equals(
                actual_percentage,
                expected_percentage,
                "T2 - P15 percentage correct",
                tolerance=0.1,
                description=f"Expected {expected_percentage}%, got {actual_percentage}%"
            )

            # Assert: label harus "Sangat Yakin" (CF ≥ 0.80)
            self.assert_equals(
                p15_result["label"],
                "Sangat Yakin",
                "T2 - P15 label is 'Sangat Yakin'",
                description="CF 0.998 ≥ 0.80"
            )

    def test_t3_single_symptom_relevant_p02(self):
        """
        T3 — 1 gejala relevan saja: Input {G02: 0.7} → expected: empty
        P02 (Koneksi Internet Terputus) butuh ≥ 2 gejala.
        """
        print("TEST T3: Single symptom relevant to P02 (should return empty)")

        # Input: hanya G02 (Tidak bisa akses internet)
        selected_symptoms = {"G02": 0.7}

        # Run diagnosis
        results = self.engine.diagnose(selected_symptoms)

        # Assert: results harus empty (P02 butuh ≥ 2 gejala)
        self.assert_equals(
            len(results),
            0,
            "T3 - Single symptom P02 returns empty result",
            description="P02 butuh ≥ 2 gejala (G02 saja tidak cukup)"
        )

    def test_t4_zero_symptoms(self):
        """
        T4 — 0 gejala: Input {} → expected: empty result
        """
        print("TEST T4: Zero symptoms (should return empty)")

        # Input: kosong
        selected_symptoms = {}

        # Run diagnosis
        results = self.engine.diagnose(selected_symptoms)

        # Assert: results harus empty
        self.assert_equals(
            len(results),
            0,
            "T4 - Zero symptoms returns empty result",
            description="Tanpa gejala, tidak ada diagnosis yang mungkin"
        )

    def test_t5_orphan_symptom_g31(self):
        """
        T5 — Orphan gejala saja: Input {G31: 0.7} → expected: empty
        G31 (VPN tidak bisa connect) adalah orphan permanen (tidak ada di rule manapun).
        """
        print("TEST T5: Orphan symptom G31 (should return empty)")

        # Input: hanya G31 (VPN symptom - orphan)
        selected_symptoms = {"G31": 0.7}

        # Run diagnosis
        results = self.engine.diagnose(selected_symptoms)

        # Assert: results harus empty (G31 tidak ada di rule manapun)
        self.assert_equals(
            len(results),
            0,
            "T5 - Orphan symptom G31 returns empty result",
            description="G31 (VPN) adalah orphan permanen, tidak ada di rule manapun"
        )

    def test_t6_cross_cutting_symptoms(self):
        """
        T6 — Cross-cutting: Input {G14: 0.9, G23: 0.7, G18: 0.8, G29: 0.9}
        Expected: P11 (G14+G23) DAN P14 (G18+G29+G14) muncul, sort desc by CF.

        Manual calc reference:
        P11 (Packet Loss Tinggi) - symptoms: G14, G23
        - G14: CF_pakar 0.90 → CF_evidence = 0.9 × 0.9 = 0.81
        - G23: CF_pakar 0.60 → CF_evidence = 0.7 × 0.6 = 0.42
        - CF_combine = 0.81 + 0.42 × (1 - 0.81) = 0.81 + 0.42 × 0.19 = 0.81 + 0.0798 = 0.8898

        P14 (Kerusakan Kabel) - symptoms: G18, G29, G14
        - G18: CF_pakar 0.95 → CF_evidence = 0.8 × 0.95 = 0.76
        - G29: CF_pakar 0.80 → CF_evidence = 0.9 × 0.8 = 0.72
        - G14: CF_pakar 0.70 → CF_evidence = 0.9 × 0.7 = 0.63
        - CF_combine step 1: 0.76 + 0.72 × (1 - 0.76) = 0.76 + 0.72 × 0.24 = 0.76 + 0.1728 = 0.9328
        - CF_combine step 2: 0.9328 + 0.63 × (1 - 0.9328) = 0.9328 + 0.63 × 0.0672 = 0.9328 + 0.0423 = 0.9751

        Expected order: P14 (CF ~0.975) > P11 (CF ~0.890)
        """
        print("TEST T6: Cross-cutting symptoms (P11 & P14 should appear)")

        # Input: G14, G23, G18, G29 dengan CF_user beragam
        selected_symptoms = {"G14": 0.9, "G23": 0.7, "G18": 0.8, "G29": 0.9}

        # Run diagnosis
        results = self.engine.diagnose(selected_symptoms)

        # Assert: results harus tidak empty
        self.assert_true(
            len(results) >= 2,
            "T6 - Cross-cutting returns at least 2 results",
            description="P11 (G14+G23) dan P14 (G18+G29+G14) harus muncul"
        )

        if len(results) >= 2:
            # Assert: P11 dan P14 harus ada di results
            p11_result = None
            p14_result = None

            for r in results:
                if r["problem_code"] == "P11":
                    p11_result = r
                elif r["problem_code"] == "P14":
                    p14_result = r

            self.assert_true(
                p11_result is not None,
                "T6 - P11 found in results",
                description="P11 (Packet Loss Tinggi) terdeteksi"
            )

            self.assert_true(
                p14_result is not None,
                "T6 - P14 found in results",
                description="P14 (Kerusakan Kabel) terdeteksi"
            )

            if p11_result and p14_result:
                # Assert: P14 harus lebih tinggi CF-nya daripada P11
                self.assert_true(
                    p14_result["cf_final"] > p11_result["cf_final"],
                    "T6 - P14 CF > P11 CF (correct order)",
                    description=f"P14: {p14_result['cf_final']:.4f} > P11: {p11_result['cf_final']:.4f}"
                )

                # Assert: P14 harus di index 0 (top result)
                self.assert_equals(
                    results[0]["problem_code"],
                    "P14",
                    "T6 - P14 is top result",
                    description="P14 harus jadi kandidat utama"
                )

                # Assert: Verify CF P14
                expected_p14_cf = 0.9751  # Manual calc
                actual_p14_cf = p14_result["cf_final"]

                self.assert_equals(
                    actual_p14_cf,
                    expected_p14_cf,
                    "T6 - P14 CF calculation correct",
                    tolerance=0.01,
                    description=f"Manual calc: {expected_p14_cf:.4f}, Engine: {actual_p14_cf:.4f}"
                )

                # Assert: Verify CF P11
                expected_p11_cf = 0.8898  # Manual calc
                actual_p11_cf = p11_result["cf_final"]

                self.assert_equals(
                    actual_p11_cf,
                    expected_p11_cf,
                    "T6 - P11 CF calculation correct",
                    tolerance=0.01,
                    description=f"Manual calc: {expected_p11_cf:.4f}, Engine: {actual_p11_cf:.4f}"
                )

                # Assert: P14 matched 3 symptoms (G18, G29, G14)
                self.assert_equals(
                    p14_result["matched_count"],
                    3,
                    "T6 - P14 matched 3 symptoms",
                    description="G18, G29, G14 semua match"
                )

                # Assert: P11 matched 2 symptoms (G14, G23)
                self.assert_equals(
                    p11_result["matched_count"],
                    2,
                    "T6 - P11 matched 2 symptoms",
                    description="G14, G23 semua match"
                )

    def run_all_tests(self):
        """Run all test scenarios."""
        self.setup()

        # Run all tests
        self.test_t1_single_symptom_p12()
        self.test_t2_multi_symptom_p15()
        self.test_t3_single_symptom_relevant_p02()
        self.test_t4_zero_symptoms()
        self.test_t5_orphan_symptom_g31()
        self.test_t6_cross_cutting_symptoms()

        return self.teardown()


if __name__ == "__main__":
    tester = TestEngineV2()
    exit_code = tester.run_all_tests()
    sys.exit(exit_code)
