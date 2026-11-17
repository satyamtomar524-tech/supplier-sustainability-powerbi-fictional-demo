"""Update the portable model snapshot from base-R outputs. Python standard library only.
Run after analyse.R, from the package root: python reproduce/refresh_snapshot.py r_outputs
"""
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / (sys.argv[1] if len(sys.argv)>1 else 'r_outputs')
TABLES = ROOT / 'SYNTHETIC Supplier Evidence Demo.SemanticModel/definition/tables'


def read(name):
    with (SOURCE/name).open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


actions = {'Identity unresolved':'Confirm the legal entity before attribution',
           'Scope mismatch':'Request the site-level scope and denominator',
           'Historical period':'Request a current-period disclosure',
           'After cutoff':'Exclude until the applicable research cutoff',
           'Missing unit':'Confirm the metric unit before interpretation',
           'Unreviewed':'Review the example source and scope',
           'No evidence':'Request a source and reporting period',
           'Usable example':'Retain evidence and schedule a later review'}
labels = [{'LabelID':r['LabelID'],'Supplier label':r['clean_label'].replace('Fictional ',''),
           'Technology':r['technology'],'Review':r['Review'],'Identity':r['Identity'],
           'Usable':int(r['Usable']=='TRUE'),'Priority':r['Priority'],'Reason':r['Reason'],
           'Next action':actions[r['Reason']],'As of':'2025-12-01'} for r in read('labels.csv')]
evidence=[]
for r in read('evidence.csv'):
    r['Year']=int(r['Year']);r['Value']=float(r['Value'])
    r['Reported value']=f"{r['Value']:g} {r['Unit'] or '[unit missing]'}"
    evidence.append(r)
occurrences=[{'LabelID':'F'+r['clean_label'][-1], 'Source row':int(r['source_row']),
              'Supplier label':r['clean_label'],'Technology':r['technology']} for r in read('occurrences.csv')]
metrics={r['Metric']:float(r['Value']) for r in read('metrics.csv')}
dq=[{'Check':label,'Value':int(metrics[key])} for label,key in [
    ('Raw supplier cells','raw_supplier_cells'),('Excluded placeholders','excluded_placeholders'),
    ('Retained occurrences','occurrences'),('Candidate labels','candidate_labels'),
    ('Raw evidence rows','raw_evidence_rows'),('Exact duplicate removed','exact_evidence_duplicates'),
    ('Retained claims','evidence_claims')]]


def mvalue(value):
    return str(value) if isinstance(value,(int,float)) else '"'+str(value).replace('"','""')+'"'


for name,rows in [('Labels',labels),('Evidence',evidence),('Occurrences',occurrences),('Data Quality',dq)]:
    path=TABLES/(name+'.tmdl')
    text=path.read_text(encoding='utf-8')
    columns=re.findall(r"^\tcolumn '([^']+)'",text,re.M)
    assert columns and rows
    body=',\n'.join('\t\t\t\t{'+', '.join(mvalue(r[c]) for c in columns)+'}' for r in rows)
    pattern=r'(Rows = #table\(\{[^\n]+\}, \{\n).*?(\n\t+\}\),)'
    updated,count=re.subn(pattern,lambda m:m[1]+body+m[2],text,flags=re.S)
    assert count==1,name
    path.write_text(updated,encoding='utf-8')
receipt={'source':'base-R output CSV files','research_as_of':'2025-12-01',
         'metrics':metrics,'table_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in TABLES.glob('*.tmdl')}}
(ROOT/'analysis_outputs/r_model_snapshot.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
print('Portable Power BI snapshot regenerated from base-R outputs. Reopen PBIP and Refresh.')
