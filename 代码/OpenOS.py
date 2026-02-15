import tkinter as tk
import os, time, subprocess
from tkinter import messagebox, filedialog, ttk
from chardet import detect as chardetect
from datetime import datetime
class TrangeBar:
    def __init__(self, master, length=125, maximum=100):
        self.master = master
        self.trange_bar = ttk.Progressbar(self.master, orient="horizontal", length=length, mode="determinate", maximum=maximum)
        self.trange_bar_value = 0
    def pack(self, padx=0, pady=0, side=tk.TOP):
        self.trange_bar.pack(padx=padx, pady=pady, side=side)
    def update(self, update_value):
        self.trange_bar_value = update_value
        self.trange_bar_value %= self.trange_bar["maximum"]
        if (self.trange_bar["maximum"] + update_value) <= self.trange_bar["maximum"]:
            self.trange_bar['value'] = self.trange_bar["maximum"] + update_value
        else:
            self.trange_bar['value'] = self.trange_bar["maximum"]
    def back(self, update_value):
        self.trange_bar_value = update_value
        self.trange_bar_value %= self.trange_bar["maximum"]
        if (self.trange_bar["maximum"] - update_value) >= 0:
            self.trange_bar['value'] = self.trange_bar["maximum"] - update_value
        else:
            self.trange_bar['value'] = self.trange_bar["maximum"]
class Fileopen():
    def read(self, path):
        with open(path, "rb") as f:
            raw_data = f.read()
            result = chardetect(raw_data)
            encoding = result['encoding']
            with open(path, "r", encoding=encoding) as f:
                return f.read()
    def write(self, path, content):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    def select_file_read(self, title="选择文件"):
        path = filedialog.askopenfilename(initialdir="/", title=title)
        if not path:
            exit()
        return self.read(path)
    def select_file_write(self, content, title="选择文件"):
        path = filedialog.asksaveasfilename(initialdir="/", title=title)
        if not path:
            exit()
        self.write(path, content)
    def select_file_save(self, content, title="选择文件"):
        self.select_file_write(content, title)
    def select_folder(self, title="选择文件夹"):
        path = filedialog.askdirectory(initialdir="/", title=title)
        if not path:
            exit()
        return path
    def select_folder_directory(self, title="选择文件夹"):
        path = filedialog.askdirectory(initialdir="/", title=title)
        if not path:
            exit()
        return path + "/"
    def create_file(self, path, content):
        self.write(path, content)
    def create_blank_file(self, path):
        self.write(path, "")
    def create_folder(self, path):
        os.makedirs(path)
xos_path = Fileopen().select_folder_directory(title="选择XOS文件夹")
xos_name, xos_key, xos_version, xos_password, xos_key_canuse = Fileopen().read(xos_path + "os_name.txt"), Fileopen().read(xos_path + "os_key.txt"), Fileopen().read(xos_path + "os_version.txt"), Fileopen().read(xos_path + "os_password.txt"), Fileopen().read(xos_path + "os_key_canuse.txt")
unlock = tk.Tk()
unlock.title(xos_name)
unlock.resizable(False, False)
unlock.geometry("200x100")
if xos_password != "":
    unlock_label = tk.Label(unlock, text="请输入解锁密码")
    unlock_label.pack(pady=10, side=tk.TOP)
    unlock_entry = tk.Entry(unlock)
    unlock_entry.pack(pady=10, side=tk.TOP)
    unlock_entry.focus()
    unlock_button = None
    unlock.protocol("WM_DELETE_WINDOW", lambda: exit())
    unlock.bind("<Return>", lambda event: unlock.destroy() if unlock_entry.get() == xos_password else messagebox.showerror("错误", "密码错误"))
    unlock.mainloop()
else:
    unlock_label = tk.Label(unlock, text="点击按钮解锁")
    unlock_label.pack(pady=10, side=tk.TOP)
    def on_closing():
        exit()
    unlock.protocol("WM_DELETE_WINDOW", on_closing)
    unlock_button = tk.Button(unlock, text="解锁", command=lambda: unlock.destroy())
    unlock_button.pack(pady=10, side=tk.TOP)
    unlock.mainloop()
del unlock_label, unlock_button
window = tk.Tk()
window.title(xos_name)
window.geometry("800x600")
window.configure(bg="darkblue")
fullscreen = False
def toggle_fullscreen(event=None):
    global fullscreen
    fullscreen = not fullscreen
    window.attributes("-fullscreen", fullscreen)
window.bind("<F11>", toggle_fullscreen)
desktop_path = xos_path + "files/Desktop/"
selected_files = clipboard_files = []
clipboard_action, file_id_map = None, {}
desktop_frame = tk.Frame(window, bg="darkblue")
desktop_frame.pack(fill=tk.BOTH, expand=True)
desktop_canvas = tk.Canvas(desktop_frame, bg="darkblue", highlightthickness=0)
desktop_canvas.pack(fill=tk.BOTH, expand=True)
def get_file_icon(filename):
    if os.path.isdir(filename):
        return "📁"
    ext = os.path.splitext(filename)[1].lower()
    icon_map = {
        ".txt": "📄",
        ".py": "🐍",
        ".rb": "💎",
        ".js": "📜",
        ".html": "🌐",
        ".css": "🎨",
        ".json": "📋",
        ".md": "📝",
        ".pdf": "📕",
        ".doc": "📘",
        ".docx": "📘",
        ".xls": "📗",
        ".xlsx": "📗",
        ".ppt": "📙",
        ".pptx": "📙",
        ".jpg": "🖼️",
        ".jpeg": "🖼️",
        ".png": "🖼️",
        ".gif": "🖼️",
        ".mp3": "🎵",
        ".mp4": "🎬",
        ".avi": "🎬",
        ".zip": "📦",
        ".rar": "📦",
        ".exe": "⚙️",
        ".bat": "💻",
        ".sh": "💻",
        ".xsa": "💻"
    }
    return icon_map.get(ext, "📄")
def refresh_desktop():
    desktop_canvas.delete("all")
    selected_files.clear()
    file_id_map.clear()
    if not os.path.exists(desktop_path):
        os.makedirs(desktop_path)
    try:
        items = sorted(os.listdir(desktop_path))
        x, y = 20, 20
        max_width = 100
        for item in items:
            item_path = os.path.join(desktop_path, item)
            icon = get_file_icon(item_path)
            file_id = f"file_{len(file_id_map)}"
            file_id_map[file_id] = item_path
            desktop_canvas.create_text(x + 30, y, text=icon, font=("Arial", 32), tags=("icon", file_id))
            desktop_canvas.create_text(x + 30, y + 40, text=item, fill="white", font=("Arial", 10), tags=("text", file_id))
            desktop_canvas.tag_bind(file_id, "<Button-1>", lambda e, fid=file_id: on_file_click(e, fid))
            desktop_canvas.tag_bind(file_id, "<Double-Button-1>", lambda e, fid=file_id: open_file(file_id_map[fid]))
            desktop_canvas.tag_bind(file_id, "<Alt-Double-Button-1>", lambda e, fid=file_id, name=item: show_file_properties(file_id_map[fid], item))
            desktop_canvas.tag_bind(file_id, "<Button-3>", lambda e, fid=file_id, name=item: show_file_context_menu(e, fid, name))
            x += max_width
            if x > window.winfo_width() - max_width:
                x = 20
                y += 80
    except Exception as e:
        messagebox.showerror("错误", f"无法读取桌面: {e}")
def on_file_click(event, file_id):
    file_path = file_id_map[file_id]
    shift_pressed = (event.state & 0x0001) != 0 or (event.state & 1) != 0
    if shift_pressed:
        if file_path not in selected_files:
            selected_files.append(file_path)
            highlight_file(file_id, True)
    else:
        for fid in file_id_map.keys():
            highlight_file(fid, False)
        selected_files.clear()
        selected_files.append(file_path)
        highlight_file(file_id, True)
def highlight_file(file_id, highlight):
    text_items = desktop_canvas.find_withtag(f"text&&{file_id}")
    if highlight:
        for item in text_items:
            desktop_canvas.itemconfig(item, fill="yellow")
    else:
        for item in text_items:
            desktop_canvas.itemconfig(item, fill="white")
def show_file_context_menu(event, file_id, file_name):
    file_path = file_id_map[file_id]
    context_menu = tk.Menu(window, tearoff=0)
    context_menu.add_command(label="打开", command=lambda: open_file(file_path))
    context_menu.add_command(label="重命名", command=lambda: rename_file(file_path, file_name))
    context_menu.add_command(label="删除", command=lambda: delete_files([file_path]))
    context_menu.add_separator()
    context_menu.add_command(label="属性", command=lambda: show_properties(file_path))
    try:
        context_menu.tk_popup(event.x_root, event.y_root)
    finally:
        context_menu.grab_release()
def show_desktop_context_menu(event):
    context_menu = tk.Menu(window, tearoff=0)
    create_menu = tk.Menu(context_menu, tearoff=0)
    create_menu.add_command(label="文本文档", command=lambda: create_file("txt"))
    create_menu.add_command(label="Python文件", command=lambda: create_file("py"))
    create_menu.add_command(label="Ruby文件", command=lambda: create_file("rb"))
    create_menu.add_command(label="HTML文件", command=lambda: create_file("html"))
    create_menu.add_command(label="JSON文件", command=lambda: create_file("json"))
    create_menu.add_command(label="文件夹", command=lambda: create_folder())
    context_menu.add_cascade(label="新建", menu=create_menu)
    context_menu.add_command(label="在此处打开终端", command=lambda: open_terminal())
    context_menu.add_separator()
    context_menu.add_command(label="刷新", command=refresh_desktop)
    try:
        context_menu.tk_popup(event.x_root, event.y_root)
    finally:
        context_menu.grab_release()
def open_file(file_path):
    protected_files = ["os_key.txt", "os_key_canuse.txt", "os_password.txt", "os_name.txt", "os_version.txt"]
    file_name = os.path.basename(file_path)
    if file_name in protected_files:
        messagebox.showerror("错误", f"无法打开系统文件: {file_name}")
        return
    if "apps" in file_path:
        messagebox.showerror("错误", "无法打开apps文件夹")
        return
    try:
        if os.path.isdir(file_path):
            messagebox.showinfo("提示", "文件夹功能开发中...")
        elif file_path.endswith(".xsa"):
            if os.path.basename(file_path) == "PowerShell.xsa":
                subprocess.Popen(["start", "PowerShell"], shell=True)
            else:
                with open(file_path, 'rb') as f:
                    raw_data = f.read()
                    result = chardetect(raw_data)
                    encoding = result['encoding']
                    content = raw_data.decode(encoding)
                os.system(content)
        else:
            os.startfile(file_path)
    except Exception as e:
        messagebox.showerror("错误", f"无法打开文件: {e}")
def rename_file(file_path, old_name):
    readonly_files = ["os_key.txt", "os_key_canuse.txt", "os_password.txt", "os_name.txt", "os_version.txt"]
    readonly_folders = ["Desktop", "files", "apps"]
    if old_name in readonly_files:
        messagebox.showerror("错误", f"无法重命名系统文件: {old_name}")
        return
    if old_name in readonly_folders:
        messagebox.showerror("错误", f"无法重命名系统文件夹: {old_name}")
        return
    new_name = tk.simpledialog.askstring("重命名", "请输入新名称:", initialvalue=old_name)
    if new_name and new_name != old_name:
        try:
            new_path = os.path.join(os.path.dirname(file_path), new_name)
            os.rename(file_path, new_path)
            refresh_desktop()
        except Exception as e:
            messagebox.showerror("错误", f"重命名失败: {e}")
def delete_files(file_paths):
    protected_folders = ["Desktop", "files", "apps"]
    protected_files = ["os_key.txt", "os_key_canuse.txt", "os_password.txt", "os_name.txt", "os_version.txt"]
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        if os.path.isdir(file_path) and file_name in protected_folders:
            messagebox.showerror("错误", f"无法删除系统文件夹: {file_name}")
            return
        if file_name in protected_files:
            messagebox.showerror("错误", f"无法删除系统文件: {file_name}")
            return
    result = messagebox.askyesno("确认", f"确定要删除选中的 {len(file_paths)} 个文件吗？")
    if result:
        for file_path in file_paths:
            try:
                if os.path.isdir(file_path):
                    os.rmdir(file_path)
                else:
                    os.remove(file_path)
            except Exception as e:
                messagebox.showerror("错误", f"删除 {os.path.basename(file_path)} 失败: {e}")
        refresh_desktop()
def show_properties(file_path):
    try:
        size = os.path.getsize(file_path)
        mtime = os.path.getmtime(file_path)
        mtime_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
        if os.path.isdir(file_path):
            file_type = "文件夹"
        else:
            file_type = "文件"
        info = f"名称: {os.path.basename(file_path)}\n类型: {file_type}\n大小: {size} 字节\n修改时间: {mtime_str}"
        messagebox.showinfo("属性", info)
    except Exception as e:
        messagebox.showerror("错误", f"无法获取属性: {e}")
def create_file(extension):
    filename = tk.simpledialog.askstring("新建文件", f"请输入文件名 (.{extension}):")
    if filename:
        if not filename.endswith(f".{extension}"):
            filename += f".{extension}"
        file_path = os.path.join(desktop_path, filename)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("")
            refresh_desktop()
        except Exception as e:
            messagebox.showerror("错误", f"创建文件失败: {e}")
def create_folder():
    foldername = tk.simpledialog.askstring("新建文件夹", "请输入文件夹名称:")
    if foldername:
        folder_path = os.path.join(desktop_path, foldername)
        try:
            os.makedirs(folder_path)
            refresh_desktop()
        except Exception as e:
            messagebox.showerror("错误", f"创建文件夹失败: {e}")
def open_terminal():
    try:
        subprocess.Popen(["start", "cmd"], shell=True, cwd=desktop_path)
    except Exception as e:
        messagebox.showerror("错误", f"无法打开终端: {e}")
def copy_files(file_paths):
    global clipboard_files, clipboard_action
    clipboard_files = file_paths.copy()
    clipboard_action = "copy"
def cut_files(file_paths):
    global clipboard_files, clipboard_action
    clipboard_files = file_paths.copy()
    clipboard_action = "cut"
def show_file_properties(file_path, file_name):
    """显示文件属性"""
    try:
        if os.path.exists(file_path):
            stat_info = os.stat(file_path)
            file_type = "文件夹" if os.path.isdir(file_path) else "文件"
            size = stat_info.st_size
            if os.path.isdir(file_path):
                size = f"{len(os.listdir(file_path))} 项"
            else:
                size = f"{size} 字节"
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stat_info.st_ctime))
            modify_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stat_info.st_mtime))
            info = f"名称: {file_name}\n"
            info += f"类型: {file_type}\n"
            info += f"位置: {os.path.dirname(file_path)}\n"
            info += f"大小: {size}\n"
            info += f"创建时间: {create_time}\n"
            info += f"修改时间: {modify_time}\n"
            messagebox.showinfo("属性", info)
        else:
            messagebox.showerror("错误", "文件不存在")
    except Exception as e:
        messagebox.showerror("错误", f"无法获取文件属性: {e}")
def open_file_location(file_path):
    """打开文件所在位置"""
    try:
        folder_path = os.path.dirname(file_path)
        subprocess.Popen(["explorer", folder_path])
    except Exception as e:
        messagebox.showerror("错误", f"无法打开文件位置: {e}")
def paste_files():
    global clipboard_files, clipboard_action
    if not clipboard_files:
        return
    for src_path in clipboard_files:
        src_name = os.path.basename(src_path)
        dst_path = os.path.join(desktop_path, src_name)
        try:
            if clipboard_action == "copy":
                if os.path.isdir(src_path):
                    os.system(f'xcopy "{src_path}" "{dst_path}" /E /I /Y')
                else:
                    shutil.copy2(src_path, dst_path)
            elif clipboard_action == "cut":
                # 先复制再删除，避免文件锁定问题
                if os.path.isdir(src_path):
                    os.system(f'xcopy "{src_path}" "{dst_path}" /E /I /Y')
                    import shutil
                    shutil.rmtree(src_path)
                else:
                    shutil.copy2(src_path, dst_path)
                    os.remove(src_path)
        except Exception as e:
            messagebox.showerror("错误", f"粘贴 {src_name} 失败: {e}")
    refresh_desktop()
    clipboard_files.clear()
    clipboard_action = None
def on_key_press(event):
    if event.keysym == "Delete":
        if selected_files:
            delete_files(selected_files)
    elif event.state & 0x0004 and event.keysym.lower() == "c":
        if selected_files:
            copy_files(selected_files)
    elif event.state & 0x0004 and event.keysym.lower() == "x":
        if selected_files:
            cut_files(selected_files)
    elif event.state & 0x0004 and event.keysym.lower() == "v":
        paste_files()
    elif event.keysym == "Return":
        if selected_files:
            for file_path in selected_files:
                open_file(file_path)
window.bind("<Key>", on_key_press)
desktop_canvas.bind("<Button-3>", show_desktop_context_menu)
window.after(100, refresh_desktop)
buttom = tk.Frame(window)
buttom.pack(side=tk.BOTTOM, fill=tk.X)
left_buttom_menu_button = tk.Menubutton(buttom, text="菜单", direction="above")
left_buttom_menu_button.pack(side=tk.LEFT, padx=10, pady=10, anchor="w")
left_buttom_menu = tk.Menu(left_buttom_menu_button, tearoff=0)
left_buttom_menu_button.config(menu=left_buttom_menu)
left_buttom_menu.add_command(label="关机", command=lambda: window.destroy())
def open_file_browser():
    current_path = xos_path + "files/"
    file_browser = tk.Toplevel(window)
    file_browser.title("文件资源管理器")
    file_browser.geometry("600x400")
    browser_selected = []
    browser_clipboard_files = []
    browser_clipboard_action = None
    def get_display_path(path):
        if path.startswith(xos_path):
            return "PC/" + path[len(xos_path):]
        return path
    path_label = tk.Label(file_browser, text="当前位置: " + get_display_path(current_path))
    path_label.pack(pady=5, anchor="w")
    file_listbox = tk.Listbox(file_browser, selectmode=tk.EXTENDED)
    file_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    display_name_map = {}
    def update_file_list():
        file_listbox.delete(0, tk.END)
        display_name_map.clear()
        try:
            items = sorted(os.listdir(current_path))
            for item in items:
                item_path = os.path.join(current_path, item)
                if os.path.isdir(item_path):
                    if item == "Desktop":
                        display_name = "📁 桌面"
                    elif item == "files":
                        display_name = "📁 文件"
                    elif item == "apps":
                        display_name = "📁 应用"
                    else:
                        display_name = "📁 " + item
                    file_listbox.insert(tk.END, display_name)
                    display_name_map[display_name] = item_path
                else:
                    display_name = "📄 " + item
                    file_listbox.insert(tk.END, display_name)
                    display_name_map[display_name] = item_path
        except Exception as e:
            messagebox.showerror("错误", f"无法读取目录: {e}")
    def get_selected_items():
        selections = file_listbox.curselection()
        items = []
        for sel in selections:
            selected_item = file_listbox.get(sel)
            item_path = display_name_map.get(selected_item)
            if item_path:
                item_name = os.path.basename(item_path)
                items.append((item_name, item_path))
        return items
    def show_browser_context_menu(event):
        context_menu = tk.Menu(file_browser, tearoff=0)
        selected_items = get_selected_items()
        if selected_items:
            context_menu.add_command(label="打开", command=lambda: open_selected_files(selected_items))
            context_menu.add_command(label="重命名", command=lambda: rename_selected_file(selected_items))
            context_menu.add_command(label="删除", command=lambda: delete_selected_files(selected_items))
            context_menu.add_separator()
            context_menu.add_command(label="复制", command=lambda: copy_selected_files(selected_items))
            context_menu.add_command(label="剪切", command=lambda: cut_selected_files(selected_items))
            context_menu.add_command(label="粘贴", command=lambda: paste_browser_files())
            context_menu.add_separator()
            context_menu.add_command(label="属性", command=lambda: show_selected_properties(selected_items))
        else:
            create_menu = tk.Menu(context_menu, tearoff=0)
            create_menu.add_command(label="文本文档", command=lambda: create_browser_file("txt"))
            create_menu.add_command(label="Python文件", command=lambda: create_browser_file("py"))
            create_menu.add_command(label="Ruby文件", command=lambda: create_browser_file("rb"))
            create_menu.add_command(label="HTML文件", command=lambda: create_browser_file("html"))
            create_menu.add_command(label="JSON文件", command=lambda: create_browser_file("json"))
            create_menu.add_command(label="文件夹", command=lambda: create_browser_folder())
            context_menu.add_cascade(label="新建", menu=create_menu)
            context_menu.add_command(label="在此处打开终端", command=lambda: open_browser_terminal())
            context_menu.add_separator()
            context_menu.add_command(label="刷新", command=update_file_list)
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
    def open_selected_files(items):
        protected_files = ["os_key.txt", "os_key_canuse.txt", "os_password.txt", "os_name.txt", "os_version.txt"]
        for item_name, item_path in items:
            if item_name in protected_files:
                messagebox.showerror("错误", f"无法打开系统文件: {item_name}", parent=file_browser)
                continue
            if "apps" in item_path:
                messagebox.showerror("错误", "无法打开apps文件夹", parent=file_browser)
                continue
            try:
                if os.path.isdir(item_path):
                    messagebox.showinfo("提示", "文件夹功能开发中...")
                elif item_path.endswith(".xsa"):
                    if item_name == "PowerShell.xsa":
                        subprocess.Popen(["start", "PowerShell"], shell=True)
                    else:
                        with open(item_path, 'rb') as f:
                            raw_data = f.read()
                            result = chardetect(raw_data)
                            encoding = result['encoding']
                            content = raw_data.decode(encoding)
                        os.system(content)
                else:
                    os.startfile(item_path)
            except Exception as e:
                messagebox.showerror("错误", f"无法打开 {item_name}: {e}")
    def rename_selected_file(items):
        readonly_files = ["os_key.txt", "os_key_canuse.txt", "os_password.txt", "os_name.txt", "os_version.txt"]
        readonly_folders = ["Desktop", "files", "apps"]
        if len(items) != 1:
            messagebox.showwarning("提示", "请只选择一个文件进行重命名", parent=file_browser)
            return
        item_name, item_path = items[0]
        if item_name in readonly_files:
            messagebox.showerror("错误", f"无法重命名系统文件: {item_name}", parent=file_browser)
            return
        if item_name in readonly_folders:
            messagebox.showerror("错误", f"无法重命名系统文件夹: {item_name}", parent=file_browser)
            return
        new_name = tk.simpledialog.askstring("重命名", "请输入新名称:", initialvalue=item_name, parent=file_browser)
        if new_name and new_name != item_name:
            try:
                new_path = os.path.join(os.path.dirname(item_path), new_name)
                os.rename(item_path, new_path)
                update_file_list()
            except Exception as e:
                messagebox.showerror("错误", f"重命名失败: {e}")
    def delete_selected_files(items):
        protected_folders = ["Desktop", "files", "apps"]
        protected_files = ["os_key.txt", "os_key_canuse.txt", "os_password.txt", "os_name.txt", "os_version.txt"]
        for item_name, item_path in items:
            if os.path.isdir(item_path) and item_name in protected_folders:
                messagebox.showerror("错误", f"无法删除系统文件夹: {item_name}", parent=file_browser)
                return
            if item_name in protected_files:
                messagebox.showerror("错误", f"无法删除系统文件: {item_name}", parent=file_browser)
                return
        result = messagebox.askyesno("确认", f"确定要删除选中的 {len(items)} 个文件吗？", parent=file_browser)
        if result:
            for item_name, item_path in items:
                try:
                    if os.path.isdir(item_path):
                        os.rmdir(item_path)
                    else:
                        os.remove(item_path)
                except Exception as e:
                    messagebox.showerror("错误", f"删除 {item_name} 失败: {e}")
            update_file_list()
    def copy_selected_files(items):
        nonlocal browser_clipboard_files, browser_clipboard_action
        browser_clipboard_files = [item_path for _, item_path in items]
        browser_clipboard_action = "copy"
    def cut_selected_files(items):
        nonlocal browser_clipboard_files, browser_clipboard_action
        browser_clipboard_files = [item_path for _, item_path in items]
        browser_clipboard_action = "cut"
    def paste_browser_files():
        nonlocal browser_clipboard_files, browser_clipboard_action
        if not browser_clipboard_files:
            return
        for src_path in browser_clipboard_files:
            src_name = os.path.basename(src_path)
            dst_path = os.path.join(current_path, src_name)
            try:
                if browser_clipboard_action == "copy":
                    if os.path.isdir(src_path):
                        os.system(f'xcopy "{src_path}" "{dst_path}" /E /I /Y')
                    else:
                        shutil.copy2(src_path, dst_path)
                elif browser_clipboard_action == "cut":
                    # 先复制再删除，避免文件锁定问题
                    if os.path.isdir(src_path):
                        os.system(f'xcopy "{src_path}" "{dst_path}" /E /I /Y')
                        import shutil
                        shutil.rmtree(src_path)
                    else:
                        shutil.copy2(src_path, dst_path)
                        os.remove(src_path)
            except Exception as e:
                messagebox.showerror("错误", f"粘贴 {src_name} 失败: {e}")
        update_file_list()
        browser_clipboard_files.clear()
        browser_clipboard_action = None
    def show_selected_properties(items):
        if len(items) != 1:
            messagebox.showwarning("提示", "请只选择一个文件查看属性")
            return
        item_name, item_path = items[0]
        try:
            size = os.path.getsize(item_path)
            mtime = os.path.getmtime(item_path)
            mtime_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            if os.path.isdir(item_path):
                file_type = "文件夹"
            else:
                file_type = "文件"
            info = f"名称: {item_name}\n类型: {file_type}\n大小: {size} 字节\n修改时间: {mtime_str}"
            messagebox.showinfo("属性", info, parent=file_browser)
        except Exception as e:
            messagebox.showerror("错误", f"无法获取属性: {e}")
    def create_browser_file(extension):
        filename = tk.simpledialog.askstring("新建文件", f"请输入文件名 (.{extension}):", parent=file_browser)
        if filename:
            if not filename.endswith(f".{extension}"):
                filename += f".{extension}"
            file_path = os.path.join(current_path, filename)
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("")
                update_file_list()
            except Exception as e:
                messagebox.showerror("错误", f"创建文件失败: {e}")
    def create_browser_folder():
        foldername = tk.simpledialog.askstring("新建文件夹", "请输入文件夹名称:", parent=file_browser)
        if foldername:
            folder_path = os.path.join(current_path, foldername)
            try:
                os.makedirs(folder_path)
                update_file_list()
            except Exception as e:
                messagebox.showerror("错误", f"创建文件夹失败: {e}")
    def open_browser_terminal():
        try:
            subprocess.Popen(["start", "cmd"], shell=True, cwd=current_path)
        except Exception as e:
            messagebox.showerror("错误", f"无法打开终端: {e}")
    def go_back():
        nonlocal current_path
        if current_path != xos_path:
            parent_path = os.path.dirname(current_path.rstrip("/"))
            if not parent_path or parent_path == ".":
                current_path = xos_path
            else:
                current_path = parent_path + "/"
            path_label.config(text="当前位置: " + get_display_path(current_path))
            update_file_list()
    def on_double_click(event):
        nonlocal current_path
        selection = file_listbox.curselection()
        if selection:
            selected_item = file_listbox.get(selection[0])
            item_path = display_name_map.get(selected_item)
            if item_path and os.path.isdir(item_path):
                if "apps" in item_path:
                    messagebox.showerror("错误", "无法打开apps文件夹", parent=file_browser)
                    return
                current_path = item_path + "/"
                if not current_path.startswith(xos_path):
                    current_path = xos_path
                path_label.config(text="当前位置: " + get_display_path(current_path))
                update_file_list()
            elif item_path:
                protected_files = ["os_key.txt", "os_key_canuse.txt", "os_password.txt", "os_name.txt", "os_version.txt"]
                item_name = os.path.basename(item_path)
                if item_name in protected_files:
                    messagebox.showerror("错误", f"无法打开系统文件: {item_name}", parent=file_browser)
                    return
                if "apps" in item_path:
                    messagebox.showerror("错误", "无法打开apps文件夹", parent=file_browser)
                    return
                try:
                    if item_name.endswith(".xsa"):
                        if item_name == "PowerShell.xsa":
                            subprocess.Popen(["start", "PowerShell"], shell=True)
                        else:
                            with open(item_path, 'rb') as f:
                                raw_data = f.read()
                                result = chardetect(raw_data)
                                encoding = result['encoding']
                                content = raw_data.decode(encoding)
                            os.system(content)
                    else:
                        os.startfile(item_path)
                except Exception as e:
                    messagebox.showerror("错误", f"无法打开文件: {e}")
    def on_browser_key_press(event):
        if event.keysym == "Delete":
            selected_items = get_selected_items()
            if selected_items:
                delete_selected_files(selected_items)
        elif event.state & 0x0004 and event.keysym.lower() == "c":
            selected_items = get_selected_items()
            if selected_items:
                copy_selected_files(selected_items)
        elif event.state & 0x0004 and event.keysym.lower() == "x":
            selected_items = get_selected_items()
            if selected_items:
                cut_selected_files(selected_items)
        elif event.state & 0x0004 and event.keysym.lower() == "v":
            paste_browser_files()
        elif event.keysym == "Return":
            selected_items = get_selected_items()
            if selected_items:
                open_selected_files(selected_items)
    back_button = tk.Button(file_browser, text="返回上级", command=go_back)
    back_button.pack(pady=5)
    file_listbox.bind("<Double-Button-1>", on_double_click); file_listbox.bind("<Alt-Double-Button-1>", lambda e: show_selected_properties(get_selected_items())); file_listbox.bind("<Button-3>", show_browser_context_menu); file_browser.bind("<Key>", on_browser_key_press)
    update_file_list()
    file_browser.mainloop()
def open_apps():
    apps_window = tk.Toplevel(window)
    apps_window.transient(window)
    apps_window.resizable(False, False)
    apps_window.title("打开软件")
    apps_window.geometry("300x400")
    apps_path = xos_path + "apps/"
    apps_listbox = tk.Listbox(apps_window)
    apps_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    apps_display_map = {}
    try:
        if os.path.exists(apps_path):
            files = sorted(os.listdir(apps_path))
            for file in files:
                file_path = os.path.join(apps_path, file)
                if os.path.isfile(file_path):
                    display_name = os.path.splitext(file)[0]
                    apps_listbox.insert(tk.END, display_name)
                    apps_display_map[display_name] = file_path
    except Exception as e:
        messagebox.showerror("错误", f"无法读取apps文件夹: {e}")
    def open_selected_app():
        selection = apps_listbox.curselection()
        if selection:
            display_name = apps_listbox.get(selection[0])
            file_path = apps_display_map.get(display_name)
            if file_path:
                try:
                    if os.path.basename(file_path) == "PowerShell.xsa":
                        subprocess.Popen(["start", "PowerShell"], shell=True)
                    elif file_path.endswith(".xsa"):
                        with open(file_path, 'rb') as f:
                            raw_data = f.read()
                            result = chardetect(raw_data)
                            encoding = result['encoding']
                            content = raw_data.decode(encoding)
                        os.system(content)
                    else:
                        os.startfile(file_path)
                except Exception as e:
                    messagebox.showerror("错误", f"无法打开软件: {e}")
    def delete_selected_app():
        selection = apps_listbox.curselection()
        if selection:
            display_name = apps_listbox.get(selection[0])
            file_path = apps_display_map.get(display_name)
            if file_path:
                protected_apps = ["PowerShell", "Notepad", "Calculator"]
                if display_name in protected_apps:
                    messagebox.showerror("错误", f"无法删除系统软件: {display_name}")
                    return
                result = messagebox.askyesno("确认", f"确定要删除 {display_name} 吗？")
                if result:
                    try:
                        os.remove(file_path)
                        apps_listbox.delete(selection[0])
                        del apps_display_map[display_name]
                    except Exception as e:
                        messagebox.showerror("错误", f"删除失败: {e}")
    def show_apps_context_menu(event):
        context_menu = tk.Menu(apps_window, tearoff=0)
        context_menu.add_command(label="打开", command=open_selected_app)
        context_menu.add_command(label="删除", command=delete_selected_app)
        context_menu.post(event.x_root, event.y_root)
    apps_listbox.bind("<Double-Button-1>", lambda e: open_selected_app())
    apps_listbox.bind("<Button-3>", show_apps_context_menu)
left_buttom_menu.add_command(label="文件资源管理器", command=open_file_browser)
left_buttom_menu.add_command(label="打开软件", command=open_apps)
window.mainloop()