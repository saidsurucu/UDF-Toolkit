import sys
import os
import zipfile
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH

def docx_to_udf(docx_file, udf_file):
    udf_template = '''<?xml version="1.0" encoding="UTF-8" ?>
<template format_id="1.8">
    <content><![CDATA[{content}]]></content>
    <properties>
        <pageFormat mediaSizeName="1" leftMargin="70.875" rightMargin="70.875" topMargin="70.875" bottomMargin="70.875" paperOrientation="1" headerFOffset="20.0" footerFOffset="20.0" />
    </properties>
    <elements resolver="hvl-default">
        {elements}
    </elements>
    <styles>
        <style name="default" description="Geçerli" family="Dialog" size="12" bold="false" italic="false" underline="false" strikethrough="false" foreground="-13421773" FONT_ATTRIBUTE_KEY="javax.swing.plaf.FontUIResource[family=Dialog,name=Dialog,style=plain,size=12]" />
        <style name="hvl-default" family="Times New Roman" size="12" description="Gövde" />
    </styles>
</template>'''

    try:
        # Load DOCX file
        document = Document(docx_file)
    except Exception as e:
        print(f"Error loading DOCX file: {e}")
        return

    # Check for tables and raise error if any are found
    if document.tables:
        print("Error: Tables are not supported in the UDF conversion process.")
        return

    content = []
    elements = []
    current_offset = 0

    def process_paragraph(paragraph):
        nonlocal current_offset
        para_text = ""
        para_elements = []

        for run in paragraph.runs:
            text = run.text
            if text:
                length = len(text)
                style_attrs = []

                if run.bold:
                    style_attrs.append('bold="true"')
                if run.italic:
                    style_attrs.append('italic="true"')
                if run.underline:
                    style_attrs.append('underline="true"')
                if run.font.strike:
                    style_attrs.append('strikethrough="true"')
                if run.font.size:
                    style_attrs.append(f'size="{int(run.font.size.pt)}"')
                if run.font.name:
                    style_attrs.append(f'family="{run.font.name}"')
                if run.font.color and run.font.color.rgb:
                    color = run.font.color.rgb
                    style_attrs.append(f'foreground="#{color}"')

                style_attr_str = ' '.join(style_attrs)
                para_elements.append(f'<content startOffset="{current_offset}" length="{length}" {style_attr_str} />')
                para_text += text
                current_offset += length

        if para_text:
            alignment = paragraph.alignment
            if alignment == WD_ALIGN_PARAGRAPH.CENTER:
                alignment_val = '1'
            elif alignment == WD_ALIGN_PARAGRAPH.RIGHT:
                alignment_val = '2'
            elif alignment == WD_ALIGN_PARAGRAPH.JUSTIFY:
                alignment_val = '3'
            else:
                alignment_val = '0'  # Default to Left

            elements.append(f'<paragraph Alignment="{alignment_val}">{"".join(para_elements)}</paragraph>')
            content.append(para_text)
            current_offset += 1  # For newline

    # Process paragraphs
    for para in document.paragraphs:
        process_paragraph(para)

    udf_content = udf_template.format(
        content='\n'.join(content).strip(),
        elements=''.join(elements)
    )

    # Save UDF content as content.xml inside a zip archive
    try:
        with zipfile.ZipFile(udf_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.writestr('content.xml', udf_content)
        print(f"UDF file created successfully: {udf_file}")
    except Exception as e:
        print(f"Error creating UDF file: {e}")

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
