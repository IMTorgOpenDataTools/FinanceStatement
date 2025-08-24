#!/usr/bin/env python3
"""
Entrypoint for creating instance document file

"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "AGPL-3.0"



# Get context info
def get_context_info(s_context_ref):
    """
    Get context info from the worksheet based on the given context reference.

    Args:
        s_context_ref (str): The context reference to search for.

    Returns:
        str: The context info as a string.
    """
    context_info = ""
    for row in worksheet.iter_rows(min_row=1, values_only=True):
        if row[0] == s_context_ref:
            context_info += f"Context ID: {row[0]}\n"
            context_info += f"Entity Scheme: {row[2]}\n"
            context_info += f"Entity ID: {row[1]}\n"
            if row[3] == "Instant":
                context_info += f"Period: [As of] {row[5]}\n"
            elif row[3] == "Duration":
                context_info += f"Period: [For Period] {row[4]} to {row[5]}\n"
            context_info += f"Period: {row[3]}\n"
            context_info += "\n"
            break
    return context_info

# Get dimensions info
def get_dimensions_info(s_context_ref):
    """
    Get dimensions info from the worksheet based on the given context reference.

    Args:
        s_context_ref (str): The context reference to search for.

    Returns:
        str: The dimensions info as a string.
    """
    dimensions_info = ""
    for row in worksheet.iter_rows(min_row=1, values_only=True):
        if row[0] == s_context_ref:
            dimensions_info += "\n"
            dimensions_info += f"Dimension: {row[2]}\n"
            dimensions_info += f"Member: {row[3]}\n"
    return dimensions_info

# Example usage
if __name__ == "__main__":
    file_path = "example.xbrl"  # Replace with your file path
    s_context_ref = "example_context_ref"  # Replace with your xbrl context reference

    lines = []
    context_info_lines = get_context_info(s_context_ref)
    dimensions_info_lines = get_dimensions_info(s_context_ref)
    lines.extend(context_info_lines)
    lines.extend(dimensions_info_lines)

    with open(file_path, 'w') as f:
        f.writelines(lines)



    print('complete')