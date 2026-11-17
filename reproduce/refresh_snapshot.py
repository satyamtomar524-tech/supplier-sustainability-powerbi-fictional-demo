"""Regenerate fictional snapshots, including after a native Desktop Save.

Read ordered M table headers; validate all outputs before replacing any file.
Only Python's standard library is required.
"""
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / 'SYNTHETIC Supplier Evidence Demo.SemanticModel/definition/tables'
ACTIONS = {'Identity unresolved': 'Confirm the legal entity before attribution',
           'Scope mismatch': 'Request the site-level scope and denominator',
           'Historical period': 'Request a current-period disclosure',
           'After cutoff': 'Exclude until the applicable research cutoff',
           'Missing unit': 'Confirm the metric unit before interpretation',
           'Unreviewed': 'Review the example source and scope',
           'No evidence': 'Request a source and reporting period',
           'Usable example': 'Retain evidence and schedule a later review'}


def read(source, name):
    with (source / name).open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def mvalue(value):
    if isinstance(value, (int, float)):
        if not math.isfinite(value):
            raise ValueError('Non-finite numeric input')
        return str(value)
    return '"' + str(value).replace('#', '#(#)').replace('"', '""').replace(
        '\r', '#(cr)').replace('\n', '#(lf)').replace('\t', '#(tab)') + '"'


def render_table(text, rows, name):
    pattern = re.compile(r'(Rows\s*=\s*#table\(\{([^\n]+)\}, \{\n).*?(\n\s*\}\),)', re.S)
    match = pattern.search(text)
    if not match or not rows:
        raise ValueError(f'{name}: missing literal-table partition or empty rows')
    columns = re.findall(r'"((?:[^"]|"")*)"', match[2])
    columns = [c.replace('""', '"') for c in columns]
    declarations = re.findall(r"(?m)^\tcolumn (?:'((?:[^']|'')+)'|([^\s]+))\s*$", text)
    declared = [a.replace("''", "'") if a else b for a, b in declarations]
    if len(set(columns)) != len(columns) or set(columns) != set(declared):
        raise ValueError(f'{name}: table header and column declarations disagree')
    if any(set(row) != set(columns) for row in rows):
        raise ValueError(f'{name}: source fields do not match model header')
    body = ',\n'.join('\t\t\t\t{' + ', '.join(mvalue(row[c]) for c in columns) + '}'
                      for row in rows)
    return text[:match.start()] + match[1] + body + match[3] + text[match.end():]


def replace_validated_files(changes):
    """Stage a validated batch; replace atomically per file, rolling back on error."""
    originals = {p: p.read_bytes() if p.exists() else None for p in changes}
    staged, replaced = {}, []
    try:
        for path, content in changes.items():
            with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
                staged[path] = Path(stream.name)
                stream.write(content)
                stream.flush()
                os.fsync(stream.fileno())
        for path, temp in staged.items():
            os.replace(temp, path)
            replaced.append(path)
    except BaseException:
        for path in reversed(replaced):
            original = originals[path]
            if original is None:
                path.unlink(missing_ok=True)
            else:
                with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
                    rollback = Path(stream.name)
                    stream.write(original)
                os.replace(rollback, path)
        raise
    finally:
        for temp in staged.values():
            temp.unlink(missing_ok=True)


def main(source):
    raw_labels = read(source, 'labels.csv')
    ids = [r['LabelID'] for r in raw_labels]
    if not ids or len(ids) != len(set(ids)):
        raise ValueError('Label IDs must be unique and nonempty')
    labels = [{'LabelID': r['LabelID'], 'Supplier label': r['clean_label'].replace('Fictional ', ''),
               'Technology': r['technology'], 'Review': r['Review'], 'Identity': r['Identity'],
               'Usable': int(r['Usable'] == 'TRUE'), 'Priority': r['Priority'], 'Reason': r['Reason'],
               'Next action': ACTIONS[r['Reason']], 'As of': '2025-12-01'} for r in raw_labels]
    evidence = read(source, 'evidence.csv')
    for row in evidence:
        if row['LabelID'] not in ids:
            raise ValueError('Evidence refers to an unknown LabelID')
        row['Year'], row['Value'] = int(row['Year']), float(row['Value'])
        if not math.isfinite(row['Value']):
            raise ValueError('Evidence value must be finite')
        row['Reported value'] = f"{row['Value']:g} {row['Unit'] or '[unit missing]'}"
    by_label = {r['clean_label']: r['LabelID'] for r in raw_labels}
    occurrences = [{'LabelID': by_label[r['clean_label']], 'Source row': int(r['source_row']),
                    'Supplier label': r['clean_label'], 'Technology': r['technology']}
                   for r in read(source, 'occurrences.csv')]
    metrics = {r['Metric']: float(r['Value']) for r in read(source, 'metrics.csv')}
    dq = [{'Check': label, 'Value': int(metrics[key])} for label, key in [
        ('Raw supplier cells', 'raw_supplier_cells'), ('Excluded placeholders', 'excluded_placeholders'),
        ('Retained occurrences', 'occurrences'), ('Candidate labels', 'candidate_labels'),
        ('Raw evidence rows', 'raw_evidence_rows'), ('Exact duplicate removed', 'exact_evidence_duplicates'),
        ('Retained claims', 'evidence_claims')]]
    changes = {}
    for name, rows in [('Labels', labels), ('Evidence', evidence),
                       ('Occurrences', occurrences), ('Data Quality', dq)]:
        path = TABLES / (name + '.tmdl')
        changes[path] = render_table(path.read_text(encoding='utf-8'), rows, name).encode('utf-8')
    receipt = {'source': 'base-R output CSV files', 'research_as_of': '2025-12-01',
               'metrics': metrics, 'table_sha256': {
                   p.name: hashlib.sha256(changes.get(p, p.read_bytes())).hexdigest()
                   for p in TABLES.glob('*.tmdl')}}
    changes[ROOT / 'analysis_outputs/r_model_snapshot.json'] = json.dumps(receipt, indent=2).encode()
    replace_validated_files(changes)
    print('Validated snapshot regenerated. Reopen the PBIP and Refresh.')


if __name__ == '__main__':
    main(ROOT / (sys.argv[1] if len(sys.argv) > 1 else 'r_outputs'))
