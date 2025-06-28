# utils/editor.py

from docx.shared import Pt
from deep_translator import GoogleTranslator
from docx import Document

def translate_paragraphs(doc: Document, target_lang: str):
    translator = GoogleTranslator(source='auto', target=target_lang)
    for para in doc.paragraphs:
        if para.text.strip():
            para.text = translator.translate(para.text)
    return doc

def style_paragraphs(doc: Document, font_name='Arial', font_size=12):
    for para in doc.paragraphs:
        for run in para.runs:
            run.font.name = font_name
            run.font.size = Pt(font_size)
    return doc

def save_document(doc: Document, output_path: str):
    doc.save(output_path)
