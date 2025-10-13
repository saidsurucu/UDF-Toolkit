from docx.oxml.ns import qn

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

def get_bullet_attrs(paragraph):
    numPr = paragraph.find('.//w:numPr', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
    if numPr is not None:
        ilvl = numPr.find('.//w:ilvl', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
        numId = numPr.find('.//w:numId', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
        if ilvl is not None and numId is not None:
            bullet_type = get_bullet_type(numId.get(qn("w:val")))
            return f'Bulleted="true" ListId="{numId.get(qn("w:val"))}" ListLevel="{int(ilvl.get(qn("w:val"))) + 1}" BulletType="{bullet_type}"'
    return ''

def get_bullet_type(num_id):
    bullet_types = {
        "1": "BULLET_TYPE_ELLIPSE",
        "2": "BULLET_TYPE_RECTANGLE",
        "3": "BULLET_TYPE_RECTANGLE_D",
        "4": "BULLET_TYPE_ARROW",
        "5": "BULLET_TYPE_DIAMOND",
        "6": "BULLET_TYPE_TRIANGLE",
    }
    return bullet_types.get(num_id, "BULLET_TYPE_ELLIPSE")  # Default to ELLIPSE

def get_font_properties(run):
    font_family = run.findtext('.//w:rFonts[@w:ascii]', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}) or "Times New Roman"
    font_size = run.findtext('.//w:sz', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}) or "20"
    font_size = str(int(font_size) // 2)  # Convert half-points to points

    style_attrs = [f'family="{font_family}"', f'size="{font_size}"']
    if run.find('.//w:b', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}) is not None:
        style_attrs.append('bold="true"')
    if run.find('.//w:i', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}) is not None:
        style_attrs.append('italic="true"')

    return ' '.join(style_attrs)

def get_line_spacing(paragraph):
    spacing = paragraph.find('.//w:spacing', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
    if spacing is not None:
        line = spacing.get(qn('w:line'))
        lineRule = spacing.get(qn('w:lineRule'))
        if line and lineRule:
            if lineRule == 'auto':
                # Convert to UDF line spacing (DOCX 2.0 = UDF 1.0)
                return max(0, (float(line) / 240) - 1)
            elif lineRule == 'exact' or lineRule == 'atLeast':
                # Convert twips to points and adjust for UDF
                return max(0, (float(line) / 20) - 12)
    return 0.0  # Default to single spacing in UDF
