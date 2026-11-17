"""Regression checks for regeneration after Desktop Save and invalid inputs."""
import csv
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
MODEL = 'SYNTHETIC Supplier Evidence Demo.SemanticModel'
RSCRIPT = os.environ.get('RSCRIPT') or shutil.which('Rscript')


class PipelineRegression(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ['reproduce', 'fictional_inputs', 'r_outputs', MODEL,
                     'SYNTHETIC Supplier Evidence Demo.Report']:
            shutil.copytree(ROOT / name, self.root / name,
                            ignore=shutil.ignore_patterns('.pbi', '__pycache__'))
        (self.root / 'analysis_outputs').mkdir()
        self.tables = self.root / MODEL / 'definition/tables'

    def adapter(self):
        return subprocess.run([sys.executable, str(self.root / 'reproduce/refresh_snapshot.py')],
                              cwd=self.root, capture_output=True, text=True)

    def test_native_saved_identifiers_preserve_row_widths(self):
        for path in self.tables.glob('*.tmdl'):
            text = re.sub(r"(?m)^(\tcolumn) '([A-Za-z_][A-Za-z_0-9]*)'$",
                          r'\1 \2', path.read_text())
            path.write_text(text)
        result = self.adapter()
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in ['Labels', 'Evidence', 'Occurrences', 'Data Quality']:
            text = (self.tables / (name + '.tmdl')).read_text()
            match = re.search(r'Rows = #table\(\{([^\n]+)\}, \{\n(.*?)\n\t+\}\),', text, re.S)
            header = json.loads('[' + match[1] + ']')
            rows = json.loads('[' + match[2].replace('{', '[').replace('}', ']') + ']')
            self.assertTrue(all(len(row) == len(header) for row in rows), name)

    def test_late_invalid_model_leaves_all_files_unchanged(self):
        source = self.root / 'r_outputs/labels.csv'
        source.write_text(source.read_text().replace('"Reviewed"', '"Not reviewed"', 1))
        bad = self.tables / 'Data Quality.tmdl'
        bad.write_text(bad.read_text().replace('Rows = #table', 'Rows = #badtable'))
        before = {p: p.read_bytes() for p in self.tables.glob('*.tmdl')}
        result = self.adapter()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(before, {p: p.read_bytes() for p in before})
        self.assertFalse((self.root / 'analysis_outputs/r_model_snapshot.json').exists())

    def test_unknown_evidence_id_rejected_before_write(self):
        path = self.root / 'r_outputs/evidence.csv'
        path.write_text(path.read_text().replace('"FA"', '"ORPHAN"', 1))
        before = {p: p.read_bytes() for p in self.tables.glob('*.tmdl')}
        result = self.adapter()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(before, {p: p.read_bytes() for p in before})

    def test_replace_failure_rolls_back_completed_files(self):
        spec = importlib.util.spec_from_file_location('snapshot', self.root / 'reproduce/refresh_snapshot.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        paths = [self.root / name for name in ['first.txt', 'second.txt', 'receipt.json']]
        paths[0].write_bytes(b'original first')
        paths[1].write_bytes(b'original second')
        replace = os.replace
        count = 0

        def fail_once(source, target):
            nonlocal count
            count += 1
            if count == 3:
                raise OSError('Simulated interrupted replacement')
            return replace(source, target)

        with patch.object(module.os, 'replace', side_effect=fail_once):
            with self.assertRaises(OSError):
                module.replace_validated_files(dict.fromkeys(paths, b'changed'))
        self.assertEqual(paths[0].read_bytes(), b'original first')
        self.assertEqual(paths[1].read_bytes(), b'original second')
        self.assertFalse(paths[2].exists())

    def test_changed_fact_value_is_checked_against_R(self):
        path = self.tables / 'Evidence.tmdl'
        path.write_text(path.read_text().replace('2.4', '9.9'))
        result = subprocess.run([sys.executable, str(self.root / 'reproduce/test_analysis.py')],
                                cwd=self.root, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)

    @unittest.skipUnless(RSCRIPT, 'Set RSCRIPT or put Rscript on PATH for R input guards.')
    def test_R_rejects_invalid_inputs_without_outputs(self):
        for case in ['missing_year', 'unknown_id', 'duplicate_review']:
            with self.subTest(case=case):
                inputs = self.root / 'fictional_inputs'
                for path in (ROOT / 'fictional_inputs').glob('*.csv'):
                    shutil.copy2(path, inputs / path.name)
                path = inputs / ('review_decisions.csv' if case == 'duplicate_review'
                                 else 'evidence_rows.csv')
                with path.open(newline='', encoding='utf-8-sig') as stream:
                    reader = csv.DictReader(stream)
                    fields, rows = reader.fieldnames, list(reader)
                if case == 'duplicate_review':
                    rows.append(rows[0].copy())
                else:
                    rows[0]['Year' if case == 'missing_year' else 'LabelID'] = (
                        '' if case == 'missing_year' else 'ORPHAN')
                with path.open('w', newline='', encoding='utf-8') as stream:
                    writer = csv.DictWriter(stream, fieldnames=fields)
                    writer.writeheader()
                    writer.writerows(rows)
                target = self.root / ('invalid_' + case)
                result = subprocess.run([RSCRIPT, '--vanilla', str(self.root / 'reproduce/analyse.R'),
                                         str(self.root), str(target)], capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(list(target.glob('*.csv')))


if __name__ == '__main__':
    unittest.main(verbosity=2)
