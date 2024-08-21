import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk  # For handling different image formats
from google.cloud import vision  # For OCR processing
import os
from fpdf import FPDF
from io import BytesIO
import time  # Simulate processing time for demonstration

class ClearTextApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window Configuration
        self.title("ClearText: AI Optical Character Recognition")
        self.geometry("800x600")  # Set window size

        # Add Logo and Title
        self.create_header()

        # Create Menu Bar
        self.create_menu()

        # Create Tabs
        self.create_tabs()

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Welcome to ClearText!")
        self.status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor='w')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Placeholder for OCR result text
        self.ocr_text = ""

    def create_header(self):
        # Header Frame
        header_frame = ttk.Frame(self)
        header_frame.pack(pady=20)
        header_frame.grid_columnconfigure(1, weight=1)

        # Load Logo Image (ensure your logo image path is correct)
        try:
            logo_image = Image.open("logo.png")  # Change 'logo.png' to your image file
            logo_image = logo_image.resize((50, 50), Image.ANTIALIAS)  # Resize logo if necessary
            self.logo = ImageTk.PhotoImage(logo_image)
        except Exception as e:
            print(f"Error loading logo: {e}")
            self.logo = None

        # Logo Label
        if self.logo:
            logo_label = ttk.Label(header_frame, image=self.logo)
            logo_label.grid(row=0, column=0, padx=10)
        
        # Title Label (centered)
        title_label = ttk.Label(header_frame, text="ClearText: AI Optical Character Recognition", 
                                font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=1)

        # Center align both logo and title
        header_frame.grid_columnconfigure(1, weight=1)

    def create_menu(self):
        # Menu Bar
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        # File Menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit Menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo")
        edit_menu.add_command(label="Redo")
        edit_menu.add_command(label="Clear")
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # Settings Menu
        settings_menu = tk.Menu(menu_bar, tearoff=0)
        settings_menu.add_command(label="API Key Settings")
        settings_menu.add_command(label="Language Settings")
        settings_menu.add_command(label="Theme Settings")
        menu_bar.add_cascade(label="Settings", menu=settings_menu)

        # Help Menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="User Guide")
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

    def create_tabs(self):
        # Create Tabs
        tab_control = ttk.Notebook(self)

        # OCR Tab
        self.ocr_tab = ttk.Frame(tab_control)
        tab_control.add(self.ocr_tab, text="OCR Processing")
        self.setup_ocr_tab()

        # Translation & Speech Tab
        self.translation_tab = ttk.Frame(tab_control)
        tab_control.add(self.translation_tab, text="Translation & Speech")
        self.setup_translation_tab()

        # History Tab
        self.history_tab = ttk.Frame(tab_control)
        tab_control.add(self.history_tab, text="History")
        self.setup_history_tab()

        tab_control.pack(expand=1, fill='both')

    def setup_ocr_tab(self):
        # File Upload Section for OCR
        ttk.Label(self.ocr_tab, text="Upload an Image or PDF for OCR").pack(pady=10)
        upload_btn = ttk.Button(self.ocr_tab, text="Upload File", command=self.open_file)
        upload_btn.pack(pady=5)

        # Progress Bar for OCR
        self.progress = ttk.Progressbar(self.ocr_tab, length=400, mode='determinate')
        self.progress.pack(pady=10)
        self.progress_label = ttk.Label(self.ocr_tab, text="Processing: 0%")
        self.progress_label.pack()

        # Text Display Area for OCR Result
        self.ocr_result = tk.Text(self.ocr_tab, wrap='word', height=15)
        self.ocr_result.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def setup_translation_tab(self):
        # Source Text Area for Translation
        ttk.Label(self.translation_tab, text="Source Text").pack(pady=10)
        self.source_text = tk.Text(self.translation_tab, wrap='word', height=8)
        self.source_text.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        # Translation Button
        translate_btn = ttk.Button(self.translation_tab, text="Translate", command=self.translate_text)
        translate_btn.pack(pady=10)

        # Translated Text Area
        ttk.Label(self.translation_tab, text="Translated Text").pack(pady=10)
        self.translated_text = tk.Text(self.translation_tab, wrap='word', height=8)
        self.translated_text.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

    def setup_history_tab(self):
        # List View of Previously Processed Files
        ttk.Label(self.history_tab, text="History of Processed Files").pack(pady=10)
        self.history_listbox = tk.Listbox(self.history_tab, height=15)
        self.history_listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def open_file(self):
        # Open File Dialog for OCR
        file_path = filedialog.askopenfilename(filetypes=[("Images and PDFs", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.pdf")])
        if file_path:
            self.status_var.set(f"Opened file: {file_path}")
            # Perform OCR on the file
            self.ocr_text = ""
            self.ocr_result.delete(1.0, tk.END)
            self.progress['value'] = 0
            self.progress_label.config(text="Processing: 0%")
            self.update_idletasks()  # Update the UI
            self.after(100, lambda: self.perform_ocr(file_path))  # Run OCR with delay to show progress

    def perform_ocr(self, file_path):
        # Simulate OCR processing time for demonstration
        num_steps = 10
        step_duration = 0.5  # Duration per step in seconds

        # Set environment variable for credentials
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "config.json"

        # Create a Vision client
        client = vision.ImageAnnotatorClient()

        if file_path.lower().endswith(".pdf"):
            import fitz  # PyMuPDF for handling PDFs
            pdf_document = fitz.open(file_path)
            total_pages = len(pdf_document)
            
            for page_num in range(total_pages):
                page = pdf_document.load_page(page_num)
                pix = page.get_pixmap()
                img_data = pix.tobytes()
                image = vision.Image(content=img_data)
                response = client.text_detection(image=image)
                text = response.text_annotations[0].description if response.text_annotations else ""
                self.ocr_text += text + "\n"
                self.update_progress((page_num + 1) / total_pages * 100)
                time.sleep(step_duration)  # Simulate processing delay
        else:
            # Read the image file
            with open(file_path, 'rb') as image_file:
                content = image_file.read()

            # Prepare the image data
            image = vision.Image(content=content)

            # Perform OCR
            response = client.text_detection(image=image)
            text = response.text_annotations[0].description if response.text_annotations else ""
            self.ocr_text = text

            self.update_progress(100)  # Completed 100% progress

        self.ocr_result.insert(tk.END, self.ocr_text)  # Display OCR result
        self.add_to_history(file_path)
        self.status_var.set(f"OCR completed for: {file_path}")

    def update_progress(self, percentage):
        self.progress['value'] = percentage
        self.progress_label.config(text=f"Processing: {int(percentage)}%")
        self.update_idletasks()

    def save_file_as(self):
        if not self.ocr_text:
            messagebox.showerror("Error", "No OCR result to save.")
            return

        # Ask the user for the file format and file path
        filetypes = [("Text file", "*.txt"), ("PDF file", "*.pdf")]
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=filetypes)
        if file_path:
            if file_path.endswith(".pdf"):
                self.save_as_pdf(file_path)
            else:
                with open(file_path, "w") as file:
                    file.write(self.ocr_text)
                messagebox.showinfo("Success", f"File saved as: {file_path}")

    def save_as_pdf(self, file_path):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, self.ocr_text)
        pdf.output(file_path)
        messagebox.showinfo("Success", f"PDF file saved as: {file_path}")

    def translate_text(self):
        # Simulate translation process for demonstration
        source_text = self.source_text.get("1.0", tk.END).strip()
        if source_text:
            self.translated_text.delete("1.0", tk.END)
            self.translated_text.insert(tk.END, f"Translated text for: {source_text}")
            self.status_var.set("Translation completed.")
        else:
            messagebox.showerror("Error", "No text to translate.")

    def add_to_history(self, file_path):
        self.history_listbox.insert(tk.END, file_path)

    def show_about(self):
        messagebox.showinfo("About ClearText", "ClearText: AI Optical Character Recognition\nVersion 1.0")

if __name__ == "__main__":
    app = ClearTextApp()
    app.mainloop()
