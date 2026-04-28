import yt_dlp
import os
import threading
import sys

def get_ffmpeg_path():
    if getattr(sys, 'frozen', False):
        # PyInstaller temp folder
        base_path = sys._MEIPASS
        ffmpeg_bin = os.path.join(base_path, 'bin', 'ffmpeg.exe')
        if os.path.exists(ffmpeg_bin):
            return ffmpeg_bin
            
    # Local project bin folder
    local_bin = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'bin', 'ffmpeg.exe')
    if os.path.exists(local_bin):
        return local_bin
        
    return 'ffmpeg' # Fallback to system-wide PATH

class YouTubeDownloader:
    def __init__(self):
        self.is_downloading = False
        self.progress_callback = None
        self.status_callback = None
        self.complete_callback = None

    def download(self, url, folder, download_type, quality):
        if self.is_downloading:
            return
        
        self.is_downloading = True
        
        thread = threading.Thread(target=self._run_download, args=(url, folder, download_type, quality))
        thread.daemon = True
        thread.start()

    def _run_download(self, url, folder, download_type, quality):
        try:
            ydl_opts = {
                'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
                'progress_hooks': [self._progress_hook],
                'noplaylist': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'ffmpeg_location': get_ffmpeg_path(),
                'restrictfilenames': True,
                'windows_filenames': True,
            }
            
            if "Audio" in download_type:
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                if quality == "Best":
                    ydl_opts['format'] = 'bestvideo+bestaudio/best'
                    ydl_opts['merge_output_format'] = 'mp4'
                else:
                    height = quality.replace("p", "")
                    ydl_opts['format'] = f'bestvideo[height<={height}]+bestaudio/best'
                    ydl_opts['merge_output_format'] = 'mp4'
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'Unknown Title')
                
                # Get the real final path safely
                base_name = ydl.prepare_filename(info)
                if "Audio" in download_type:
                    final_path = os.path.splitext(base_name)[0] + '.mp3'
                else:
                    final_path = base_name
            
            if self.complete_callback:
                self.complete_callback(True, "Download completed!", title, final_path, url)
                
        except Exception as e:
            if self.complete_callback:
                self.complete_callback(False, f"Error: {str(e)}", None, None, None)
        finally:
            self.is_downloading = False

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            p = 0
            if 'total_bytes' in d:
                p = d['downloaded_bytes'] / d['total_bytes']
            elif 'total_bytes_estimate' in d:
                p = d['downloaded_bytes'] / d['total_bytes_estimate']
            
            if self.progress_callback:
                self.progress_callback(p)
            
            if self.status_callback:
                percent = int(p * 100)
                self.status_callback(f"Downloading: {percent}%")
                
        elif d['status'] == 'finished':
            if self.status_callback:
                self.status_callback("Processing final file...")
