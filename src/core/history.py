import json
import os
import sys
from datetime import datetime

class HistoryManager:
    def __init__(self):
        # Determine a persistent storage location
        if getattr(sys, 'frozen', False):
            # If running as .exe, save in AppData to avoid losing data in Temp folders
            base_dir = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), "SkipDownloader")
        else:
            # If running as script, keep it in the project folder
            base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")
            
        self.history_file = os.path.join(base_dir, "history.json")
        self._ensure_file()

    def _ensure_file(self):
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def add_entry(self, title, path, url):
        entry = {
            "title": title,
            "path": path,
            "url": url,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        history = self.get_all()
        history.insert(0, entry) # Add to top
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=4, ensure_ascii=False)

    def get_all(self):
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []

    def clear_history(self):
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump([], f)
