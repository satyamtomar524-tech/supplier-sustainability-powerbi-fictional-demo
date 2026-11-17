# Validation record - 17 November 2026

## Verified for this fictional rebuild

- Base R 4.6.1 independently derives all 13 expected metrics and checks priority membership and edge rules. Locale warnings occurred; assertions passed. No dependencies were installed.
- `python reproduce/test_analysis.py`: all 7 contract tests passed, including raw-to-clean totals, priority membership, technology populations, duplicate-grain protection, metric scope/unit, R-to-model agreement and visual/tab-order definitions.
- Existing Ruff ran with `--select F,E9` on the public Python scripts: passed. This is a bounded error check, not a full style audit.
- Generated model partitions matched the independently derived R output and the substantive Desktop-tested snapshot. Four tables, two single-direction relationships, eight explicit measures.
- Power BI Desktop opened and refreshed the substantive report. DAX Query View executed all five cases in `reproduce/desktop_checks.dax`: baseline 8/6/2/6/75%; Machining 2/2/1/1/100%; Finishing 2/1/0/2/50%; empty blank/0/0/0/blank; A+H 2/1/1/1/50% (candidate/reviewed/usable/follow-up/coverage).
- Ordinary technology selection and clear/reset worked. All eight single-workshop profiles were inspected against source, review reason and next action. Workshop F correctly has no claim rows. A has two periods; E visibly marks its missing unit.
- Supplier slicer strict single-selection was tested with Ctrl+Space and Shift+Down/Shift+Space. Home/Enter returned to A. Keyboard entry/exit and page navigation were exercised. Descriptive visual alternatives and heading-first tab order are present.
- Final layout reopened and refreshed: Labels 8, Evidence 8, Occurrences 10, Data Quality 7. The enlarged source table shows both A source rows without clipping. Headings and all eight slicer labels fit. Native Desktop export produced three pages.
- Ten-slide PPTX: package-integrity and geometry validators returned zero findings. All ten rendered slides were visually inspected. The ten-page PDF was built from those slide renders; every slide's extracted text matches its PDF page after whitespace normalization. PPTX has no embedded workbook.
- The old academic GitHub repository was checked through the authenticated GitHub connector and returned `private: true`. It was not made public or edited.

## Privacy and limits

The distributable is assembled without `.pbi`, `.platform`, binary model caches, originals, original Excel/PBIX, old ZIPs or private research records. Fixture rows are authored examples, not anonymised internal records. Text and Office XML are checked against internal supplier labels of at least six characters and private path/credential markers; the three report exports and ten slides were also visually inspected. File hashes and archive equality are recorded separately. This is a bounded content/provenance review, not proof that every possible sensitive string is detectable.

Power BI Desktop initially exhausted available memory with old test copies open; the final named copy subsequently loaded, refreshed, saved and exported successfully. No private source report was changed for this rebuild.

No Power BI Service deployment, spoken screen-reader audit, WCAG certification or independent environmental verification was performed. The presentation was structurally validated and rendered locally; native PowerPoint editing was not tested. The presentation finalizer passed its checks but its final Windows hard-link publication step failed with EPERM; the checked draft was copied byte-for-byte to the final PPTX. The optional artifact-operation marker helper was absent in the installed skill folders.

Original academic counts, date provenance and unresolved legacy reconciliation are documented as historical/reported evidence in CASE_STUDY.md. This fictional validation does not resolve those private academic questions or establish Satyam's independent mastery. Interview rehearsal requires the student's participation.
