# Keyboard guide and verified scope

Tested in Power BI Desktop on 17 November 2026 with fictional records only.

## Move around

- Use Ctrl+F6 to move among application sections. Tab and Shift+Tab move forward and backward within a section.
- In the page-tab section, use arrows and Enter to open Overview, Supplier Explorer or Data Quality.
- Enter a selected visual with Ctrl+Right. Escape leaves the current layer. Desktop also has authoring controls; a text box may expose its editing toolbar.
- All report visuals have meaningful alternative descriptions exposed in the accessibility tree. Tab order follows the page layout, with the page heading before data.

## Supplier Explorer

The radio-button selector now enforces one supplier. The initial example is Alpha. Use Up/Down or Home/End to navigate, then Space or Enter to activate. Ctrl+Space and Shift+Space were tested and did not add a second selection. Shift+Down was also tested with single-selection retained. Alpha shows one claim; Beta and Gamma show their review reason and an empty evidence table.

The Explorer is a single-supplier profile. Use Overview for an all-label comparison. Do not expect Clear to produce a zero-selection Explorer state: the strict selector retains a supplier. This replaces the earlier draft's multi-select/clear instructions.

## Overview and tables

Arrow keys move among table cells. Ctrl+Home and Ctrl+End reach the table boundaries. With a data cell focused, Ctrl+Space toggles that row in the selection. Alpha plus Gamma gives 2 eligible labels, 1 reviewed and 50% coverage. Toggle selected rows off to restore 3 labels, 2 reviewed and 66.7% coverage. This reset was verified. Ctrl+Shift+C did not reliably reset the overview in this Desktop session; use the tested toggle method.

## Scope

Keyboard focus was visible. Page navigation, slicer activation, modifier combinations, table-cell movement and row-selection reset were tested. Native accessibility names were inspected. This is functional keyboard verification of this report, not a WCAG certification or a spoken screen-reader audit. Ctrl/Shift mouse-click combinations were not separately exercised; the corresponding keyboard selection commands were tested.

Reference: [Microsoft Power BI keyboard shortcuts](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-accessibility-keyboard-shortcuts).
