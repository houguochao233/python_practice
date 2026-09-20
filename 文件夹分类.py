from pathlib import Path
import shutil
import sys

dry_run = "--dry-run" in sys.argv

files= Path(input(r"请输入要整理的目标文件夹路径：").strip("'").strip('"'))
extension_map = {
    # 对应 excel_dir (保留了你代码中的原分类归属)
    ".xlsx": "excel",
    ".xls": "excel",
    ".csv": "excel",
    ".docx": "excel",
    ".doc": "excel",
    # 对应 music_dir
    ".mp3": "music",
    ".mp4": "music",
    ".mkv": "music",
    # 对应 text_dir
    ".txt": "text",
    # 对应 img_dir
    ".jpg": "img",
    ".jpeg": "img",
    ".png": "img",
    ".gif": "img",
    ".webp": "img",
    # 对应 pdf_dir
    ".pdf": "pdf",
    # 对应 ppt_dir
    ".pptx": "ppt",
    ".ppt": "ppt",
    ".pps": "ppt",
    ".ppsx": "ppt",
    # 对应 zip_dir
    ".zip": "zip",
    ".rar": "zip",
    ".7z": "zip",
}

for file in files.iterdir():
    if not file.is_file():
         continue
    ext = file.suffix.lower()

    category = extension_map.get(ext)
    if not category:
        print(f"{ext}格式未被包含")
        continue

    target_dir = files / category
    if not target_dir.exists():
        if dry_run:
            print(f"{target_dir}已创建")
        else:
            target_dir.mkdir(parents = True,exist_ok = True)
            print(f"{target_dir}已创建")

    target_path = target_dir / file.name

    if target_path.exists:
        stem = file.stem
        suffix = file.suffix
        count = 1
        while target_path.exists():
            print(f"{file}有重名文件,进行编号处理")
            target_path = target_dir / f"{stem}_{count}{suffix}"
            count += 1

    if dry_run:
        print(f"{file}已移动到{target_path}")
    else:
        shutil.move(file,target_path)
        print(f"{file}已移动到{target_path}")
        
    
