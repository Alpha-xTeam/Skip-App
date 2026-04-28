import PyInstaller.__main__
import os
import customtkinter
import sys

# تحديد المسارات
ctk_path = os.path.dirname(customtkinter.__file__)

# أوامر البناء الاحترافية
args = [
    'main.py',
    '--noconsole',
    '--onefile',
    '--name=SkipDownloader',
    # تضمين الكود المصدري
    '--add-data=src;src',
    # تضمين مكتبة customtkinter بالكامل مع ملفات الـ json والـ themes
    f'--add-data={ctk_path};customtkinter',
    # إجبار البرنامج على رؤية المكتبات المخفية
    '--hidden-import=customtkinter',
    '--hidden-import=yt_dlp',
    '--hidden-import=tkinter',
    f'--icon={os.path.abspath("src/ChatGPT_Image_Apr_28__2026__06_30_59_AM-removebg-preview.ico")}',
    '--clean',
]

# التحقق من وجود ffmpeg لضمه داخل الـ exe
if os.path.exists('bin/ffmpeg.exe'):
    args.append('--add-binary=bin/ffmpeg.exe;bin')
    print("Found ffmpeg.exe, bundling into executable...")

print("--- STARTING FINAL STANDALONE BUILD ---")
PyInstaller.__main__.run(args)
print("--- DONE! SEND THE EXE IN 'dist' FOLDER TO YOUR FRIEND ---")
