# Validation - fictional build ISM-FICTIONAL-v3

Read ACCEPTANCE_MATRIX.md for item-level status and MANIFEST_SHA256.json for the final delivered file hashes. This record supersedes the v2 validation for the fictional release only.

## Fixes and execution

The native-save failure was reproduced before patching. The previous adapter read only quoted column names and partially changed other tables before failing. The corrected adapter reads the ordered M table header, checks header/declaration/source agreement for every table, stages all outputs before replacing any, and rolls back completed replacements after an ordinary replacement error. No all-files transaction against sudden power loss is claimed.

R 4.6.1 regenerated all thirteen metrics. The seven analytical tests and six pipeline regressions pass with no skipped tests when RSCRIPT points to the installed R executable. Invalid reporting years, unknown claim IDs and duplicate review decisions are rejected before output. Full keyed claim and occurrence records are compared, including metric values, units, scope and year. The intentional fixture result remains 8 labels, 6 reviewed, 2 usable and 6 follow-ups.

Power BI Desktop **2.155.756.0** opened and refreshed the updated five-table project. It was saved natively; the actual saved model was processed with the corrected adapter; the project was closed, reopened and refreshed successfully at **2026-11-17 19:30:09 UTC**. It had initially refreshed at 19:22:14 UTC. The final native report state was saved after the controls were restored to all technologies and Workshop A. Model/report definition-tree SHA-256: **64ba18fd18876f8d3cece8822c09e069b70f9850b348ae296b802472d35a794d**.

The saved DAX query executed successfully in Desktop (336.0 ms): baseline, Machining, Finishing, no eligible labels and A+H match the expected results. The separate fictional filter example executed as eligible 2 / global reviewed 6 / wrong coverage 3 / selected reviewed 2 / corrected coverage 1. The deliberately wrong expression is confined to an explanatory query; it is not a report measure.

Technology selection/reset, all eight supplier profiles, page navigation and Ctrl/Shift strict single selection were checked in the current build. Native accessibility text was intermittently unavailable; profile screenshots were inspected directly rather than treating failed automated string matches as passes. The source tables show both A periods, C's unresolved identity, E's missing unit and F's empty claim set. The previous unchanged overview row-cross-filter test is retained as prior evidence rather than described as a fresh v3 click test.

The report uses reporting years **2023-2025**, a separate fictional snapshot date and a genuine UTC refresh/build footer. RefreshInfo is disconnected from analytical populations. Real Desktop export produced the three report pages. Some PDF renderers omitted repeated native text; the distributed preview normalises the Poppler-rendered native page bodies, retains searchable native text and prints the observed UTC footer consistently. The original native export is retained privately as execution evidence. No source values were changed by that formatting step.

The revised PowerPoint has thirteen slides, two actual fictional report images and slide-specific notes. It adds a four-stage chronology, worked filter-context correction, technical repair explanation and version-specific walkthrough. Structural, geometry, reference-font and artifact-import checks passed with zero findings; the finalizer completed successfully. Every full-size slide was visually inspected. The searchable thirteen-page PDF uses those exact slide renders, and extracted PPTX/PDF text agrees on all thirteen pages. The named user remains responsible for confirming original contribution and demonstrating understanding.

## Reproducible checks

From the package folder, with Rscript available:

```text
Rscript --vanilla reproduce/analyse.R . r_outputs
python reproduce/refresh_snapshot.py r_outputs
python -m unittest discover -s reproduce -p test_*.py
```

Close Desktop before regeneration; reopen and Refresh afterwards. If Rscript is not on PATH, set RSCRIPT to its executable for the R guard test. The current run set it to the installed R 4.6.1 executable. Existing Ruff checked the public Python scripts with `--select F,E9`; all checks passed. R emitted startup locale warnings; assertions and outputs passed. No dependencies were installed.

## Privacy and remaining boundaries

Only authored fictional inputs, derived outputs, report/model definitions and selected portfolio files enter this release. Original workbooks, original PBIX, private source lists/screenshots, model caches, .platform metadata and older archives are excluded. Public privacy/hash receipts are generated after final assembly. This is a bounded provenance, string, Office XML, PDF metadata and visual review, not a claim that every possible sensitive string can be detected.

No cloud Power BI deployment, spoken screen-reader audit, WCAG certification or native PowerPoint edit/save roundtrip was performed. These are not implied by keyboard, import or rendering checks. Original 341/345/340 catalog reconciliation, original email-date authentication and student rehearsal remain separately unresolved. The original private repository is not made public or copied wholesale.
