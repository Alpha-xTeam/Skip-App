import customtkinter as ctk
from tkinter import filedialog
import os
from .styles import Theme
from core.history import HistoryManager

class MainWindow(ctk.CTk):
    def __init__(self, downloader):
        super().__init__()
        
        self.downloader = downloader
        
        # Window Setup
        self.title("Skip - YouTube Downloader")
        self.geometry("1000x700")
        self.configure(fg_color=Theme.BG_DARK)
        
        # State
        self.pages = {}
        self.current_page = None
        self.last_clipboard_url = ""
        self.auto_paste_enabled = True
        self.history_mgr = HistoryManager()
        
        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Link callbacks
        self.downloader.progress_callback = self.update_progress
        self.downloader.status_callback = self.update_status
        self.downloader.complete_callback = self.on_complete
        
        self.create_sidebar()
        self.create_pages()
        self.show_page("downloads")
        
        # Start Clipboard Monitor
        self.check_clipboard()
        
    def check_clipboard(self):
        if self.auto_paste_enabled:
            clipboard_text = ""
            try:
                # Attempt to get clipboard with selection_get (better for different locales)
                clipboard_text = self.selection_get(selection='CLIPBOARD')
            except Exception:
                try:
                    # Fallback to standard clipboard_get
                    clipboard_text = self.clipboard_get()
                except Exception:
                    pass
            
            if clipboard_text:
                # Clean up the text, removing any invisible RTL/LTR characters or spaces
                clipboard_text = clipboard_text.strip()
                
                # Check if it's a new YouTube link
                if clipboard_text != self.last_clipboard_url and ("youtube.com" in clipboard_text.lower() or "youtu.be" in clipboard_text.lower()):
                    self.last_clipboard_url = clipboard_text
                    
                    # Only auto-paste if the field is empty or has a different URL
                    current_entry = self.url_entry.get()
                    if current_entry != clipboard_text:
                        self.url_entry.delete(0, "end")
                        self.url_entry.insert(0, clipboard_text)
                        self.update_status("Link Detected & Pasted")
        
        # Run again after 1500ms
        self.after(1500, self.check_clipboard)
        
    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=Theme.CARD_BG)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Brand
        self.brand = ctk.CTkLabel(self.sidebar, text="Skip", font=Theme.FONT_TITLE, text_color=Theme.PRIMARY)
        self.brand.pack(pady=40, padx=20, anchor="w")
        
        # Nav
        self.nav_buttons = {}
        self.nav_buttons["downloads"] = self.create_nav_item("Downloads", "📥", "downloads")
        self.nav_buttons["library"] = self.create_nav_item("Library", "📁", "library")

        
    def create_nav_item(self, label, icon, page_name):
        btn = ctk.CTkButton(
            self.sidebar, 
            text=f"  {icon}  {label}", 
            height=45, 
            anchor="w",
            corner_radius=8,
            fg_color="transparent",
            text_color=Theme.TEXT_MAIN,
            hover_color=Theme.INPUT_BG,
            font=("Segoe UI", 13),
            command=lambda p=page_name: self.show_page(p)
        )
        btn.pack(fill="x", padx=15, pady=5)
        return btn

    def create_pages(self):
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=1, sticky="nsew", padx=40, pady=40)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self.pages["downloads"] = self.create_downloads_page()
        self.pages["library"] = self.create_library_page()


    def show_page(self, page_name):
        if self.current_page:
            self.pages[self.current_page].grid_remove()
            self.nav_buttons[self.current_page].configure(fg_color="transparent", text_color=Theme.TEXT_MAIN)
            
        self.pages[page_name].grid(row=0, column=0, sticky="nsew")
        self.nav_buttons[page_name].configure(fg_color=Theme.PRIMARY, text_color=Theme.BG_DARK)
        self.current_page = page_name

    def create_downloads_page(self):
        page = ctk.CTkFrame(self.container, fg_color="transparent")
        page.grid_columnconfigure(0, weight=1)
        
        # Header
        ctk.CTkLabel(page, text="New Download", font=Theme.FONT_TITLE, text_color=Theme.TEXT_MAIN).grid(row=0, column=0, sticky="w", pady=(0, 30))
        
        # Content
        content = ctk.CTkFrame(page, fg_color=Theme.CARD_BG, corner_radius=15, border_width=1, border_color=Theme.INPUT_BG)
        content.grid(row=1, column=0, sticky="ew")
        content.grid_columnconfigure(0, weight=1)
        
        # URL
        ctk.CTkLabel(content, text="URL", font=Theme.FONT_LABEL, text_color=Theme.SECONDARY).pack(anchor="w", padx=30, pady=(30, 5))
        self.url_entry = ctk.CTkEntry(content, placeholder_text="Paste YouTube link here...", height=50, fg_color=Theme.BG_DARK, border_width=0, corner_radius=10)
        self.url_entry.pack(fill="x", padx=30, pady=(0, 20))
        self.enable_arabic_shortcuts(self.url_entry)
        
        # Options
        options = ctk.CTkFrame(content, fg_color="transparent")
        options.pack(fill="x", padx=30, pady=10)
        options.grid_columnconfigure((0, 1), weight=1)

        
        # Type
        type_f = ctk.CTkFrame(options, fg_color="transparent")
        type_f.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        ctk.CTkLabel(type_f, text="Format", font=Theme.FONT_LABEL, text_color=Theme.SECONDARY).pack(anchor="w")
        self.download_type = ctk.CTkComboBox(type_f, values=["Video (MP4)", "Audio (MP3)"], height=40, fg_color=Theme.BG_DARK, border_width=0)
        self.download_type.pack(fill="x", pady=5)
        
        # Quality
        qual_f = ctk.CTkFrame(options, fg_color="transparent")
        qual_f.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        ctk.CTkLabel(qual_f, text="Quality", font=Theme.FONT_LABEL, text_color=Theme.SECONDARY).pack(anchor="w")
        self.quality = ctk.CTkComboBox(qual_f, values=["Best", "1080p", "720p", "480p"], height=40, fg_color=Theme.BG_DARK, border_width=0)
        self.quality.pack(fill="x", pady=5)
        
        # Path
        ctk.CTkLabel(content, text="Save To", font=Theme.FONT_LABEL, text_color=Theme.SECONDARY).pack(anchor="w", padx=30, pady=(15, 5))
        self.path_btn = ctk.CTkButton(content, text="Select Folder", height=45, fg_color=Theme.INPUT_BG, hover_color=Theme.BG_DARK, command=self.select_folder)
        self.path_btn.pack(fill="x", padx=30, pady=(0, 30))
        self.download_folder = ""
        
        # Download Button
        self.download_btn = ctk.CTkButton(page, text="Start Download", height=60, corner_radius=12, fg_color=Theme.PRIMARY, text_color=Theme.BG_DARK, font=Theme.FONT_BUTTON, command=self.start_download)
        self.download_btn.grid(row=2, column=0, sticky="ew", pady=30)
        
        # Progress
        self.status_card = ctk.CTkFrame(page, fg_color=Theme.CARD_BG, corner_radius=12)
        self.status_card.grid(row=3, column=0, sticky="ew")
        self.progress_bar = ctk.CTkProgressBar(self.status_card, height=6, progress_color=Theme.PRIMARY, fg_color=Theme.BG_DARK)
        self.progress_bar.pack(fill="x", padx=25, pady=(20, 10))
        self.progress_bar.set(0)
        self.status_label = ctk.CTkLabel(self.status_card, text="Ready", font=("Segoe UI", 11), text_color=Theme.SECONDARY)
        self.status_label.pack(pady=(0, 20))
        
        return page

    def create_library_page(self):
        page = ctk.CTkFrame(self.container, fg_color="transparent")
        page.grid_columnconfigure(0, weight=1)
        page.grid_rowconfigure(1, weight=1)
        
        # Header Row with Clear Button
        header = ctk.CTkFrame(page, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        ctk.CTkLabel(header, text="Download History", font=Theme.FONT_TITLE, text_color=Theme.TEXT_MAIN).pack(side="left")
        ctk.CTkButton(header, text="Clear All", width=100, height=32, fg_color="#F43F5E", hover_color="#BE123C", command=self.clear_all_history).pack(side="right", pady=5)
        
        self.history_scroll = ctk.CTkScrollableFrame(page, fg_color=Theme.CARD_BG, corner_radius=15, border_width=1, border_color=Theme.INPUT_BG)
        self.history_scroll.grid(row=1, column=0, sticky="nsew")
        
        self.load_history_entries()
        return page

    def load_history_entries(self):
        # Clear existing
        for child in self.history_scroll.winfo_children():
            child.destroy()
            
        history = self.history_mgr.get_all()
        
        if not history:
            ctk.CTkLabel(self.history_scroll, text="No downloads yet.", text_color=Theme.TEXT_MUTED).pack(pady=40)
            return

        for entry in history:
            item = ctk.CTkFrame(self.history_scroll, fg_color=Theme.BG_DARK, corner_radius=10)
            item.pack(fill="x", padx=15, pady=8)
            
            # Info
            info_f = ctk.CTkFrame(item, fg_color="transparent")
            info_f.pack(side="left", fill="both", expand=True, padx=20, pady=10)
            
            ctk.CTkLabel(info_f, text=entry['title'], font=("Segoe UI Bold", 13), text_color=Theme.TEXT_MAIN, anchor="w").pack(fill="x")
            ctk.CTkLabel(info_f, text=f"{entry['date']} • {os.path.dirname(entry['path'])}", font=("Segoe UI", 10), text_color=Theme.TEXT_MUTED, anchor="w").pack(fill="x")
            
            # Actions
            btn_f = ctk.CTkFrame(item, fg_color="transparent")
            btn_f.pack(side="right", padx=15)
            
            ctk.CTkButton(btn_f, text="📂", width=40, height=35, fg_color=Theme.INPUT_BG, command=lambda p=entry['path']: self.open_folder(p)).pack(side="left", padx=5)
            ctk.CTkButton(btn_f, text="▶", width=40, height=35, fg_color=Theme.PRIMARY, text_color=Theme.BG_DARK, command=lambda p=entry['path']: self.play_file(p)).pack(side="left", padx=5)

    def open_folder(self, path):
        # Normalize and clean path
        path = os.path.normpath(path)
        folder = os.path.dirname(path)
        
        # Try to fix common character mismatches in folder name
        if not os.path.exists(folder):
            folder = folder.replace('|', '｜')
            
        if os.path.exists(folder):
            try:
                os.startfile(folder)
            except Exception as e:
                self.update_status(f"Error opening folder: {e}")
        else:
            self.update_status("Folder not found")

    def play_file(self, path):
        # Normalize and clean path
        path = os.path.normpath(path)
        
        # Try to fix common character mismatches
        if not os.path.exists(path):
            # Try replacing | with ｜
            alt_path = path.replace('|', '｜')
            if os.path.exists(alt_path):
                path = alt_path
            else:
                # Try finding the file with a different extension in the same folder
                folder = os.path.dirname(path)
                if not os.path.exists(folder):
                    folder = folder.replace('|', '｜')
                    
                if os.path.exists(folder):
                    base_name = os.path.splitext(os.path.basename(path))[0]
                    # Replace invalid chars in base_name for searching
                    search_name = base_name.replace('|', '｜')
                    
                    found = False
                    try:
                        for f in os.listdir(folder):
                            f_base, _ = os.path.splitext(f)
                            if f_base == search_name or f_base == base_name:
                                path = os.path.join(folder, f)
                                found = True
                                break
                    except Exception:
                        pass
                    
        if os.path.exists(path):
            try:
                os.startfile(path)
            except Exception as e:
                self.update_status(f"Error playing file: {e}")
        else:
            self.update_status("File not found")


    def clear_all_history(self):
        self.history_mgr.clear_history()
        self.load_history_entries()



    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.download_folder = folder
            self.path_btn.configure(text=folder)

    def start_download(self):
        url = self.url_entry.get()
        if not url: return
        if not self.download_folder: return
        self.download_btn.configure(state="disabled", text="Downloading...")
        self.downloader.download(url, self.download_folder, self.download_type.get(), self.quality.get())

    def update_progress(self, value):
        self.after(0, lambda: self.progress_bar.set(value))

    def update_status(self, text):
        self.after(0, lambda: self.status_label.configure(text=text))

    def on_complete(self, success, message, title=None, path=None, url=None):
        if success and title and path:
            self.history_mgr.add_entry(title, path, url)
            self.after(0, self.load_history_entries) # Ensure UI update happens on main thread
            
        self.after(0, lambda: self._finalize(success, message))

    def _finalize(self, success, message):
        self.download_btn.configure(state="normal", text="Start Download")
        self.progress_bar.set(0)
        self.status_label.configure(text=message)
        if success: self.url_entry.delete(0, "end")

    def enable_arabic_shortcuts(self, entry_widget):
        def paste(event):
            try:
                # Try getting the clipboard
                text = self.clipboard_get()
                # Insert at cursor position
                entry_widget.insert("insert", text)
                return "break"
            except:
                pass
        
        def copy(event):
            try:
                # Check if text is selected
                if entry_widget.select_present():
                    self.clipboard_clear()
                    self.clipboard_append(entry_widget.selection_get())
                return "break"
            except:
                pass
        
        def select_all(event):
            # Select all text
            entry_widget.select_range(0, "end")
            return "break"

        def cut(event):
            try:
                if entry_widget.select_present():
                    self.clipboard_clear()
                    self.clipboard_append(entry_widget.selection_get())
                    # Delete selected text
                    first = entry_widget.index("sel.first")
                    last = entry_widget.index("sel.last")
                    entry_widget.delete(first, last)
                return "break"
            except:
                pass

        # Handle shortcuts independently of keyboard language using Windows Keycodes
        # 86 = V, 67 = C, 88 = X, 65 = A
        def on_ctrl_key(event):
            if event.keycode == 86:
                return paste(event)
            elif event.keycode == 67:
                return copy(event)
            elif event.keycode == 88:
                return cut(event)
            elif event.keycode == 65:
                return select_all(event)
                
        entry_widget.bind("<Control-KeyPress>", on_ctrl_key)
