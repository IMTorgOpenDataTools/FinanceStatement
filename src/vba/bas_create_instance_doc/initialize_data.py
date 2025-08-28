#!/usr/bin/env python3
"""
Test template (default) workflow


This Python code uses the `openpyxl` library to interact 
with Excel workbooks. The `initialize_data` function takes 
the path to the workbook as an argument and performs the 
same operations as the original Visual Basic code. The 
function loads the workbook, processes the "Mapping" 
worksheet, and updates the target worksheets based on the 
mapping data. Finally, it saves the workbook.
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "AGPL-3.0"


import openpyxl
from openpyxl.utils import get_column_letter

def initialize_data(workbook_path):
    # Load the workbook
    wb = openpyxl.load_workbook(workbook_path)
    started_at_sheet = wb.active.title

    # Disable screen updating (not applicable in Python)
    # Application.ScreenUpdating = False

    # Select the "Mapping" worksheet
    ws_mapping = wb["Mapping"]

    empty_cell_count = 0
    current_row = 2  # Start from row 2

    while empty_cell_count < 100:
        # Get the cell in column A of the current row
        cell = ws_mapping[f"A{current_row}"]

        if cell.value is None:
            # Cell is empty
            empty_cell_count += 1
        else:
            # Get values from the current row
            s_spreadsheet = cell.value
            s_cell = ws_mapping[f"B{current_row}"].value
            s_concept = ws_mapping[f"C{current_row}"].value
            s_context_ref = ws_mapping[f"D{current_row}"].value
            s_unit_ref = ws_mapping[f"E{current_row}"].value
            s_decimals = ws_mapping[f"F{current_row}"].value

            # Tests to see if it is a start/stop tuple, if so, skips row in mapping table.
            if s_context_ref is not None and len(str(s_context_ref)) > 0:
                if s_unit_ref is not None and len(str(s_unit_ref)) > 0 and s_decimals is not None and len(str(s_decimals)) > 0:
                    # Has unit ref and decimals, therefore is Numeric
                    s_value = 0
                else:
                    # No unit ref or decimals, so string
                    s_value = "[enter text here]"

                # Set the value in the target worksheet and cell
                target_ws = wb[s_spreadsheet]
                target_ws[s_cell] = s_value

        current_row += 1

    # Select the original worksheet
    wb.active = wb[started_at_sheet]

    # Save the workbook
    wb.save(workbook_path)

# Example usage
# initialize_data("path_to_your_workbook.xlsx")