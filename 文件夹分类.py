from pathlib import Path
import shutil
import sys

try:
    from tkinter import END, SINGLE, StringVar, BooleanVar
    from tkinter import filedialog, messagebox
    from tkinter import ttk
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    # 命令行模式仍可以使用；双击打开窗口时会提示安装 tkinterdnd2
    TkinterDnD = None

extension_map = {
    ".xlsx": "excel", ".xls": "excel", ".csv": "excel",
    ".docx": "word", ".doc": "word",
    ".pptx": "ppt", ".ppt": "ppt", ".pps": "ppt", ".ppsx": "ppt",
    ".txt": "text", ".md": "text", ".log": "text",
    ".jpg": "img", ".jpeg": "img", ".png": "img", ".gif": "img",
    ".webp": "img", ".bmp": "img", ".svg": "img",
    ".mp3": "audio", ".wav": "audio", ".flac": "audio",
    ".mp4": "video", ".mkv": "video", ".avi": "video", ".mov": "video",
    ".pdf": "pdf",
    ".zip": "zip", ".rar": "zip", ".7z": "zip",
}


def clean_path_text(value):
    return value.strip().strip('"').strip("'")


def get_unique(target_dir, file):
    """返回不会覆盖已有文件的目标路径。"""
    target_path = target_dir / file.name
    # 文件本来就在目标目录时，不要给它重新命名或移动
    if file.parent.resolve() == target_dir.resolve():
        return file
    if not target_path.exists():
        return target_path

    count = 1
    while True:
        target_path = target_dir / f"{file.stem}_{count}{file.suffix}"
        if not target_path.exists():
            return target_path
        count += 1


def move_file(file, target_dir, dry_run=False):
    target_path = get_unique(target_dir, file)

    if target_path == file:
        print(f"跳过：{file} 已经在 {target_dir.name} 文件夹中")
        return False

    if dry_run:
        print(f"[预览] {file} -> {target_path}")
        return True

    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.move(str(file), str(target_path))
    print(f"{file} -> {target_path}")
    return True


def organize_folder(folder, dry_run=False):
    """整理一个文件夹的直接文件，不递归整理子文件夹。"""
    stats = {}
    for file in list(folder.iterdir()):
        if not file.is_file():
            continue

        ext = file.suffix.lower()
        category = extension_map.get(ext)
        if not category:
            print(f"跳过：{file.name}（{ext or '无扩展名'}格式未被包含）")
            continue

        target_dir = folder / category
        if move_file(file, target_dir, dry_run):
            stats[category] = stats.get(category, 0) + 1
    return stats


def resolve_folders(targets):
    """文件按其所在目录整理；文件夹按该文件夹整理。"""
    folders = []
    for target in targets:
        target = Path(target).expanduser()
        if not target.exists():
            continue
        folders.append(target.parent if target.is_file() else target)

    unique_folders = []
    seen = set()
    for folder in folders:
        key = str(folder.resolve()).lower()
        if key not in seen:
            seen.add(key)
            unique_folders.append(folder)
    return unique_folders


def parse_dropped_paths(root, data):
    """正确解析 Windows 拖拽事件中的带空格路径和多路径。"""
    return [Path(clean_path_text(item)) for item in root.tk.splitlist(data)]


def launch_gui():
    if TkinterDnD is None:
        print("缺少 tkinterdnd2，请先执行：python -m pip install tkinterdnd2")
        return

    root = TkinterDnD.Tk()
    root.title("文件夹分类工具")
    root.geometry("760x560")
    root.minsize(620, 420)

    paths = []
    status = StringVar(value="把文件或文件夹拖到下面的区域")
    dry_run = BooleanVar(value=False)

    title = ttk.Label(root, text="文件夹分类工具", font=("Microsoft YaHei UI", 18, "bold"))
    title.pack(pady=(16, 4))

    hint = ttk.Label(
        root,
        text="拖入文件：整理它所在的文件夹    |    拖入文件夹：整理该文件夹中的文件",
    )
    hint.pack(pady=(0, 10))

    drop_area = ttk.Label(
        root,
        text="将文件或文件夹拖到这里",
        anchor="center",
        relief="solid",
        padding=28,
    )
    drop_area.pack(fill="x", padx=24, pady=8)

    list_frame = ttk.Frame(root)
    list_frame.pack(fill="both", expand=True, padx=24, pady=8)

    scrollbar = ttk.Scrollbar(list_frame, orient="vertical")
    path_list = __import__("tkinter").Listbox(
        list_frame,
        height=10,
        selectmode=SINGLE,
        yscrollcommand=scrollbar.set,
        font=("Consolas", 10),
    )
    scrollbar.config(command=path_list.yview)
    path_list.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def refresh_list():
        path_list.delete(0, END)
        for index, path in enumerate(paths, 1):
            path_list.insert(END, f"{index}. {path}")
        status.set(f"已获取 {len(paths)} 个路径")

    def add_paths(new_paths):
        for path in new_paths:
            path = Path(path)
            if path.exists() and path not in paths:
                paths.append(path)
        refresh_list()

    def on_drop(event):
        add_paths(parse_dropped_paths(root, event.data))

    def choose_paths():
        selected = filedialog.askopenfilenames(title="选择文件（可多选）")
        if selected:
            add_paths(selected)

    def choose_folder():
        selected = filedialog.askdirectory(title="选择文件夹")
        if selected:
            add_paths([selected])

    def copy_selected():
        selection = path_list.curselection()
        if not selection:
            messagebox.showinfo("提示", "请先在列表中选择一个路径")
            return
        value = str(paths[selection[0]])
        root.clipboard_clear()
        root.clipboard_append(value)
        root.update()
        status.set("已复制选中路径：" + value)

    def copy_all():
        if not paths:
            messagebox.showinfo("提示", "当前没有路径")
            return
        value = "\n".join(str(path) for path in paths)
        root.clipboard_clear()
        root.clipboard_append(value)
        root.update()
        status.set(f"已复制 {len(paths)} 个路径")

    def clear_paths():
        paths.clear()
        refresh_list()

    def organize_selected():
        if not paths:
            messagebox.showinfo("提示", "请先拖入文件或文件夹")
            return

        folders = resolve_folders(paths)
        if dry_run.get():
            message = "当前是预览模式，不会真正移动文件。\n\n是否开始预览？"
        else:
            message = "将真正移动文件，建议先预览确认。\n\n是否继续？"
        if not messagebox.askyesno("确认整理", message):
            return

        all_stats = {}
        for folder in folders:
            stats = organize_folder(folder, dry_run=dry_run.get())
            for category, count in stats.items():
                all_stats[category] = all_stats.get(category, 0) + count

        total = sum(all_stats.values())
        result = "、".join(f"{category}: {count}" for category, count in all_stats.items())
        status.set(f"完成：共处理 {total} 个文件" + (f"（{result}）" if result else ""))
        messagebox.showinfo("整理完成", status.get())

    drop_area.drop_target_register(DND_FILES)
    drop_area.dnd_bind("<<Drop>>", on_drop)
    path_list.drop_target_register(DND_FILES)
    path_list.dnd_bind("<<Drop>>", on_drop)

    button_frame = ttk.Frame(root)
    button_frame.pack(fill="x", padx=24, pady=(2, 8))
    ttk.Button(button_frame, text="选择文件", command=choose_paths).pack(side="left", padx=(0, 6))
    ttk.Button(button_frame, text="选择文件夹", command=choose_folder).pack(side="left", padx=6)
    ttk.Button(button_frame, text="复制选中地址", command=copy_selected).pack(side="left", padx=6)
    ttk.Button(button_frame, text="复制全部地址", command=copy_all).pack(side="left", padx=6)
    ttk.Button(button_frame, text="清空", command=clear_paths).pack(side="right")

    options = ttk.Frame(root)
    options.pack(fill="x", padx=24, pady=4)
    ttk.Checkbutton(options, text="预览模式（勾选后只查看，不移动）", variable=dry_run).pack(side="left")
    ttk.Button(options, text="开始整理", command=organize_selected).pack(side="right")

    ttk.Label(root, textvariable=status, foreground="#555555").pack(fill="x", padx=24, pady=(4, 14))
    root.mainloop()


def main_cli():
    dry_run = "--dry-run" in sys.argv
    raw_paths = [item for item in sys.argv[1:] if not item.startswith("--")]
    if not raw_paths:
        print("没有传入路径，正在打开拖拽窗口……")
        launch_gui()
        return

    targets = [Path(clean_path_text(item)) for item in raw_paths]
    folders = resolve_folders(targets)
    if not folders:
        print("没有找到有效的文件或文件夹。")
        return

    all_stats = {}
    for folder in folders:
        print(f"正在整理：{folder}")
        stats = organize_folder(folder, dry_run=dry_run)
        for category, count in stats.items():
            all_stats[category] = all_stats.get(category, 0) + count

    print("整理完成：")
    for category, count in all_stats.items():
        print(f"{category}: {count} 份")
    print(f"一共处理 {sum(all_stats.values())} 份文件")


if __name__ == "__main__":
    main_cli()

