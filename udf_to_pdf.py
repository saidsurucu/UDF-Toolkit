import sys
import os
import xml.etree.ElementTree as ET
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.units import mm
import base64
import io
import zipfile
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Add a font that supports Turkish characters
pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))

def udf_to_pdf(udf_file, pdf_file):
    # Open the UDF file and read the content.xml file
    with zipfile.ZipFile(udf_file, 'r') as z:
        if 'content.xml' in z.namelist():
            with z.open('content.xml') as content_file:
                tree = ET.parse(content_file, parser=ET.XMLParser(encoding='utf-8'))
                root = tree.getroot()
        else:
            print("The 'content.xml' file could not be found in the UDF file.")
            exit()

    # Retrieve content text
    content_element = root.find('content')
    if content_element is not None:
        content_text = content_element.text
        if content_text.startswith('<![CDATA[') and content_text.endswith(']]>'):
            content_text = content_text[9:-3]
    else:
        print("'content' could not be found in the XML.")
        exit()

    # Process the 'elements' section
    elements_element = root.find('elements')
    if elements_element is not None:
        # Create the PDF document
        pdf = SimpleDocTemplate(pdf_file, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        # Define a style that supports Turkish characters
        normal_style = ParagraphStyle('CustomNormal', 
                                      parent=styles['Normal'],
                                      fontName='DejaVuSans',
                                      encoding='utf-8')

        content_buffer = content_text

        for elem in elements_element:
            if elem.tag == 'paragraph':
                # Process the paragraph content
                paragraph_text = ''
                for child in elem:
                    if child.tag == 'content':
                        # Get and format the text
                        start_offset = int(child.get('startOffset', '0'))
                        length = int(child.get('length', '0'))
                        text = content_buffer[start_offset:start_offset+length]

                        # Get style information
                        style = ''
                        if child.get('bold', 'false') == 'true':
                            style += '<b>'
                        if child.get('italic', 'false') == 'true':
                            style += '<i>'

                        # Add the text
                        paragraph_text += f"{style}{text}"

                        # Closing tags
                        if 'i' in style:
                            paragraph_text += '</i>'
                        if 'b' in style:
                            paragraph_text += '</b>'
                    elif child.tag == 'space':
                        paragraph_text += ' '
                    elif child.tag == 'image':
                        # Add the image
                        image_data = child.get('imageData')
                        if image_data:
                            image_bytes = base64.b64decode(image_data)
                            image_stream = io.BytesIO(image_bytes)
                            img = Image(image_stream)
                            elements.append(img)

                # Add the paragraph
                elements.append(Paragraph(paragraph_text, normal_style))
                elements.append(Spacer(1, 5))
            elif elem.tag == 'table':
                # Create the table
                table_data = []
                rows = elem.findall('row')
                for row in rows:
                    row_data = []
                    cells = row.findall('cell')
                    for cell in cells:
                        cell_text = ''
                        paragraphs = cell.findall('paragraph')
                        for para in paragraphs:
                            for child in para:
                                if child.tag == 'content':
                                    start_offset = int(child.get('startOffset', '0'))
                                    length = int(child.get('length', '0'))
                                    text = content_buffer[start_offset:start_offset+length]

                                    # Get style information
                                    style = ''
                                    if child.get('bold', 'false') == 'true':
                                        style += '<b>'
                                    if child.get('italic', 'false') == 'true':
                                        style += '<i>'

                                    # Add the text
                                    cell_text += f"{style}{text}"

                                    # Closing tags
                                    if 'i' in style:
                                        cell_text += '</i>'
                                    if 'b' in style:
                                        cell_text += '</b>'
                                elif child.tag == 'space':
                                    cell_text += ' '
                                elif child.tag == 'image':
                                    # Images may not be supported inside tables
                                    pass
                        row_data.append(Paragraph(cell_text, normal_style))
                    table_data.append(row_data)
                # Set the table style
                table_style = TableStyle([
                    ('GRID', (0,0), (-1,-1), 1, colors.black),
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ])
                table = Table(table_data)
                table.setStyle(table_style)
                elements.append(table)
                elements.append(Spacer(1, 5))
        # Build the PDF document
        pdf.build(elements)
        print(f"PDF file created: {pdf_file}")
    else:
        print("'elements' could not be found in the XML.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python udf_to_pdf.py input.udf")
        exit()

    udf_file = sys.argv[1]

    if not os.path.isfile(udf_file):
        print(f"Input file not found: {udf_file}")
        exit()

    filename, ext = os.path.splitext(udf_file)

    if ext.lower() == '.udf':
        pdf_file = filename + '.pdf'
        udf_to_pdf(udf_file, pdf_file)
    else:
        print("Please provide a .udf file.")

if __name__ == '__main__':
    main()
