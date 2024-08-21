import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from googletrans import LANGUAGES
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from googletrans import LANGUAGES
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from googletrans import LANGUAGES

class OCRView(tk.Tk):
    def __init__(self):
        super().__init__()

        self.controller = None

        # Window Configuration
        self.title("ClearText: AI Optical Character Recognition")
        self.geometry("800x600")
        self.minsize(600, 400)  # Set minimum size for better usability

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
        self.translated_text = ""

    def create_header(self):
        header_frame = ttk.Frame(self)
        header_frame.pack(pady=10, fill=tk.X)
        header_frame.grid_columnconfigure(1, weight=1)

        try:
            logo_image = Image.open("logo.png")
            logo_image = logo_image.resize((50, 50), Image.ANTIALIAS)
            self.logo = ImageTk.PhotoImage(logo_image)
        except Exception as e:
            print(f"Error loading logo: {e}")
            self.logo = None

        if self.logo:
            logo_label = ttk.Label(header_frame, image=self.logo)
            logo_label.grid(row=0, column=0, padx=10)

        title_label = ttk.Label(header_frame, text="ClearText: AI Optical Character Recognition", 
                                font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=1, padx=10, sticky='ew')
        header_frame.grid_columnconfigure(1, weight=1)

    def create_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo")
        edit_menu.add_command(label="Redo")
        edit_menu.add_command(label="Clear")
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        settings_menu = tk.Menu(menu_bar, tearoff=0)
        settings_menu.add_command(label="API Key Settings")
        settings_menu.add_command(label="Language Settings")
        settings_menu.add_command(label="Theme Settings")
        menu_bar.add_cascade(label="Settings", menu=settings_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="User Guide")
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

    def create_tabs(self):
        tab_control = ttk.Notebook(self)

        self.ocr_tab = ttk.Frame(tab_control)
        tab_control.add(self.ocr_tab, text="OCR Processing")
        self.setup_ocr_tab()

        self.translation_tab = ttk.Frame(tab_control)
        tab_control.add(self.translation_tab, text="Translation & Speech")
        self.setup_translation_tab()

        self.history_tab = ttk.Frame(tab_control)
        tab_control.add(self.history_tab, text="History")
        self.setup_history_tab()

        tab_control.pack(expand=1, fill='both')

    def setup_ocr_tab(self):
        ocr_frame = ttk.Frame(self.ocr_tab)
        ocr_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        ttk.Label(ocr_frame, text="Upload an Image or PDF for OCR").pack(pady=10)
        upload_btn = ttk.Button(ocr_frame, text="Upload File", command=self.open_file)
        upload_btn.pack(pady=5)

        self.progress = ttk.Progressbar(ocr_frame, length=400, mode='determinate')
        self.progress.pack(pady=10, fill=tk.X)
        self.progress_label = ttk.Label(ocr_frame, text="Processing: 0%")
        self.progress_label.pack()

        self.ocr_result = tk.Text(ocr_frame, wrap='word', height=15)
        self.ocr_result.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def setup_translation_tab(self):
        translation_frame = ttk.Frame(self.translation_tab)
        translation_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        ttk.Label(translation_frame, text="Source Text").pack(pady=10)
        self.source_text = tk.Text(translation_frame, wrap='word', height=8)
        self.source_text.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        language_frame = ttk.Frame(translation_frame)
        language_frame.pack(pady=10, fill=tk.X)

        ttk.Label(language_frame, text="Detect Source Language").pack(pady=5)
        self.detect_language_btn = ttk.Button(language_frame, text="Detect Language", command=self.detect_language)
        self.detect_language_btn.pack(pady=5)

        ttk.Label(language_frame, text="Source Language").pack(pady=5)
        self.source_language_var = tk.StringVar(value="auto")
        source_language_menu = ttk.Combobox(language_frame, textvariable=self.source_language_var)
        source_language_menu['values'] = ['auto'] + [name for code, name in LANGUAGES.items()]
        source_language_menu.pack(pady=5, fill=tk.X)

        ttk.Label(language_frame, text="Target Language").pack(pady=5)
        self.target_language_var = tk.StringVar(value="en")
        target_language_menu = ttk.Combobox(language_frame, textvariable=self.target_language_var)
        target_language_menu['values'] = [name for code, name in LANGUAGES.items()]
        target_language_menu.pack(pady=5, fill=tk.X)

        translate_btn = ttk.Button(translation_frame, text="Translate", command=self.translate_text)
        translate_btn.pack(pady=10)

        ttk.Label(translation_frame, text="Translated Text").pack(pady=10)
        self.translated_text_area = tk.Text(translation_frame, wrap='word', height=8)
        self.translated_text_area.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

    def setup_history_tab(self):
        history_frame = ttk.Frame(self.history_tab)
        history_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        ttk.Label(history_frame, text="History of Processed Files").pack(pady=10)
        self.history_listbox = tk.Listbox(history_frame, height=15)
        self.history_listbox.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png"), ("PDF Files", "*.pdf")])
        if file_path:
            self.controller.process_file(file_path)

    def save_file_as(self):
        filetypes = [
            ("Text Files", "*.txt"),
            ("PDF Files", "*.pdf"),
            ("Word Documents", "*.docx"),
            ("Excel Files", "*.xlsx"),
            ("CSV Files", "*.csv"),
            ("HTML Files", "*.html"),
            ("JSON Files", "*.json"),
            ("XML Files", "*.xml"),
        ]
        
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=filetypes)
        if file_path:
            extension = os.path.splitext(file_path)[1]
            if extension == ".txt":
                self.controller.save_as_text(self.ocr_text, file_path)
            elif extension == ".pdf":
                self.controller.save_as_pdf(self.ocr_text, file_path)
            elif extension == ".docx":
                self.controller.save_as_docx(self.ocr_text, file_path)
            elif extension == ".xlsx":
                self.controller.save_as_xlsx(self.ocr_text, file_path)
            elif extension == ".csv":
                self.controller.save_as_csv(self.ocr_text, file_path)
            elif extension == ".html":
                self.controller.save_as_html(self.ocr_text, file_path)
            elif extension == ".json":
                self.controller.save_as_json(self.ocr_text, file_path)
            elif extension == ".xml":
                self.controller.save_as_xml(self.ocr_text, file_path)
            messagebox.showinfo("Success", f"File saved as {file_path}")

    def detect_language(self):
        source_text = self.source_text.get("1.0", tk.END).strip()
        detected_language = self.controller.detect_language(source_text)
        if detected_language:
            self.source_language_var.set(LANGUAGES.get(detected_language, "auto"))
        else:
            messagebox.showwarning("Warning", "Unable to detect language.")

    def translate_text(self):
        source_text = self.source_text.get("1.0", tk.END).strip()
        if not source_text:
            messagebox.showwarning("Warning", "No text to translate.")
            return

        source_language = self.source_language_var.get()
        target_language = self.target_language_var.get()
        target_language_code = [code for code, name in LANGUAGES.items() if name == target_language]

        if not target_language_code:
            messagebox.showwarning("Warning", "Selected target language is not supported.")
            return

        target_language_code = target_language_code[0]

        if source_language == "auto":
            source_language = None

        translated_text = self.controller.translate_text(source_text, target_language_code, source_language)
        self.translated_text_area.delete("1.0", tk.END)
        self.translated_text_area.insert(tk.END, translated_text)
    
    def show_about(self):
        messagebox.showinfo("About", "ClearText: AI Optical Character Recognition\nVersion 1.0\nDeveloped by [Your Name]")
    
    def set_controller(self, controller):
        self.controller = controller

    def update_ocr_result(self, text):
        self.ocr_text = text
        self.ocr_result.delete(1.0, tk.END)
        self.ocr_result.insert(tk.END, text)

    def update_progress(self, value, text):
        self.progress["value"] = value
        self.progress_label.config(text=text)
        self.update_idletasks()

    def add_to_history(self, file_path):
        self.history_listbox.insert(tk.END, file_path)
