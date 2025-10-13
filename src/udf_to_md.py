import sys
import os
import xml.etree.ElementTree as ET
import zipfile
import base64
import io

def is_zip_file(file_path):
    """Check if the file is a valid ZIP file"""
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            return True
    except zipfile.BadZipFile:
        return False

def udf_to_markdown(udf_file):
    root = None
    
    # Check if the file is a ZIP file
    if is_zip_file(udf_file):
        # Process as a ZIP file
        with zipfile.ZipFile(udf_file, 'r') as z:
            if 'content.xml' in z.namelist():
                with z.open('content.xml') as content_file:
                    tree = ET.parse(content_file)
                    root = tree.getroot()
            else:
                print("The 'content.xml' file could not be found in the UDF file.")
                exit()
    else:
        # Process as an XML file directly
        try:
            tree = ET.parse(udf_file)
            root = tree.getroot()
        except ET.ParseError:
            print(f"The file {udf_file} is neither a valid ZIP nor a valid XML file.")
            exit()

    if root is None:
        print("Failed to parse the file.")
        exit()

    # Initialize the markdown output
    markdown_output = ""

    # Create a dictionary for style definitions
    styles = {}

    # Retrieve style information
    styles_element = root.find('styles')
    if styles_element is not None:
        for style in styles_element.findall('style'):
            style_name = style.get('name')
            style_attributes = {
                'family': style.get('family'),
                'size': int(style.get('size', 12)),
                'bold': style.get('bold', 'false') == 'true',
                'italic': style.get('italic', 'false') == 'true',
                'foreground': int(style.get('foreground', '-13421773')),
            }
            styles[style_name] = style_attributes

    # Retrieve content text
    content_element = root.find('content')
    if content_element is not None:
        content_text = content_element.text
        if content_text and content_text.startswith('<![CDATA[') and content_text.endswith(']]>'):
            content_text = content_text[9:-3]
    else:
        print("'content' could not be found in the XML.")
        exit()

    # Process the 'elements' section
    elements_element = root.find('elements')
    
    if elements_element is not None:
        for elem in elements_element:
            if elem.tag == 'paragraph':
                # Handle the paragraph
                paragraph_text = ""
                
                # Set paragraph alignment (we'll add this as HTML in markdown since markdown doesn't have native alignment)
                alignment = elem.get('Alignment', '0')
                alignment_tag = ""
                if alignment == '1':
                    alignment_tag = "<div align='center'>"
                elif alignment == '2':
                    alignment_tag = "<div align='right'>"
                elif alignment == '3':
                    alignment_tag = "<div align='justify'>"
                
                # Process the paragraph content
                for child in elem:
                    if child.tag == 'content':
                        # Get the text
                        start_offset = int(child.get('startOffset', '0'))
                        length = int(child.get('length', '0'))
                        text = content_text[start_offset:start_offset+length]
                        
                        # Apply formatting
                        if child.get('bold', 'false') == 'true' and child.get('italic', 'false') == 'true':
                            text = f"***{text}***"
                        elif child.get('bold', 'false') == 'true':
                            text = f"**{text}**"
                        elif child.get('italic', 'false') == 'true':
                            text = f"*{text}*"
                            
                        paragraph_text += text
                        
                    elif child.tag == 'space':
                        paragraph_text += " "
                    elif child.tag == 'image':
                        # For images, we'll just add a placeholder in markdown
                        paragraph_text += "[Image]"
                
                # Apply alignment if needed
                if alignment_tag:
                    paragraph_text = f"{alignment_tag}{paragraph_text}</div>"
                
                markdown_output += paragraph_text + "\n\n"
                
            elif elem.tag == 'table':
                # Handle tables
                column_count = int(elem.get('columnCount', '1'))
                rows = elem.findall('row')
                
                # Create table header row with correct number of columns
                markdown_output += "| " + " | ".join(["Column"] * column_count) + " |\n"
                markdown_output += "| " + " | ".join(["---"] * column_count) + " |\n"
                
                for row in rows:
                    cells = row.findall('cell')
                    row_text = "| "
                    
                    for cell in cells:
                        cell_text = ""
                        paragraphs = cell.findall('paragraph')
                        
                        for para in paragraphs:
                            para_text = ""
                            
                            for child in para:
                                if child.tag == 'content':
                                    # Get the text
                                    start_offset = int(child.get('startOffset', '0'))
                                    length = int(child.get('length', '0'))
                                    text = content_text[start_offset:start_offset+length]
                                    
                                    # Apply formatting
                                    if child.get('bold', 'false') == 'true' and child.get('italic', 'false') == 'true':
                                        text = f"***{text}***"
                                    elif child.get('bold', 'false') == 'true':
                                        text = f"**{text}**"
                                    elif child.get('italic', 'false') == 'true':
                                        text = f"*{text}*"
                                        
                                    para_text += text
                                    
                                elif child.tag == 'space':
                                    para_text += " "
                                elif child.tag == 'image':
                                    para_text += "[Image]"
                            
                            cell_text += para_text + " "
                        
                        # Remove pipe characters from cell content as they would break the markdown table
                        cell_text = cell_text.replace("|", "\\|").strip()
                        row_text += cell_text + " | "
                    
                    markdown_output += row_text + "\n"
                
                markdown_output += "\n"
    else:
        print("'elements' could not be found in the XML.")

    return markdown_output

def main():
    if len(sys.argv) < 2:
        print("Usage: python udf_to_markdown.py input.udf")
        exit()

    udf_file = sys.argv[1]

    if not os.path.isfile(udf_file):
        print(f"Input file not found: {udf_file}")
        exit()

    # Convert UDF to markdown and print to console
    markdown_content = udf_to_markdown(udf_file)
    print(markdown_content)
    
    # Optionally save to a file
    filename, ext = os.path.splitext(udf_file)
    markdown_file = filename + '.md'
    with open(markdown_file, 'w', encoding='utf-8') as md_file:
        md_file.write(markdown_content)
    print(f"Markdown file created: {markdown_file}")

if __name__ == '__main__':
    main()