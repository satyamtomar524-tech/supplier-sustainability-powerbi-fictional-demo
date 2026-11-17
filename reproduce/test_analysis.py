"""Contract tests for the authored scenario and generated Power BI snapshot."""
import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def records(name):
    with (ROOT / 'r_outputs' / name).open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def model_rows(name):
    text = (ROOT / 'SYNTHETIC Supplier Evidence Demo.SemanticModel' / 'definition' /
            'tables' / (name + '.tmdl')).read_text(encoding='utf-8')
    match = re.search(r'Rows = #table\(\{([^\n]+)\}, \{\n(.*?)\n\t+\}\),', text, re.S)
    columns = json.loads('[' + match[1] + ']')
    rows = json.loads('[' + match[2].replace('{', '[').replace('}', ']') + ']')
    return [dict(zip(columns, row)) for row in rows]


class ScenarioContract(unittest.TestCase):
    def test_raw_to_clean_reconciliation(self):
        metrics = {r['Metric']: float(r['Value']) for r in records('metrics.csv')}
        expected = {'candidate_labels': 8, 'reviewed_labels': 6, 'usable_labels': 2,
                    'follow_up_labels': 6, 'raw_supplier_cells': 11, 'occurrences': 10,
                    'excluded_placeholders': 1, 'raw_evidence_rows': 9, 'evidence_claims': 8,
                    'exact_evidence_duplicates': 1, 'review_coverage': .75,
                    'usable_coverage': .25, 'A_energy_change_pct': -.2}
        for key, value in expected.items():
            self.assertAlmostEqual(metrics[key], value, places=10, msg=key)

    def test_action_groups_are_correct(self):
        labels = model_rows('Labels')
        self.assertEqual({r['LabelID'] for r in labels if r['Priority'] == 'P1'}, {'FB', 'FC'})
        self.assertEqual({r['LabelID'] for r in labels if r['Usable']}, {'FA', 'FG'})
        self.assertEqual(next(r for r in labels if r['LabelID'] == 'FE')['Reason'], 'Missing unit')
        self.assertTrue(all(r['Next action'] for r in labels))

    def test_filter_populations(self):
        labels = model_rows('Labels')
        for technology, reviewed, usable in [('Machining', 2, 1), ('Finishing', 1, 0),
                                            ('Automation', 2, 0), ('Forming', 1, 1)]:
            chosen = [r for r in labels if r['Technology'] == technology]
            self.assertEqual(len(chosen), 2)
            self.assertEqual(sum(r['Review'] == 'Reviewed' for r in chosen), reviewed)
            self.assertEqual(sum(r['Usable'] for r in chosen), usable)

    def test_occurrences_do_not_change_label_grain(self):
        self.assertEqual(len([r for r in model_rows('Occurrences') if r['LabelID'] == 'FA']), 2)
        self.assertEqual(len([r for r in model_rows('Labels') if r['LabelID'] == 'FA']), 1)
        self.assertEqual(len({r['evidence_id'] for r in model_rows('Evidence')}), 8)

    def test_measured_values_keep_scope_and_unit(self):
        evidence = model_rows('Evidence')
        a = {r['Year']: r for r in evidence if r['LabelID'] == 'FA'}
        self.assertEqual({r['Unit'] for r in a.values()}, {'MWh'})
        self.assertEqual({r['Scope'] for r in a.values()}, {'Site'})
        self.assertAlmostEqual(a[2024]['Value'] / a[2023]['Value'] - 1, -.2)
        b = next(r for r in evidence if r['LabelID'] == 'FB')
        self.assertEqual((b['Unit'], b['Scope'], b['Assessment']), ('kWh/unit', 'Group', 'Scope mismatch'))

    def test_snapshot_matches_independent_R(self):
        model = {r['LabelID']: r for r in model_rows('Labels')}
        for r in records('labels.csv'):
            for column in ['Review', 'Identity', 'Priority', 'Reason']:
                self.assertEqual(model[r['LabelID']][column], r[column])
        self.assertEqual(len(model_rows('Occurrences')), len(records('occurrences.csv')))
        self.assertEqual(len(model_rows('Evidence')), len(records('evidence.csv')))

    def test_visual_fields_and_keyboard_order(self):
        model = {name: set(model_rows(name)[0]) for name in ['Labels', 'Evidence', 'Occurrences', 'Data Quality']}
        measures = {'Candidate Labels', 'Review Coverage %', 'Usable Labels', 'Follow Up Labels'}
        root = ROOT / 'SYNTHETIC Supplier Evidence Demo.Report/definition/pages'
        for page in root.iterdir():
            if not page.is_dir():
                continue
            visuals = [json.loads(p.read_text(encoding='utf-8')) for p in page.glob('visuals/*/visual.json')]
            self.assertEqual([v['name'] for v in sorted(visuals, key=lambda v: -v['position']['tabOrder'])],
                             [v['name'] for v in sorted(visuals, key=lambda v: (v['position']['y'], v['position']['x']))])
            for v in visuals:
                pos = v['position']
                self.assertLessEqual(pos['x'] + pos['width'], 1280)
                self.assertLessEqual(pos['y'] + pos['height'], 720)
                self.assertTrue(v['visual']['visualContainerObjects']['general'][0]['properties']['altText'])
                for spec in v['visual'].get('query', {}).get('queryState', {}).values():
                    for projection in spec['projections']:
                        kind, field = next(iter(projection['field'].items()))
                        self.assertIn(field['Property'], measures if kind == 'Measure' else model[field['Expression']['SourceRef']['Entity']])


if __name__ == '__main__':
    unittest.main(verbosity=2)
