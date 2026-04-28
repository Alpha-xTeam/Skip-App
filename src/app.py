from gui.main_window import MainWindow
from core.downloader import YouTubeDownloader
import customtkinter as ctk

def main():
    # Set default appearance
    ctk.set_appearance_mode("dark")
    
    # Initialize Core
    downloader = YouTubeDownloader()
    
    # Initialize UI
    app = MainWindow(downloader)
    
    # Start app
    app.mainloop()

if __name__ == "__main__":
    main()
