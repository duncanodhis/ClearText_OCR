import os
from google.cloud import vision
from fpdf import FPDF
import docx
import pandas as pd
import csv
import json
import xml.etree.ElementTree as ET
import fitz  # PyMuPDF for handling PDFs
from googletrans import Translator
import os
from google.cloud import vision
from fpdf import FPDF
import docx
import pandas as pd
import csv
import json
import xml.etree.ElementTree as ET
import fitz  # PyMuPDF for handling PDFs
from googletrans import Translator, LANGUAGES

class OCRModel:
    def __init__(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "config.json"
        self.client = vision.ImageAnnotatorClient()
        self.translator = Translator()
    
    def perform_ocr(self, file_path):
        ocr_text = ""
        if file_path.lower().endswith(".pdf"):
            pdf_document = fitz.open(file_path)
            total_pages = len(pdf_document)
            
            for page_num in range(total_pages):
                page = pdf_document.load_page(page_num)
                pix = page.get_pixmap()
                img_data = pix.tobytes()
                image = vision.Image(content=img_data)
                response = self.client.text_detection(image=image)
                text = response.text_annotations[0].description if response.text_annotations else ""
                ocr_text += text + "\n"
        else:
            with open(file_path, 'rb') as image_file:
                content = image_file.read()
            image = vision.Image(content=content)
            response = self.client.text_detection(image=image)
            text = response.text_annotations[0].description if response.text_annotations else ""
            ocr_text = text

        return ocr_text

    def detect_language(self, text):
        if not text:
            return None
        detection = self.translator.detect(text)
        return detection.lang

    def translate_text(self, text, target_language, source_language=None):
        if not text:
            return ""
        if source_language:
            translation = self.translator.translate(text, src=source_language, dest=target_language)
        else:
            translation = self.translator.translate(text, dest=target_language)
        return translation.text

    def get_supported_languages(self):
        return LANGUAGES
