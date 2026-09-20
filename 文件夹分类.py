from pathlib import Path
import shutil
import sys

dry_run = "--dry-run" in sys.argv

base_path= Path(input(r"请输入要整理的目标文件夹路径：").strip("'").strip('"'))
files = base_path
excel_dir = base_path / 'excel'
music_dir = base_path / 'music' 
text_dir = base_path / 'text'
img_dir = base_path / 'img'
pdf_dir = base_path / 'pdf'
ppt_dir = base_path / 'ppt'
zip_dir = base_path / 'zip'

for file in files.iterdir():
    if not file.is_file():
         continue
    ext = file.suffix.lower()
    if ext in ['.xlsx','.xls','.csv','.docx','doc']:
        target_dir = excel_dir
    elif ext in ['.mp3','.mp4','.mkv']:
            target_dir = music_dir
    elif ext in ['.txt']:
        target_dir = text_dir
    elif ext in['.jpg', '.jpeg', '.png', '.gif', '.webp']:
        target_dir = img_dir
    elif ext in ['.pdf']:
            target_dir = pdf_dir    
    elif ext in ['.pptx','.ppt','pps','ppsx']:
            target_dir = ppt_dir
    elif ext in ['.zip','.rar','.7z']:
            target_dir = zip_dir
    else:
        continue

    if not target_dir.exists():
        if dry_run:
            print(f"{target_dir}已创建")
        else:
            target_dir.mkdir(parents = True,exist_ok = True)
            print(f"{target_dir}已创建")

    target_path = target_dir / file.name
    if dry_run:
        print(f"{file}已移动到{target_path}")
    else:
        shutil.move(str(file),str(target_path))
        print(f"{file}已移动到{target_path}")
        
    
