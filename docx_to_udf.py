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

    # Check for tables and raise error if any are found
    if document.tables:
        print("Error: Tables are not supported in the UDF conversion process.")
        return

    content = []
    elements = []
    current_offset = 0
    EMPTY_PARAGRAPH_PLACEHOLDER = '\u200B'  # Zero-width space

    for paragraph in document.paragraphs:
        para_text = ""
        para_elements = []
        for run in paragraph.runs:
            # Process images in the run
            drawing_elements = run._element.findall('.//' + qn('w:drawing'))
            if drawing_elements:
                for drawing in drawing_elements:
                    blip = drawing.find('.//' + qn('a:blip'))
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

            # Process text in the run
            text = run.text
            if text:
                length = len(text)
                style_attrs = []

                if run.bold:
                    style_attrs.append('bold="true"')
                if run.italic:
                    style_attrs.append('italic="true"')
                if run.font.size:
                    # Convert to point size
                    size = run.font.size.pt
                    style_attrs.append(f'size="{size}"')
                if run.font.name:
                    style_attrs.append(f'family="{run.font.name}"')
                if run.font.color and run.font.color.rgb:
                    color = run.font.color.rgb
                    style_attrs.append(f'foreground="#{color}"')

                style_attr_str = ' '.join(style_attrs)
                para_elements.append(
                    f'<content startOffset="{current_offset}" length="{length}" {style_attr_str} />'
                )
                para_text += text
                current_offset += length

        # If paragraph is empty, add placeholder
        if not para_text:
            para_text = EMPTY_PARAGRAPH_PLACEHOLDER
            para_elements.append(f'<content startOffset="{current_offset}" length="1" />')
            current_offset += 1

        alignment = paragraph.alignment
        if alignment == WD_ALIGN_PARAGRAPH.CENTER:
            alignment_val = '1'
        elif alignment == WD_ALIGN_PARAGRAPH.RIGHT:
            alignment_val = '2'
        elif alignment == WD_ALIGN_PARAGRAPH.JUSTIFY:
            alignment_val = '3'
        else:
            alignment_val = '0'  # Default to Left

        left_indent = paragraph.paragraph_format.left_indent
        right_indent = paragraph.paragraph_format.right_indent
        indent_attrs = f'LeftIndent="{left_indent.pt if left_indent else 0.0}" RightIndent="{right_indent.pt if right_indent else 0.0}"'

        elements.append(
            f'<paragraph Alignment="{alignment_val}" {indent_attrs}>{"".join(para_elements)}</paragraph>'
        )
        content.append(para_text)

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