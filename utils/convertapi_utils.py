import os
import shutil

def convert_docx_to_pdf_and_download(filepath, output_folder, bearer_token=None):
    """
    Offline conversion from DOCX to PDF using docx2pdf.
    No API token required!
    """
    try:
        from docx2pdf import convert
        filename = os.path.basename(filepath)
        output_path = os.path.join(output_folder, filename.replace(".docx", ".pdf"))
        
        try:
            # docx2pdf works natively on Windows if MS Word is installed and activated
            convert(filepath, output_path)
        except Exception as ms_word_e:
            # Fallback: Pure Python text-to-PDF if MS Word COM fails (e.g. RPC failed)
            import fitz
            from docx import Document
            
            doc = Document(filepath)
            pdf = fitz.open()
            page = pdf.new_page()
            
            y = 50
            for para in doc.paragraphs:
                text = para.text.strip()
                if not text:
                    y += 15
                    continue
                    
                # Handle text wrapping manually or simple line breaks
                # We'll do a simple wrap at ~90 characters
                words = text.split()
                line = ""
                for word in words:
                    if len(line) + len(word) > 90:
                        if y > page.rect.height - 50:
                            page = pdf.new_page()
                            y = 50
                        page.insert_text((50, y), line, fontsize=11, fontname="helv")
                        y += 15
                        line = word + " "
                    else:
                        line += word + " "
                
                if line:
                    if y > page.rect.height - 50:
                        page = pdf.new_page()
                        y = 50
                    page.insert_text((50, y), line, fontsize=11, fontname="helv")
                    y += 25  # Paragraph spacing
            
            pdf.save(output_path)
            pdf.close()
        
        if os.path.exists(output_path):
            return True, output_path
        else:
            return False, "Failed to create PDF offline."
    except Exception as e:
        return False, f"Offline DOCX to PDF Conversion Error: {str(e)}"

def convert_pdf_to_docx_and_download(filepath, output_folder, bearer_token=None):
    """
    Offline conversion from PDF to DOCX using pdf2docx.
    No API token required!
    """
    try:
        from pdf2docx import Converter
        filename = os.path.basename(filepath)
        output_path = os.path.join(output_folder, filename.replace(".pdf", ".docx"))
        
        cv = Converter(filepath)
        cv.convert(output_path, start=0, end=None)
        cv.close()
        
        if os.path.exists(output_path):
            return True, output_path
        else:
            return False, "Failed to create DOCX offline."
    except Exception as e:
        return False, f"Offline PDF to DOCX Conversion Error: {str(e)}"

def compress_pdf_with_convertapi(filepath, output_folder, bearer_token=None, quality="medium"):
    """
    Offline PDF compression using PyMuPDF (fitz).
    No API token required!
    """
    try:
        import fitz
        filename = os.path.basename(filepath)
        output_path = os.path.join(output_folder, f"compressed_{filename}")
        
        doc = fitz.open(filepath)
        
        # Compression parameters based on quality
        if quality == "high":
            doc.save(output_path, garbage=4, deflate=True, clean=True)
        elif quality == "low":
            doc.save(output_path, garbage=1, deflate=False)
        else:
            # Medium/default
            doc.save(output_path, garbage=3, deflate=True)
            
        doc.close()
        
        if os.path.exists(output_path):
            return True, output_path
        else:
            return False, "Failed to compress PDF offline."
    except Exception as e:
        return False, f"Offline PDF Compression Error: {str(e)}"
