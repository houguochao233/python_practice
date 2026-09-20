from pathlib import Path
import shutil
import sys

dry_run = "--dry-run" in sys.argv

files = Path(r"E:\python\garbage")

for file in files.iterdir():
    if file.suffix == '.xlsx':
        if Path(r"E:\python\excel").exists():
            if dry_run:
                 print(f"{file.name}移动完成")
            else:
                shutil.move(f"{file}",r"E:\python\excel")
                print(f"{file.name}移动完成")
        else:
            if dry_run:
                 print("文件夹创建完成")
                 print(f"{file.name}移动完成")
            else:
                Path(r"E:\python\excel").mkdir(parents=True,exist_ok=True),
                print("文件夹创建完成")
                shutil.move(f"{file}",r"E:\python\excel")
                print(f"{file.name}移动完成")
    elif file.suffix == '.txt':
            if Path(r"E:\python\text").exists():
                if dry_run:
                     print(f"{file.name}移动完成")
                else:
                    shutil.move(f"{file}",r"E:\python\text")
                    print(f"{file.name}移动完成")
            else:
                if dry_run:
                     print("文件夹创建完成")
                     print(f"{file.name}移动完成")
                else:
                    Path(r"E:\python\text").mkdir(parents=True,exist_ok=True)
                    print("文件夹创建完成")
                    shutil.move(f"{file}",r"E:\python\text")        
                    print(f"{file.name}移动完成")
    
