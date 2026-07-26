#!/usr/bin/env python3
"""Test script untuk rendering cf_table.html"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask
from inference.knowledge_base import KnowledgeBase

app = Flask(__name__)

# Load data
kb = KnowledgeBase()
rules = kb.load_rules()
problems = kb.load_problems()
symptoms = kb.load_symptoms()

# Build enriched data per problem
problems_with_cf = []
for problem in problems:
    # Find rule for this problem
    rule = None
    for r in rules:
        if r.get('target_problem') == problem['code']:
            rule = r
            break

    # Extract CFpakar data per symptom
    cf_symptoms = []
    if rule:
        for sym in rule.get('symptoms', []):
            symptom_code = sym.get('code')
            cf_pakar = sym.get('cf_pakar', 0.0)
            evidence = sym.get('evidence', '')

            # Get symptom details
            symptom_detail = None
            for s in symptoms:
                if s.get('code') == symptom_code:
                    symptom_detail = s
                    break

            if symptom_detail:
                cf_symptoms.append({
                    'code': symptom_code,
                    'name': symptom_detail.get('name', ''),
                    'cf_pakar': cf_pakar,
                    'evidence': evidence
                })

    # Get source links from rule
    sources = rule.get('sources', []) if rule else []

    problems_with_cf.append({
        'problem': problem,
        'cf_symptoms': cf_symptoms,
        'sources': sources
    })

print('Data prepared successfully')
print(f'Problems with CF: {len(problems_with_cf)}')

# Test render template
try:
    with app.app_context():
        from flask import render_template
        html = render_template('cf_table.html', problems_with_cf=problems_with_cf)
        print('SUCCESS: Template rendered successfully!')
        print(f'HTML length: {len(html)} characters')
        # Save to file for inspection
        with open('/tmp/cf_table_test.html', 'w') as f:
            f.write(html)
        print('Saved to /tmp/cf_table_test.html')
except Exception as e:
    print(f'ERROR: {str(e)}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
