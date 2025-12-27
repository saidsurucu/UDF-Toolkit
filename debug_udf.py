import sys
import os
import zipfile
import xml.etree.ElementTree as ET

def debug_udf(udf_file):
    print(f"Analyzing {udf_file}")
    
    content_text = ""
    root = None
    
    if zipfile.is_zipfile(udf_file):
        with zipfile.ZipFile(udf_file, 'r') as z:
            if 'content.xml' in z.namelist():
                with z.open('content.xml') as content_file:
                    tree = ET.parse(content_file, parser=ET.XMLParser(encoding='utf-8'))
                    root = tree.getroot()
    else:
        try:
            tree = ET.parse(udf_file, parser=ET.XMLParser(encoding='utf-8'))
            root = tree.getroot()
        except Exception as e:
            print(f"Error parsing XML: {e}")
            return

    if root is None:
        print("Root is None")
        return

    content_element = root.find('content')
    if content_element is not None:
        content_text = content_element.text or ""
        if content_text.startswith('<![CDATA[') and content_text.endswith(']]>'):
            content_text = content_text[9:-3]
        
        print(f"Content Text Length: {len(content_text)}")
        has_newlines = '\n' in content_text
        print(f"Content contains newlines: {has_newlines}")
        print(f"First 100 chars of content: {repr(content_text[:100])}")
    
    elements = root.find('elements')
    if elements is not None:
        paragraphs = elements.findall('paragraph')
        print(f"Found {len(paragraphs)} paragraphs.")
        
        # Analyze the first few paragraphs
        for i, para in enumerate(paragraphs[:5]):
            print(f"\nParagraph {i+1}:")
            last_end = 0
            
            for child in para:
                start = int(child.get('startOffset', 0)) if child.get('startOffset') else None
                length = int(child.get('length', 0)) if child.get('length') else 0
                tag = child.tag
                
                print(f"  Tag: {tag}, Start: {start}, Length: {length}")
                
                if start is not None:
                    if start > last_end:
                        gap_content = content_text[last_end:start]
                        print(f"    Gap [{last_end}:{start}]: {repr(gap_content)}")
                    
                    if child.tag == 'content' or child.tag == 'field':
                         text_segment = content_text[start:start+length]
                         print(f"    Text: {repr(text_segment)}")
                    
                    last_end = start + length

if __name__ == "__main__":
    if len(sys.argv) > 1:
        debug_udf(sys.argv[1])
    else:
        print("Usage: python debug_udf.py <filename>")
