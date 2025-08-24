#!/usr/bin/env python3
"""
Test template (default) workflow



Please note that you'll need to replace `'your_file.xlsx'` with the actual path to your Excel file. Also, the `openpyxl` library is used for Excel file manipulation in Python. You can install it using `pip install openpyxl` if you haven't already.
"""
import openpyxl

def clear_audit_information():
    # Load the active workbook
    workbook = openpyxl.load_workbook('your_file.xlsx')  # Replace 'your_file.xlsx' with your actual file path
    active_sheet = workbook.active
    started_at_sheet = active_sheet.title

    # Disable screen updating (not applicable in Python, but included for reference)
    # Application.ScreenUpdating = False

    # Select the "Mapping" worksheet
    mapping_sheet = workbook['Mapping']

    # Start from cell A2
    current_cell = mapping_sheet['A2']

    empty_cell_count = 0

    while empty_cell_count < 100:
        if current_cell.value is None:
            # Cell is empty
            empty_cell_count += 1
        else:
            # Get values from the current row
            s_spreadsheet = current_cell.value
            s_cell = current_cell.offset(column=1).value

            # Clear comments from the specified cell
            target_sheet = workbook[s_spreadsheet]
            target_cell = target_sheet[s_cell]
            target_cell.comment = None

        # Move to the next row
        current_cell = current_cell.offset(row=1)

    # Save the workbook
    workbook.save('your_file.xlsx')  # Replace 'your_file.xlsx' with your actual file path

    # Re-enable screen updating (not applicable in Python, but included for reference)
    # Application.ScreenUpdating = True

# Call the function
clear_audit_information()