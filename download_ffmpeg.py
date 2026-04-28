import urllib.request
import zipfile
import os
import shutil

def main():
    bin_dir = r"c:\Projects\Skip\bin"
    os.makedirs(bin_dir, exist_ok=True)
    zip_path = os.path.join(bin_dir, "ffmpeg.zip")
    
    print("Downloading ffmpeg (this might take a minute)...")
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    
    # Custom headers to avoid being blocked
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    
    with urllib.request.urlopen(req) as response, open(zip_path, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
        
    print("Extracting...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(bin_dir)
        
    print("Finding ffmpeg.exe...")
    for root, dirs, files in os.walk(bin_dir):
        if "ffmpeg.exe" in files:
            shutil.copy(os.path.join(root, "ffmpeg.exe"), os.path.join(bin_dir, "ffmpeg.exe"))
            print("ffmpeg.exe found and copied.")
            break
            
    # Cleanup
    print("Cleaning up temporary files...")
    os.remove(zip_path)
    for item in os.listdir(bin_dir):
        item_path = os.path.join(bin_dir, item)
        if os.path.isdir(item_path) and item.startswith("ffmpeg-"):
            shutil.rmtree(item_path)
            
    print("ffmpeg setup successfully!")

if __name__ == "__main__":
    main()
