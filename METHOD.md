# Fictional metric and decision contract

Scenario version 2, rebuilt 17 November 2026. Research-as-of 1 December 2025. Authored inputs only.

## Grain and cleaning

Supplier cells retain source_row. Trim whitespace. Exclude exactly the placeholders empty, 0 and Unknown. Map this fixture's A-H labels explicitly; no fuzzy legal-entity matching. Repeated labels are retained as separate source occurrences. Labels uses one row per stable FA-FH ID. A display alias such as Workshop A does not change its raw label in the occurrence ledger.

Evidence has one row per unique entire input claim row. Remove only exact duplicate rows. A changed value or ID remains a separate claim and would need review; do not use this policy to conceal conflicting disclosures. SIM IDs denote authored sources with no external URLs.

## Evidence rule

The decision is intended for a site-level review. Check branches in order: not reviewed -> Unreviewed; unresolved identity -> Identity unresolved; scope other than Site -> Scope mismatch; absent unit -> Missing unit; year after 2025 -> After cutoff; year before 2023 -> Historical period; otherwise Usable example. The rule's three-year window and priority order are scenario assumptions, not an external standard. A Usable example means complete for this exercise, not audited truth or verified certification.

The pre-authored fields only use reporting year; exact publication dates are not supplied. The cutoff therefore operates at reporting-year granularity. No exact historical publication-eligibility claim is made.

## Label-level decision

A label has usable evidence if any of its claims passes the rule. Its priority reason is the highest-severity claim reason, even if another claim is usable. Thus usable-evidence coverage and follow-up coverage are different measures and need not be complements in a changed scenario. In this fixture they partition 2 and 6.

P1: Identity unresolved, Scope mismatch. P2: Historical period, After cutoff, Missing unit, Unreviewed, No evidence. P3: Usable example. Ties within a priority are equally urgent; no supplier-performance score is calculated. Store a plain-English next action for every reason. An empty claim set is No evidence.

## Measures and filters

Candidate Labels: COUNTROWS on the unique label table in current filter context. Reviewed Labels: reviewed subset with KEEPFILTERS and zero-safe return. Review Coverage %: reviewed / eligible, DIVIDE with blank for empty denominator. Usable Labels: subset with Usable=1. Follow Up Labels: subset with Priority different from P3. Usable Coverage %: usable / eligible. Occurrence Rows and Claim Rows count their respective facts.

Technology sits on Labels, with Labels -> Evidence and Labels -> Occurrences single-direction relationships. Overview slicer and selected table rows affect its cards. Supplier Evidence uses a strict single-select slicer and filters all profile/source/claim tables on that page. The two page slicers are not synchronised. Data Quality is the fixed full-fixture reconciliation; it is deliberately disconnected from label filters. No chart, drillthrough or custom tooltip page exists in this build.

## Comparability

Compare observations only when label, metric, unit and scope align. A's 2023 and 2024 Energy use observations are both Site/MWh: change=-20%. B is Group/kWh per unit and cannot join that calculation. The fictional figures do not establish causal energy savings.
