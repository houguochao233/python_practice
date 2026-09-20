from pathlib import Path
import shutil
import sys

dry_run = "--dry-run" in sys.argv

files = Path(r"E:\python\garbage")
excel_dir = Path(r"E:\python\excel")
text_dir = Path(r"E:\python\text")
picture_dir = Path(r"E:\python\picture") 

for file in files.iterdir():
    if not file.is_file():
         continue
    ext = file.suffix.lower()
    if ext == '.xlsx':
        target_dir = excel_dir
    elif ext == '.txt':
        target_dir = text_dir
    elif ext in['.jpg' or '.jpeg' or '.png' or '.gif']:
        target_dir = picture_dir
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
        
    
