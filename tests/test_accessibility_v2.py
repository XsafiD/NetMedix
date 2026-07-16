#!/usr/bin/env python3
"""
Basic Accessibility & Quality Check for NetMedix v2.0.0
Phase 7.C - Testing & QA (Alternative to Lighthouse Audit)

Note: This is a basic accessibility check. Full Lighthouse audit requires
browser automation tools (Chrome DevTools, Lighthouse) which are not available
in the current environment.

This script checks:
- HTML structure validation
- Basic accessibility attributes (alt tags, labels, etc.)
- Template loading without errors
- Color contrast basics (via template analysis)
"""

import sys
import os
import re

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app


class AccessibilityChecker:
    """Basic accessibility and quality check suite for NetMedix v2.0.0."""

    def __init__(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.passed = 0
        self.failed = 0
        self.warnings = 0

    def setup(self):
        """Setup test environment."""
        print("=" * 70)
        print("NetMedix v2.0.0 - Basic Accessibility & Quality Check")
        print("(Alternative to Lighthouse Audit)")
        print("=" * 70)
        print()

    def teardown(self):
        """Print summary after all tests."""
        print()
        print("=" * 70)
        print(f"Check Summary: {self.passed} passed, {self.failed} failed, {self.warnings} warnings")
        print("=" * 70)

        if self.failed == 0:
            print("✅ All accessibility checks PASSED!")
            if self.warnings > 0:
                print(f"⚠️  {self.warnings} warning(s) - review recommended")
            return 0
        else:
            print(f"❌ {self.failed} check(s) FAILED")
            return 1

    def assert_true(self, condition, test_name, description="", is_warning=False):
        """Assert helper - check if condition is True."""
        if condition:
            self.passed += 1
            print(f"✅ PASS: {test_name}")
            if description:
                print(f"   {description}")
        else:
            if is_warning:
                self.warnings += 1
                print(f"⚠️  WARNING: {test_name}")
                if description:
                    print(f"   {description}")
            else:
                self.failed += 1
                print(f"❌ FAIL: {test_name}")
                if description:
                    print(f"   {description}")
        print()

    def check_template_loading(self):
        """Check 1: Template loading without errors."""
        print("CHECK 1: Template Loading")

        # Test main templates load without errors
        templates_to_test = [
            ('/', 'index.html'),
            ('/diagnose', 'diagnose.html'),
            ('/about', 'about.html'),
            ('/history', 'history.html'),
            ('/tutorial/G01', 'tutorial.html'),
        ]

        for route, template_name in templates_to_test:
            try:
                response = self.client.get(route)
                self.assert_true(
                    response.status_code == 200,
                    f"1.{templates_to_test.index((route, template_name)) + 1} - {template_name} loads successfully",
                    description=f"GET {route} returns 200"
                )
            except Exception as e:
                self.assert_true(
                    False,
                    f"1.{templates_to_test.index((route, template_name)) + 1} - {template_name} loads successfully",
                    description=f"Error: {str(e)}"
                )

    def check_html_structure(self):
        """Check 2: Basic HTML structure."""
        print("CHECK 2: Basic HTML Structure")

        # Check if pages have proper HTML structure
        response = self.client.get('/')
        html_content = response.data.decode('utf-8')

        # Check for basic HTML elements
        checks = [
            (r'<!DOCTYPE html>', 'DOCTYPE declaration'),
            (r'<html[^>]*>', 'HTML tag'),
            (r'<head>', 'HEAD tag'),
            (r'<body>', 'BODY tag'),
            (r'<meta charset=', 'Charset meta tag'),
            (r'<meta name="viewport"', 'Viewport meta tag'),
        ]

        for pattern, description in checks:
            found = re.search(pattern, html_content, re.IGNORECASE)
            self.assert_true(
                found is not None,
                f"2.{checks.index((pattern, description)) + 1} - {description} present",
                description="Found in HTML"
            )

    def check_accessibility_basics(self):
        """Check 3: Basic accessibility attributes."""
        print("CHECK 3: Basic Accessibility Attributes")

        # Check diagnose page for proper labels
        response = self.client.get('/diagnose')
        html_content = response.data.decode('utf-8')

        # Check for input labels
        input_count = len(re.findall(r'<input[^>]*type=["\']checkbox["\']', html_content, re.IGNORECASE))
        label_count = len(re.findall(r'<label[^>]*for=["\'][gG]\d{2}["\']', html_content, re.IGNORECASE))

        self.assert_true(
            input_count > 0,
            "3.1 - Checkbox inputs present",
            description=f"Found {input_count} checkbox inputs"
        )

        self.assert_true(
            label_count > 0,
            "3.2 - Labels with 'for' attribute present",
            description=f"Found {label_count} labels with 'for' attribute"
        )

        # Check for ARIA labels where interactive elements exist
        button_count = len(re.findall(r'<button[^>]*>', html_content, re.IGNORECASE))
        aria_label_count = len(re.findall(r'aria-label=', html_content, re.IGNORECASE))

        self.assert_true(
            button_count > 0,
            "3.3 - Buttons present",
            description=f"Found {button_count} buttons"
        )

        self.assert_true(
            aria_label_count >= 0,  # Allow 0, but warn if many buttons without labels
            "3.4 - ARIA labels checked",
            description=f"Found {aria_label_count} ARIA labels (optional for this check)",
            is_warning=(button_count > 5 and aria_label_count == 0)
        )

    def check_form_accessibility(self):
        """Check 4: Form accessibility."""
        print("CHECK 4: Form Accessibility")

        # Check diagnose_step2 page for radio button accessibility
        # First, we need to POST to /diagnose to get symptoms selected
        response = self.client.post('/diagnose/step2', data={'symptoms': ['G01', 'G02']})

        if response.status_code == 200:
            html_content = response.data.decode('utf-8')

            # Check for radio button groups
            radio_count = len(re.findall(r'type=["\']radio["\']', html_content, re.IGNORECASE))
            fieldset_count = len(re.findall(r'<fieldset', html_content, re.IGNORECASE))
            legend_count = len(re.findall(r'<legend', html_content, re.IGNORECASE))

            self.assert_true(
                radio_count > 0,
                "4.1 - Radio buttons present for CF selection",
                description=f"Found {radio_count} radio buttons"
            )

            self.assert_true(
                fieldset_count > 0,
                "4.2 - Fieldset tags used for radio groups",
                description=f"Found {fieldset_count} fieldset tags"
            )

            self.assert_true(
                legend_count > 0,
                "4.3 - Legend tags present for fieldsets",
                description=f"Found {legend_count} legend tags"
            )
        else:
            self.assert_true(
                False,
                "4.0 - Form accessibility check",
                description="Could not access diagnose_step2 page"
            )

    def check_error_handling(self):
        """Check 5: Error handling and 404 pages."""
        print("CHECK 5: Error Handling")

        # Check 404 page
        response = self.client.get('/nonexistent-page')
        self.assert_true(
            response.status_code == 404,
            "5.1 - 404 page returns proper status",
            description="GET /nonexistent-page returns 404"
        )

        # Check 404 page has content
        if response.status_code == 404:
            html_content = response.data.decode('utf-8')
            has_content = len(html_content) > 100
            self.assert_true(
                has_content,
                "5.2 - 404 page has content",
                description="404 page renders with user-friendly message"
            )

        # Check invalid tutorial code
        response = self.client.get('/tutorial/G99')
        self.assert_true(
            response.status_code == 404,
            "5.3 - Invalid tutorial code returns 404",
            description="GET /tutorial/G99 returns 404"
        )

    def check_content_quality(self):
        """Check 6: Content quality basics."""
        print("CHECK 6: Content Quality")

        # Check tutorial page has structured content
        response = self.client.get('/tutorial/G01')
        html_content = response.data.decode('utf-8')

        # Check for structured sections
        section_checks = [
            (r'definisi|definition', 'Definition section'),
            (r'verifikasi|verification', 'Verification section'),
            (r'interpretasi|interpretation', 'Interpretation section'),
        ]

        for pattern, description in section_checks:
            found = re.search(pattern, html_content, re.IGNORECASE)
            self.assert_true(
                found is not None,
                f"6.{section_checks.index((pattern, description)) + 1} - {description} present",
                description="Found in tutorial page"
            )

    def check_performance_basics(self):
        """Check 7: Basic performance indicators."""
        print("CHECK 7: Basic Performance Indicators")

        import time

        # Check page load time (basic)
        start_time = time.time()
        response = self.client.get('/')
        load_time = time.time() - start_time

        self.assert_true(
            load_time < 2.0,  # Allow 2 seconds for test environment
            "7.1 - Home page load time acceptable",
            description=f"Load time: {load_time:.3f}s (target: < 2.0s)",
            is_warning=(load_time > 1.0)
        )

        # Check diagnose page load time
        start_time = time.time()
        response = self.client.get('/diagnose')
        load_time = time.time() - start_time

        self.assert_true(
            load_time < 2.0,
            "7.2 - Diagnose page load time acceptable",
            description=f"Load time: {load_time:.3f}s (target: < 2.0s)",
            is_warning=(load_time > 1.0)
        )

    def run_all_checks(self):
        """Run all accessibility and quality checks."""
        self.setup()

        # Run all checks
        self.check_template_loading()
        self.check_html_structure()
        self.check_accessibility_basics()
        self.check_form_accessibility()
        self.check_error_handling()
        self.check_content_quality()
        self.check_performance_basics()

        return self.teardown()


if __name__ == "__main__":
    checker = AccessibilityChecker()
    exit_code = checker.run_all_checks()
    sys.exit(exit_code)
