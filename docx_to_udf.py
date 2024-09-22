import sys
import os
import zipfile
import base64
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

def docx_to_udf(docx_file, udf_file):
    udf_template = '''<?xml version="1.0" encoding="UTF-8" ?>
<template format_id="1.8">
<content><![CDATA[{content}]]></content>
<properties><pageFormat mediaSizeName="1" leftMargin="42.51968479156494" rightMargin="28.34645652770996" topMargin="14.17322826385498" bottomMargin="14.17322826385498" paperOrientation="1" headerFOffset="20.0" footerFOffset="20.0" /></properties>
<elements resolver="hvl-default">
{elements}
</elements>
<styles><style name="default" description="Geçerli" family="Dialog" size="12" bold="false" italic="false" foreground="-13421773" FONT_ATTRIBUTE_KEY="javax.swing.plaf.FontUIResource[family=Dialog,name=Dialog,style=plain,size=12]" /><style name="hvl-default" family="Times New Roman" size="12" description="Gövde" /></styles>
</template>'''

    try:
        document = Document(docx_file)
    except Exception as e:
        print(f"Error loading DOCX file: {e}")
        return

    content = []
    elements = []
    current_offset = 0
    EMPTY_PARAGRAPH_PLACEHOLDER = '\u200B'  # Zero-width space
    TAB_CHARACTER = '\t'  # Tab character

    for element in document.element.body:
        if element.tag.endswith('p'):  # Paragraph
            para_text, para_elements = process_paragraph(element, document, current_offset)
            elements.append(
                f'<paragraph Alignment="{get_alignment(element)}" {get_indent_attrs(element)}>{"".join(para_elements)}</paragraph>'
            )
            content.append(para_text)
            current_offset += len(para_text)

        elif element.tag.endswith('tbl'):  # Table
            table_text, table_element = process_table(element, document, current_offset)
            elements.append(table_element)
            content.append(table_text)
            current_offset += len(table_text)

    # Ensure there's at least one paragraph after the table
    if not content:
        content.append(EMPTY_PARAGRAPH_PLACEHOLDER)
        elements.append(f'<paragraph Alignment="0" LeftIndent="0.0" RightIndent="0.0"><content startOffset="{current_offset}" length="1" /></paragraph>')

    udf_content = udf_template.format(
        content=''.join(content),
        elements='\n'.join(elements)
    )

    try:
        with zipfile.ZipFile(udf_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.writestr('content.xml', udf_content)
        print(f"UDF file created successfully: {udf_file}")
    except Exception as e:
        print(f"Error creating UDF file: {e}")

def process_paragraph(paragraph, document, current_offset):
    EMPTY_PARAGRAPH_PLACEHOLDER = '\u200B'  # Zero-width space
    TAB_CHARACTER = '\t'  # Tab character
    
    para_text = ""
    para_elements = []
    for run in paragraph.findall('.//w:r', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}):
        # Process images in the run
        drawing_elements = run.findall('.//w:drawing', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
        if drawing_elements:
            for drawing in drawing_elements:
                blip = drawing.find('.//a:blip', namespaces={'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'})
                if blip is not None:
                    blip_embed = blip.get(qn('r:embed'))
                    image_part = document.part.related_parts[blip_embed]
                    image_data = image_part.blob
                    image_base64 = base64.b64encode(image_data).decode('utf-8')

                    # Insert a placeholder character in content
                    placeholder = '\uFFFC'  # Object Replacement Character
                    para_text += placeholder

                    # Add image element
                    para_elements.append(
                        f'<image family="Times New Roman" size="10" imageData="{image_base64}" startOffset="{current_offset}" length="1" />'
                    )

                    current_offset += 1

        # Process text and tab characters in the run
        text = run.findtext('.//w:t', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}) or ''
        if text or run.find('.//w:tab', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}) is not None:
            # Get font properties
            font_family = run.findtext('.//w:rFonts[@w:ascii]', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}) or "Times New Roman"
            font_size = run.findtext('.//w:sz', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}) or "20"
            font_size = str(int(font_size) // 2)  # Convert half-points to points

            style_attrs = [f'family="{font_family}"', f'size="{font_size}"']
            if run.find('.//w:b', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}) is not None:
                style_attrs.append('bold="true"')
            if run.find('.//w:i', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}) is not None:
                style_attrs.append('italic="true"')

            style_attr_str = ' '.join(style_attrs)

            # Process text and tab characters
            for child in run:
                if child.tag.endswith('}t'):  # Text
                    para_elements.append(f'<content startOffset="{current_offset}" length="{len(child.text)}" {style_attr_str} />')
                    para_text += child.text
                    current_offset += len(child.text)
                elif child.tag.endswith('}tab'):  # Tab
                    para_elements.append(f'<tab family="{font_family}" size="{font_size}" startOffset="{current_offset}" length="1" />')
                    para_text += TAB_CHARACTER
                    current_offset += 1

    # If paragraph is empty, add placeholder
    if not para_text:
        para_text = EMPTY_PARAGRAPH_PLACEHOLDER
        para_elements.append(f'<content startOffset="{current_offset}" length="1" family="Times New Roman" size="10" />')
        current_offset += 1

    return para_text, para_elements

def process_table(table, document, current_offset):
    table_text = ""
    rows = []
    column_count = len(table.findall('.//w:gridCol', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}))
    column_spans = ",".join(["100"] * column_count)  # Assuming equal column widths

    for row_index, row in enumerate(table.findall('.//w:tr', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})):
        cells = []
        for cell in row.findall('.//w:tc', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}):
            cell_text, cell_elements = process_cell(cell, document, current_offset)
            cells.append(f'<cell><paragraph Alignment="0" LeftIndent="3.0" RightIndent="1.0">{"".join(cell_elements)}</paragraph></cell>')
            table_text += cell_text
            current_offset += len(cell_text)

        rows.append(f'<row rowName="row{row_index + 1}" rowType="dataRow">{"".join(cells)}</row>')

    table_element = f'<table tableName="Sabit" columnCount="{column_count}" columnSpans="{column_spans}" border="borderCell">{"".join(rows)}</table>'
    return table_text, table_element

def process_cell(cell, document, current_offset):
    cell_text = ""
    cell_elements = []
    for paragraph in cell.findall('.//w:p', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}):
        para_text, para_elements = process_paragraph(paragraph, document, current_offset)
        cell_text += para_text
        cell_elements.extend(para_elements)
        current_offset += len(para_text)

    # If cell is empty, add a space character
    if not cell_text:
        cell_text = " "
        cell_elements.append(f'<content startOffset="{current_offset}" length="1" family="Times New Roman" size="10" />')
        current_offset += 1

    return cell_text, cell_elements

def get_alignment(paragraph):
    alignment = paragraph.find('.//w:jc', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
    if alignment is not None:
        val = alignment.get(qn('w:val'))
        if val == 'center':
            return '1'
        elif val == 'right':
            return '2'
        elif val == 'both':
            return '3'
    return '0'  # Default to Left

def get_indent_attrs(paragraph):
    ind = paragraph.find('.//w:ind', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
    left = ind.get(qn('w:left')) if ind is not None else None
    right = ind.get(qn('w:right')) if ind is not None else None
    firstLine = ind.get(qn('w:firstLine')) if ind is not None else None
    
    indent_attrs = f'LeftIndent="{float(left) / 20 if left else 0.0}" RightIndent="{float(right) / 20 if right else 0.0}"'
    
    if firstLine:
        indent_attrs += f' FirstLineIndent="{float(firstLine) / 20}"'
    
    return indent_attrs

def main():
    if len(sys.argv) < 2:
        print("Usage: python docx_to_udf.py input.docx")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.isfile(input_file):
        print(f"Input file not found: {input_file}")
        sys.exit(1)

    filename, ext = os.path.splitext(input_file)

    if ext.lower() == '.docx':
        udf_file = filename + '.udf'
        docx_to_udf(input_file, udf_file)
    else:
        print("Please provide a .docx file.")
        sys.exit(1)

if __name__ == '__main__':
    main()