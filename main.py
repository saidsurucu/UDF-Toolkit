import zipfile
from docx import Document
from paragraph_processor import process_paragraph
from table_processor import process_table

def main(docx_file, udf_file):
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

    for element in document.element.body:
        if element.tag.endswith('p'):  # Paragraph
            para_text, para_elements = process_paragraph(element, document, current_offset)
            elements.append(para_elements)
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
