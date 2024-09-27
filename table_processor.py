from docx.oxml.ns import qn
from paragraph_processor import process_paragraph

def process_table(table, document, current_offset):
    table_text = ""
    rows = []
    grid_cols = table.findall('.//w:gridCol', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
    column_count = len(grid_cols)
    
    # Calculate column widths
    total_width = sum(int(col.get(qn('w:w'), '0')) for col in grid_cols)
    column_widths = [int(col.get(qn('w:w'), '0')) for col in grid_cols]
    column_spans = ",".join([str(int((width / total_width) * 300)) for width in column_widths])  # Scale to 300

    # Check table borders
    tblBorders = table.find('.//w:tblBorders', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
    border_type = "borderCell"  # Default to visible borders
    if tblBorders is not None:
        border_elements = ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']
        all_borders_none = all(
            tblBorders.find(f'.//w:{border}', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}) is None or
            tblBorders.find(f'.//w:{border}', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}).get(qn('w:val')) in ['none', 'nil', '0']
            for border in border_elements
        )
        if all_borders_none:
            border_type = "borderNone"
    else:
        # If tblBorders is not defined, assume borderless table
        border_type = "borderNone"

    for row_index, row in enumerate(table.findall('.//w:tr', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})):
        cells = []
        for cell in row.findall('.//w:tc', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}):
            cell_text, cell_elements = process_cell(cell, document, current_offset)
            cells.append(f'<cell>{"".join(cell_elements)}</cell>')
            table_text += cell_text
            current_offset += len(cell_text)

        rows.append(f'<row rowName="row{row_index + 1}" rowType="dataRow">{"".join(cells)}</row>')

    table_element = f'<table tableName="Sabit" columnCount="{column_count}" columnSpans="{column_spans}" border="{border_type}">{"".join(rows)}</table>'
    return table_text, table_element


def process_cell(cell, document, current_offset):
    cell_text = ""
    cell_elements = []
    paragraphs = cell.findall('.//w:p', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
    
    for i, paragraph in enumerate(paragraphs):
        para_text, para_elements = process_paragraph(paragraph, document, current_offset)
        cell_text += para_text
        cell_elements.extend(para_elements)
        current_offset += len(para_text)
        
        # Add a line break between paragraphs, but not after the last paragraph
        if i < len(paragraphs) - 1 and para_text.strip():
            cell_text += '\n'
            cell_elements.append(f'<content startOffset="{current_offset}" length="1" family="Times New Roman" size="10" />')
            current_offset += 1

    # If cell is empty, add a space character
    if not cell_text:
        cell_text = " "
        cell_elements.append(f'<content startOffset="{current_offset}" length="1" family="Times New Roman" size="10" />')
        current_offset += 1

    return cell_text, cell_elements
