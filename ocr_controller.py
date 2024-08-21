from ocr_model import OCRModel
from tkinter import messagebox
class OCRController:
    def __init__(self, view):
        self.view = view
        self.model = OCRModel()
        self.view.set_controller(self)

    def process_file(self, file_path):
        self.view.update_progress(0, "Processing: 0%")
        try:
            ocr_text = self.model.perform_ocr(file_path)
            self.view.update_ocr_result(ocr_text)
            self.view.add_to_history(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            self.view.update_progress(100, "Processing: Done")

    def save_as_text(self, ocr_text, file_path):
        self.model.save_as_text(ocr_text, file_path)

    def save_as_pdf(self, ocr_text, file_path):
        self.model.save_as_pdf(ocr_text, file_path)

    def save_as_docx(self, ocr_text, file_path):
        self.model.save_as_docx(ocr_text, file_path)

    def save_as_xlsx(self, ocr_text, file_path):
        self.model.save_as_xlsx(ocr_text, file_path)

    def save_as_csv(self, ocr_text, file_path):
        self.model.save_as_csv(ocr_text, file_path)

    def save_as_html(self, ocr_text, file_path):
        self.model.save_as_html(ocr_text, file_path)

    def save_as_json(self, ocr_text, file_path):
        self.model.save_as_json(ocr_text, file_path)

    def save_as_xml(self, ocr_text, file_path):
        self.model.save_as_xml(ocr_text, file_path)

    def translate_text(self, text, target_language, source_language=None):
        return self.model.translate_text(text, target_language, source_language)

    def detect_language(self, text):
        return self.model.detect_language(text)
