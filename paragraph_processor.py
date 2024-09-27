from docx.oxml.ns import qn
from image_processor import process_image
from utils import get_alignment, get_indent_attrs, get_bullet_attrs

def process_paragraph(paragraph, document, current_offset):
    EMPTY_PARAGRAPH_PLACEHOLDER = '\u200B'  # Zero-width space
    TAB_CHARACTER = '\t'  # Tab character
    
    para_text = ""
    para_elements = []
    
    # Numaralandırma ve madde işareti özelliklerini al
    numPr = paragraph.find('.//w:numPr', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
    numbered = False
    list_id = ""
    list_level = ""
    number_type = ""
    
    if numPr is not None:
        ilvl = numPr.find('.//w:ilvl', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
        numId = numPr.find('.//w:numId', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
        if ilvl is not None and numId is not None:
            numbered = True
            list_id = numId.get(qn("w:val"))
            list_level = str(int(ilvl.get(qn("w:val"))) + 1)
            number_type = get_number_type(list_id)
    
    for run in paragraph.findall('.//w:r', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}):
        # Process images in the run
        drawing_elements = run.findall('.//w:drawing', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
        if drawing_elements:
            for drawing in drawing_elements:
                image_data, width, height = process_image(drawing, document)
                if image_data:
                    # Insert a placeholder character in content
                    placeholder = '\uFFFC'  # Object Replacement Character
                    para_text += placeholder

                    # Add image element
                    para_elements.append(
                        f'<image imageData="{image_data}" '
                        f'startOffset="{current_offset}" length="1" width="{width}" height="{height}" />'
                    )
                    current_offset += 1
                else:
                    print("Failed to process image, skipping...")



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
                    para_elements.append(f'<tab {style_attr_str} startOffset="{current_offset}" length="1" />')
                    para_text += TAB_CHARACTER
                    current_offset += 1

    # If paragraph is empty, add placeholder
    if not para_text:
        para_text = EMPTY_PARAGRAPH_PLACEHOLDER
        para_elements.append(f'<content startOffset="{current_offset}" length="1" family="Times New Roman" size="10" />')
        current_offset += 1

    # Numaralandırma ve madde işareti özelliklerini paragraf elementine ekle
    paragraph_attrs = f'Alignment="{get_alignment(paragraph)}" {get_indent_attrs(paragraph)}'
    if numbered:
        if number_type.startswith("NUMBER_TYPE_"):
            paragraph_attrs += f' Numbered="true" ListId="{list_id}" ListLevel="{list_level}" NumberType="{number_type}"'
        else:
            paragraph_attrs += f' Bulleted="true" ListId="{list_id}" ListLevel="{list_level}" BulletType="{number_type}"'

    paragraph_element = f'<paragraph {paragraph_attrs}>{"".join(para_elements)}</paragraph>'
    return para_text, paragraph_element

def get_number_type(list_id):
    # Bu fonksiyonu, belgenizin numaralandırma tanımlarına göre özelleştirmeniz gerekebilir
    number_types = {
        "1": "NUMBER_TYPE_CHAR_SMALL_DOT",
        "2": "BULLET_TYPE_ARROW",
        "3": "NUMBER_TYPE_ROMAN_BIG_DOT",
        "4": "NUMBER_TYPE_CHAR_BIG_DOT",
        "5": "NUMBER_TYPE_CHAR_SMALL_PARANTHESE",
        "6": "NUMBER_TYPE_NUMBER_TRE",
        "7": "NUMBER_TYPE_ROMAN_SMALL_DOT",
        "8": "BULLET_TYPE_ELLIPSE",
        "9": "BULLET_TYPE_RECTANGLE",
        "10": "BULLET_TYPE_RECTANGLE_D",
        "11": "NUMBER_TYPE_NUMBER_PARANTHESE",
        "12": "BULLET_TYPE_DIAMOND",
        "13": "BULLET_TYPE_TRIANGLE",
        # Diğer numaralandırma ve madde işareti türlerini buraya ekleyin
    }
    return number_types.get(list_id, "NUMBER_TYPE_NUMBER_TRE")  # Varsayılan olarak NUMBER_TYPE_NUMBER_TRE kullan
