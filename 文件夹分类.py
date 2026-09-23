from pathlib import Path
import shutil
import sys

extension_map = {
    # Excel
    ".xlsx": "excel",
    ".xls": "excel",
    ".csv": "excel",

    # Word
    ".docx": "word",
    ".doc": "word",

    # PowerPoint
    ".pptx": "ppt",
    ".ppt": "ppt",
    ".pps": "ppt",
    ".ppsx": "ppt",

    # Text
    ".txt": "text",
    ".md": "text",
    ".log": "text",

    # Image
    ".jpg": "img",
    ".jpeg": "img",
    ".png": "img",
    ".gif": "img",
    ".webp": "img",
    ".bmp": "img",
    ".svg": "img",

    # Audio
    ".mp3": "audio",
    ".wav": "audio",
    ".flac": "audio",

    # Video
    ".mp4": "video",
    ".mkv": "video",
    ".avi": "video",
    ".mov": "video",

    # PDF
    ".pdf": "pdf",

    # Archive
    ".zip": "zip",
    ".rar": "zip",
    ".7z": "zip",
}

def get_unique(target_dir,file): #判断文件重复，并返回带编号重复文件路径
    target_path = target_dir / file.name #样本将要移入的目标路径
    if not target_path.exists():
        return target_path

    count = 1

    while True:
        target_path = target_dir / f"{file.stem}_{count}{file.suffix}"

        if not target_path.exists(): #判断是否重名
            return target_path    
        count += 1


def move_file(file,target_dir,dry_run=False):
    if not target_dir.exists():
        if dry_run:
            print(f"[预览]{target_dir}已创建")
        else:
            target_dir.mkdir(parents = True,exist_ok = True)
            print(f"{target_dir}已创建")

    target_path = get_unique(target_dir,file)

    if dry_run:
        print(f"[预览]{file}已移动到{target_path}")
    else:
        shutil.move(file,target_path)
        print(f"{file}已移动到{target_path}")
    return True

def orginaze_files(files,extension_map,dry_run = False):
    stats = {}
    
    for file in files.iterdir():
        if not file.is_file():
            continue
        ext = file.suffix.lower()     #获取后缀

        category = extension_map.get(ext)#样本是否在词典中
        if not category:
            print(f"{ext}格式未被包含")
            continue

        target_dir = files / category#想要将样本移入的文件夹路径
        success = move_file(file,target_dir)
        if success :
            stats[category] = stats.get(category,0)+1

    return stats

def main():
    dry_run = "--dry-run" in sys.argv #测试代码
    files= Path(input(r"请输入要整理的目标文件夹路径：").strip("'").strip('"'))
    if not files.exists():
        print(f"{files}不存在")
        return
    if not files.is_dir():
        print(f"{files}不是文件夹")
        return

    total = 0

    stats = orginaze_files(files,extension_map,dry_run=False)
    for category,count in stats.items():
        print(f"{category} : {count}份")
        total += count
    print(f"一共{total}份")

if __name__ == "__main__":
    main()
     
    
