from tkinter import filedialog
from tkinter import messagebox
import tkinter as tk
import os
print("等待安装系统...")
# 安装表格
"""
files
    none
apps
    none
os_name
os_key
os_version
os_password
os_key_canuse
"""
print("等待选择文件夹")
path = filedialog.askdirectory(initialdir="/", title="选择安装目录（特殊位置要选择管理员权限！）")
if not path:
    exit()
path += "/"
os.makedirs(path + "files")
os.makedirs(path + "apps")
with open(path + "os_name.txt", "w") as f:
    f.write("XOS")
with open(path + "os_key.txt", "w") as f:
    f.write("")
with open(path + "os_version.txt", "w") as f:
    f.write("XOS 1")
with open(path + "os_password.txt", "w") as f:
    f.write("")
with open(path + "os_key_canuse.txt", "w") as f:
    f.write("0")
print("等待选择XOS扩展...")
select_extension = tk.Tk()
select_extension.title("选择XOS扩展")
select_extension.resizable(False, False)
select_extension_list = ["XSA（XOS系统基础应用）", "PowerShell"]
extension_select = tk.StringVar(value="XSA（XOS系统基础应用）")
for i in range(len(select_extension_list)):
    tk.Radiobutton(select_extension, text=select_extension_list[i], variable=extension_select, value=select_extension_list[i]).pack(side=tk.LEFT)
checked_extensions = []
def confirm_select_extensions():
    global checked_extensions
    for i in range(len(select_extension_list)):
        if extension_select.get() == select_extension_list[i]:
            checked_extensions.append(select_extension_list[i])
    if len(checked_extensions) != 0:
        print("已选择扩展：",extension_select.get())
        select_extension.destroy()
    else:
        messagebox.showerror("错误", "请选择一个扩展")
confirm_select_extensions_button = tk.Button(select_extension, text="确认/取消", command=confirm_select_extensions).pack(padx=10, side=tk.LEFT)
select_extension.mainloop()
del select_extension
del select_extension_list
del confirm_select_extensions
del confirm_select_extensions_button
if extension_select.get() == 'PowerShell':
    with open(path + "apps/PowerShell.xsa", "w") as f:
        f.write("PowerShell")
    print("已安装PowerShell")
elif extension_select.get() == 'XSA（XOS系统基础应用）':
    with open(path + "apps/PowerShell.xsa", "w") as f:
        f.write("PowerShell")
    with open(path + "apps/Calculator.xsa", "w") as f:
        f.write("calc")
    with open(path + "apps/Notepad.xsa", "w") as f:
        f.write("notepad")
    print("已安装XSA（XOS系统基础应用）")
del extension_select
print("安装完成XOS。请完成窗口中的问题，这可能需要一些时间。")
question_window = tk.Tk()
question_window.title("XOS系统问题")
question_window.resizable(False, False)
step_1_frame = tk.Frame(question_window)
step_1_frame.pack(side=tk.TOP, pady=5)
step_1 = tk.Label(step_1_frame, text="1. 请输入XOS系统名称（例如：XOS）：")
step_1.pack(side=tk.LEFT)
step_1_entry = tk.Entry(step_1_frame)
step_1_entry.pack(side=tk.LEFT, padx=5)
step_2_frame = tk.Frame(question_window)
step_2_frame.pack(side=tk.TOP, pady=5)
step_2 = tk.Label(step_2_frame, text="2. 请输入XOS系统密钥（例如：XXXXX:XXXXX:XXXXX:XXXXX:XXXXX，已公开到GitHub，可选）：")
step_2.pack(side=tk.LEFT)
step_2_entry = tk.Entry(step_2_frame)
step_2_entry.pack(side=tk.LEFT, padx=5)
step_3_frame = tk.Frame(question_window)
step_3_frame.pack(side=tk.TOP, pady=5)
step_3 = tk.Label(step_3_frame, text="3. 请输入XOS系统密码（可选）：")
step_3.pack(side=tk.LEFT)
step_3_entry = tk.Entry(step_3_frame, show="*")
step_3_entry.pack(side=tk.LEFT, padx=5)
step_4_frame = tk.Frame(question_window)
step_4_frame.pack(side=tk.TOP, pady=5)
step_4 = tk.Label(step_4_frame, text="4. 请确认XOS系统密码（可选）：")
step_4.pack(side=tk.LEFT)
step_4_entry = tk.Entry(step_4_frame, show="*")
step_4_entry.pack(side=tk.LEFT, padx=5)
def confirm_questions():
    if step_1_entry.get() == "" and step_3_entry.get() != step_4_entry.get():
        messagebox.showerror("错误", "请输入XOS系统名称\n两次输入的XOS系统密码不一致")
        return
    elif step_1_entry.get() == "":
        messagebox.showerror("错误", "请输入XOS系统名称")
        return
    elif step_3_entry.get() != step_4_entry.get():
        messagebox.showerror("错误", "两次输入的XOS系统密码不一致")
        return
    elif step_1_entry.get() != "":
        with open(path + "os_name.txt", "w") as f:
            f.write(step_1_entry.get())
        if step_2_entry.get() != "":
            with open(path + "os_key.txt", "w") as f:
                f.write(step_2_entry.get())
            # 0123456789 ABCDEF
            can_using_os_keys = ["A47B0:94AFF:42D38:1F24B:63B05", "B76FC:3C09D:C3721:CD738:63B05", "C85E9:2B176:84902:0E815:63B05", "D9487:1D264:95A50:2F349:63B05", "E0375:0E463:56B94:30482:63B05", "F1263:57C89:48D20:3G358:63B05", "1A48B:63B05:74A87:67918:DA3E2", "F3281:C4781:54AE3:84531:7AD91", "34EFC:1928A:8E283:2A817:12D29", "E3735:6875C:4CE45:E7386:C5479"]
            if step_2_entry.get() in can_using_os_keys:
                with open(path + "os_key_canuse.txt", "w") as f:
                    f.write("1")
            else:
                with open(path + "os_key_canuse.txt", "w") as f:
                    f.write("0")
                messagebox.showerror("错误", "XOS系统密钥错误，你可以在GitHub上查看公开的密钥。")
        if step_3_entry.get() != "" and step_4_entry.get() != "" and step_3_entry.get() == step_4_entry.get():
            with open(path + "os_password.txt", "w") as f:
                f.write(step_3_entry.get())
        question_window.destroy()
confirm_questions_button = tk.Button(question_window, text="确认", command=confirm_questions).pack(padx=10, pady=5, side=tk.LEFT)
question_window.mainloop()