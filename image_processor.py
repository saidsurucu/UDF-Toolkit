import base64
from docx.oxml.ns import qn
from PIL import Image
import io

def process_image(drawing, document):
    try:
        inline = drawing.find('.//wp:inline', namespaces={'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'})
        anchor = drawing.find('.//wp:anchor', namespaces={'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'})
        
        extent = None
        if inline is not None:
            extent = inline.find('.//wp:extent', namespaces={'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'})
        elif anchor is not None:
            extent = anchor.find('.//wp:extent', namespaces={'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'})
        
        if extent is not None:
            width = int(extent.get('cx')) // 9525
            height = int(extent.get('cy')) // 9525
        else:
            width = height = 100

        blip = drawing.find('.//a:blip', namespaces={'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'})
        if blip is not None:
            rId = blip.get(qn('r:embed'))
            if rId in document.part.rels:
                image_part = document.part.rels[rId].target_part
                image_bytes = image_part.blob
                
                try:
                    with Image.open(io.BytesIO(image_bytes)) as img:
                        png_buffer = io.BytesIO()
                        img.save(png_buffer, format='PNG')
                        png_bytes = png_buffer.getvalue()
                        image_data = base64.b64encode(png_bytes).decode('utf-8')
                except Exception:
                    image_data = base64.b64encode(image_bytes).decode('utf-8')
                
                return image_data, width, height

    except Exception:
        pass
    
    return None, None, None