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

import pytest
from inference.knowledge_base import KnowledgeBase
from inference.engine import InferenceEngine


@pytest.fixture
def kb():
    """Fixture untuk KnowledgeBase instance."""
    return KnowledgeBase()


@pytest.fixture
def engine(kb):
    """Fixture untuk InferenceEngine instance dengan KnowledgeBase."""
    return InferenceEngine(kb)


@pytest.fixture
def cf_pakar_reference():
    """
    Fixture untuk referensi CF_pakar dari rules.json.
    Nilai-nilai ini digunakan untuk verifikasi manual calculation.

    P12 (Latensi Tinggi/Jitter):
    - G15: CF_pakar 0.95 (signature symptom)

    P15 (Kerusakan Router/Switch):
    - G19: CF_pakar 0.90 (lampu router mati/tidak normal)
    - G27: CF_pakar 0.70 (ping ke gateway IP RTO)
    - G34: CF_pakar 0.90 (switch port/link LED off)

    P02 (Koneksi Internet Terputus):
    - G02: CF_pakar 0.90 (tidak bisa akses internet)

    P11 (Packet Loss Tinggi):
    - G14: CF_pakar 0.90 (signature symptom)
    - G23: CF_pakar 0.60 (intermittent connection)

    P14 (Kerusakan Kabel):
    - G18: CF_pakar 0.95 (physical damage visible)
    - G29: CF_pakar 0.80 (kabel longgar)
    - G14: CF_pakar 0.70 (impact dari packet loss)

    G31 (VPN tidak bisa connect): Orphan permanen (tidak ada di rule manapun)
    """
    return {
        "P12": {"G15": 0.95},
        "P15": {"G19": 0.90, "G27": 0.70, "G34": 0.90},
        "P02": {"G02": 0.90},
        "P11": {"G14": 0.90, "G23": 0.60},
        "P14": {"G18": 0.95, "G29": 0.80, "G14": 0.70},
    }


class TestEngineV2Basic:
    """Test suite dasar untuk NetMedix v2.0.0 Inference Engine - Filter & Edge Cases."""

    def test_t1_single_symptom_p12_returns_empty(self, engine):
        """
        T1 — Single symptom P12: Input {G15: 0.7} → expected: empty result
        P12 "Latensi Tinggi/Jitter" butuh ≥ 2 gejala, jadi harus return empty.

        Test requirements:
        - Filter ≥ 2 gejala relevan harus aktif
        - Single symptom tidak cukup untuk trigger diagnosis
        """
        # Input: hanya G15 (Ping latensi tinggi) dengan CF_user 0.7
        selected_symptoms = {"G15": 0.7}

        # Run diagnosis
        results = engine.diagnose(selected_symptoms)

        # Assert: results harus empty (karena < 2 gejala relevan)
        assert len(results) == 0, (
            "T1 FAILED: Single symptom P12 harus return empty result. "
            f"Got {len(results)} results instead of 0. "
            "Filter ≥ 2 gejala relevan harus memblok P12."
        )

    def test_t3_single_symptom_relevant_p02_returns_empty(self, engine):
        """
        T3 — 1 gejala relevan saja: Input {G02: 0.7} → expected: empty
        P02 (Koneksi Internet Terputus) butuh ≥ 2 gejala.

        Test requirements:
        - Filter ≥ 2 gejala relevan harus konsisten untuk semua rule
        - Satu gejala walaupun relevan tidak cukup
        """
        # Input: hanya G02 (Tidak bisa akses internet)
        selected_symptoms = {"G02": 0.7}

        # Run diagnosis
        results = engine.diagnose(selected_symptoms)

        # Assert: results harus empty (P02 butuh ≥ 2 gejala)
        assert len(results) == 0, (
            "T3 FAILED: Single symptom P02 harus return empty result. "
            f"Got {len(results)} results instead of 0. "
            "P02 butuh ≥ 2 gejala (G02 saja tidak cukup)."
        )

    def test_t4_zero_symptoms_returns_empty(self, engine):
        """
        T4 — 0 gejala: Input {} → expected: empty result

        Test requirements:
        - Engine harus handle empty input gracefully
        - Tidak ada exception untuk input kosong
        """
        # Input: kosong
        selected_symptoms = {}

        # Run diagnosis
        results = engine.diagnose(selected_symptoms)

        # Assert: results harus empty
        assert len(results) == 0, (
            "T4 FAILED: Zero symptoms harus return empty result. "
            f"Got {len(results)} results instead of 0. "
            "Tanpa gejala, tidak ada diagnosis yang mungkin."
        )

    def test_t5_orphan_symptom_g31_returns_empty(self, engine):
        """
        T5 — Orphan gejala saja: Input {G31: 0.7} → expected: empty
        G31 (VPN tidak bisa connect) adalah orphan permanen (tidak ada di rule manapun).

        Test requirements:
        - Orphan symptoms (G31-G39 yang tidak masuk rule) harus tidak trigger diagnosis
        - Engine harus handle symptoms yang tidak ada di manapun
        """
        # Input: hanya G31 (VPN symptom - orphan)
        selected_symptoms = {"G31": 0.7}

        # Run diagnosis
        results = engine.diagnose(selected_symptoms)

        # Assert: results harus empty (G31 tidak ada di rule manapun)
        assert len(results) == 0, (
            "T5 FAILED: Orphan symptom G31 harus return empty result. "
            f"Got {len(results)} results instead of 0. "
            "G31 (VPN) adalah orphan permanen, tidak ada di rule manapun."
        )


class TestEngineV2Calculation:
    """Test suite untuk verifikasi perhitungan CF di NetMedix v2.0.0."""

    def test_t2_multi_symptom_p15_cf_calculation(self, engine, cf_pakar_reference):
        """
        T2 — Multi-symptom P15: Input {G19: 1.0, G27: 0.8, G34: 1.0}
        Expected: P15 muncul dengan CF sesuai manual calc dari tabel riset.

        Manual calc reference:
        P15 (Kerusakan Router/Switch) symptoms:
        - G19: Lampu router mati/tidak normal → CF_pakar 0.90
        - G27: Ping ke gateway IP RTO → CF_pakar 0.70
        - G34: Switch port/link LED off → CF_pakar 0.90

        Step 1: Hitung CF_evidence per gejala
        - G19: CF_evidence = 1.0 × 0.90 = 0.90
        - G27: CF_evidence = 0.8 × 0.70 = 0.56
        - G34: CF_evidence = 1.0 × 0.90 = 0.90

        Step 2: Combine sekuensial (left-to-right)
        - CF₁ = 0.90 (G19)
        - CF₂ = 0.90 + 0.56 × (1 - 0.90) = 0.90 + 0.056 = 0.956
        - CF₃ = 0.956 + 0.90 × (1 - 0.956) = 0.956 + 0.0396 = 0.9956

        Expected CF_final ≈ 0.996 (round to 4 decimals)
        """
        # Input: G19, G27, G34 dengan CF_user tinggi
        selected_symptoms = {"G19": 1.0, "G27": 0.8, "G34": 1.0}

        # Run diagnosis
        results = engine.diagnose(selected_symptoms)

        # Assert: results harus tidak empty
        assert len(results) > 0, (
            "T2 FAILED: P15 harus return non-empty result. "
            f"Got {len(results)} results. P15 punya 3 gejala relevan (G19, G27, G34)."
        )

        # Assert: P15 harus ada di results
        p15_result = next((r for r in results if r["problem_code"] == "P15"), None)
        assert p15_result is not None, (
            "T2 FAILED: P15 tidak ditemukan di results. "
            "Problem P15 (Kerusakan Router/Switch) harus terdeteksi."
        )

        # Manual calculation
        expected_cf = 0.9956
        actual_cf = p15_result["cf_final"]

        # Assert: CF_final harus mendekati 0.996 (manual calc)
        assert abs(actual_cf - expected_cf) <= 0.01, (
            f"T2 FAILED: P15 CF calculation incorrect. "
            f"Manual calc: {expected_cf:.4f}, Engine: {actual_cf:.4f}, "
            f"Difference: {abs(actual_cf - expected_cf):.4f}"
        )

        # Assert: matched_count harus 3 (semua gejala P15 match)
        assert p15_result["matched_count"] == 3, (
            f"T2 FAILED: P15 harus match 3 symptoms. "
            f"Got {p15_result['matched_count']}. Expected: G19, G27, G34 semua match."
        )

        # Assert: percentage harus CF × 100
        expected_percentage = round(expected_cf * 100, 2)  # 99.56
        actual_percentage = p15_result["percentage"]
        assert abs(actual_percentage - expected_percentage) <= 0.1, (
            f"T2 FAILED: P15 percentage incorrect. "
            f"Expected {expected_percentage}%, got {actual_percentage}%"
        )

        # Assert: label harus "Sangat Yakin" (CF ≥ 0.80)
        assert p15_result["label"] == "Sangat Yakin", (
            f"T2 FAILED: P15 label must be 'Sangat Yakin'. Got '{p15_result['label']}'. "
            f"CF {actual_cf:.4f} ≥ 0.80"
        )

    def test_t6_cross_cutting_symptoms_p11_p14(self, engine, cf_pakar_reference):
        """
        T6 — Cross-cutting: Input {G14: 0.9, G23: 0.7, G18: 0.8, G29: 0.9}
        Expected: P11 (G14+G23) DAN P14 (G18+G29+G14) muncul, sort desc by CF.

        Manual calc reference:
        P11 (Packet Loss Tinggi) - symptoms: G14, G23
        - G14: CF_pakar 0.90 → CF_evidence = 0.9 × 0.9 = 0.81
        - G23: CF_pakar 0.60 → CF_evidence = 0.7 × 0.6 = 0.42
        - CF_combine = 0.81 + 0.42 × (1 - 0.81) = 0.81 + 0.0798 = 0.8898

        P14 (Kerusakan Kabel) - symptoms: G18, G29, G14
        - G18: CF_pakar 0.95 → CF_evidence = 0.8 × 0.95 = 0.76
        - G29: CF_pakar 0.80 → CF_evidence = 0.9 × 0.8 = 0.72
        - G14: CF_pakar 0.70 → CF_evidence = 0.9 × 0.7 = 0.63
        - CF_combine step 1: 0.76 + 0.72 × (1 - 0.76) = 0.76 + 0.1728 = 0.9328
        - CF_combine step 2: 0.9328 + 0.63 × (1 - 0.9328) = 0.9328 + 0.0423 = 0.9751

        Expected order: P14 (CF ~0.975) > P11 (CF ~0.890)
        """
        # Input: G14, G23, G18, G29 dengan CF_user beragam
        selected_symptoms = {"G14": 0.9, "G23": 0.7, "G18": 0.8, "G29": 0.9}

        # Run diagnosis
        results = engine.diagnose(selected_symptoms)

        # Assert: results harus tidak empty
        assert len(results) >= 2, (
            f"T6 FAILED: Cross-cutting harus return at least 2 results. Got {len(results)}. "
            "P11 (G14+G23) dan P14 (G18+G29+G14) harus muncul."
        )

        # Assert: P11 dan P14 harus ada di results
        p11_result = next((r for r in results if r["problem_code"] == "P11"), None)
        p14_result = next((r for r in results if r["problem_code"] == "P14"), None)

        assert p11_result is not None, (
            "T6 FAILED: P11 tidak ditemukan di results. "
            "P11 (Packet Loss Tinggi) harus terdeteksi dari G14 + G23."
        )

        assert p14_result is not None, (
            "T6 FAILED: P14 tidak ditemukan di results. "
            "P14 (Kerusakan Kabel) harus terdeteksi dari G18 + G29 + G14."
        )

        # Assert: P14 harus lebih tinggi CF-nya daripada P11
        assert p14_result["cf_final"] > p11_result["cf_final"], (
            f"T6 FAILED: P14 CF harus > P11 CF. "
            f"P14: {p14_result['cf_final']:.4f}, P11: {p11_result['cf_final']:.4f}"
        )

        # Assert: P14 harus di index 0 (top result)
        assert results[0]["problem_code"] == "P14", (
            f"T6 FAILED: P14 harus jadi top result. Got {results[0]['problem_code']} instead."
        )

        # Assert: Verify CF P14 (manual calc: 0.9751)
        expected_p14_cf = 0.9751
        actual_p14_cf = p14_result["cf_final"]
        assert abs(actual_p14_cf - expected_p14_cf) <= 0.01, (
            f"T6 FAILED: P14 CF calculation incorrect. "
            f"Manual calc: {expected_p14_cf:.4f}, Engine: {actual_p14_cf:.4f}"
        )

        # Assert: Verify CF P11 (manual calc: 0.8898)
        expected_p11_cf = 0.8898
        actual_p11_cf = p11_result["cf_final"]
        assert abs(actual_p11_cf - expected_p11_cf) <= 0.01, (
            f"T6 FAILED: P11 CF calculation incorrect. "
            f"Manual calc: {expected_p11_cf:.4f}, Engine: {actual_p11_cf:.4f}"
        )

        # Assert: P14 matched 3 symptoms (G18, G29, G14)
        assert p14_result["matched_count"] == 3, (
            f"T6 FAILED: P14 harus match 3 symptoms. Got {p14_result['matched_count']}. "
            "Expected: G18, G29, G14 semua match."
        )

        # Assert: P11 matched 2 symptoms (G14, G23)
        assert p11_result["matched_count"] == 2, (
            f"T6 FAILED: P11 harus match 2 symptoms. Got {p11_result['matched_count']}. "
            "Expected: G14, G23 semua match."
        )


class TestEngineV2EdgeCases:
    """Test suite untuk edge cases dan boundary conditions."""

    def test_cf_user_boundary_values(self, engine):
        """Test CF_user pada boundary values (0.1 dan 1.0)."""
        # Test dengan CF_user minimum (0.1)
        selected_min = {"G19": 0.1, "G27": 0.1, "G34": 0.1}
        results_min = engine.diagnose(selected_min)

        assert len(results_min) > 0, "Minimum CF_user (0.1) harus masih trigger diagnosis"

        p15_min = next((r for r in results_min if r["problem_code"] == "P15"), None)
        assert p15_min is not None, "P15 harus terdeteksi dengan CF_user minimum"

    def test_all_symptoms_for_single_problem(self, engine):
        """Test dengan semua gejala untuk satu problem (P15)."""
        all_p15_symptoms = {"G19": 1.0, "G27": 1.0, "G34": 1.0}
        results = engine.diagnose(all_p15_symptoms)

        p15_result = next((r for r in results if r["problem_code"] == "P15"), None)
        assert p15_result is not None, "P15 harus terdeteksi"
        assert p15_result["matched_count"] == 3, "Semua 3 gejala P15 harus match"

    def test_multiple_problems_triggered(self, engine):
        """Test bahwa multiple problems bisa muncul simultaneously."""
        # Input yang trigger P11, P14, dan P15
        selected = {
            "G14": 0.9,  # P11 & P14
            "G23": 0.7,  # P11
            "G18": 0.8,  # P14
            "G29": 0.9,  # P14
            "G19": 1.0,  # P15
            "G27": 0.8,  # P15
            "G34": 1.0,  # P15
        }

        results = engine.diagnose(selected)

        # Harus ada minimal 3 problems (P11, P14, P15)
        problem_codes = [r["problem_code"] for r in results]
        assert "P11" in problem_codes, "P11 harus muncul"
        assert "P14" in problem_codes, "P14 harus muncul"
        assert "P15" in problem_codes, "P15 harus muncul"

    def test_results_sorted_by_cf_desc(self, engine):
        """Test bahwa results selalu di-sort descending by CF."""
        # Input yang trigger multiple problems
        selected = {"G14": 0.9, "G23": 0.7, "G18": 0.8, "G29": 0.9}
        results = engine.diagnose(selected)

        # Verify descending order
        for i in range(len(results) - 1):
            assert results[i]["cf_final"] >= results[i+1]["cf_final"], (
                f"Results harus di-sort descending. "
                f"Index {i}: {results[i]['cf_final']:.4f}, "
                f"Index {i+1}: {results[i+1]['cf_final']:.4f}"
            )

    def test_result_structure_completeness(self, engine):
        """Test bahwa setiap result memiliki semua field yang diperlukan."""
        selected = {"G19": 1.0, "G27": 0.8, "G34": 1.0}
        results = engine.diagnose(selected)

        required_fields = [
            "problem_code", "problem_name", "category", "rule_code",
            "cf_final", "percentage", "label", "matched_count",
            "total_symptoms_in_rule", "details"
        ]

        for result in results:
            for field in required_fields:
                assert field in result, f"Field '{field}' tidak ada di result"

            # Check details structure
            assert "evidence_steps" in result["details"]
            assert "combine_steps" in result["details"]


class TestEngineV2EvidenceSteps:
    """Test suite untuk verifikasi evidence steps dan combine steps."""

    def test_evidence_steps_structure(self, engine):
        """Test structure evidence_steps untuk setiap gejala."""
        selected = {"G19": 1.0, "G27": 0.8, "G34": 1.0}
        results = engine.diagnose(selected)

        p15_result = next((r for r in results if r["problem_code"] == "P15"), None)
        assert p15_result is not None, "P15 harus ditemukan"

        evidence_steps = p15_result["details"]["evidence_steps"]

        # Harus ada 3 evidence steps (satu per gejala)
        assert len(evidence_steps) == 3, f"Harus ada 3 evidence steps, got {len(evidence_steps)}"

        # Check structure setiap evidence step
        for step in evidence_steps:
            required_fields = ["symptom_code", "cf_pakar", "cf_user", "cf_evidence"]
            for field in required_fields:
                assert field in step, f"Field '{field}' tidak ada di evidence step"

    def test_combine_steps_structure(self, engine):
        """Test structure combine_steps untuk sequential combination."""
        selected = {"G19": 1.0, "G27": 0.8, "G34": 1.0}
        results = engine.diagnose(selected)

        p15_result = next((r for r in results if r["problem_code"] == "P15"), None)
        assert p15_result is not None, "P15 harus ditemukan"

        combine_steps = p15_result["details"]["combine_steps"]

        # Untuk 3 gejala, harus ada 2 combine steps (step 1 dan step 2)
        assert len(combine_steps) == 2, f"Harus ada 2 combine steps, got {len(combine_steps)}"

        # Check structure setiap combine step
        for step in combine_steps:
            required_fields = ["step", "cf_a", "cf_b", "result"]
            for field in required_fields:
                assert field in step, f"Field '{field}' tidak ada di combine step"


if __name__ == "__main__":
    # Run tests dengan pytest
    pytest.main([__file__, "-v", "--tb=short"])
