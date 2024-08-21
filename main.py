from ocr_view import OCRView
from ocr_controller import OCRController

if __name__ == "__main__":
    view = OCRView()
    controller = OCRController(view)
    view.mainloop()
