import tkinter as tk
from tkinter import ttk, messagebox, filedialog
root = tk.Tk()
root.title("XOS 2.0")
root.resizable(False, False)
root_Versionlabel = tk.Label(root, text="XOS 2.0")
root_Versionlabel.pack(side=tk.TOP, anchor=tk.W)
root_question_frames = tk.Frame(root)
root_question_frames.pack(side=tk.TOP, anchor=tk.W)
system_name = ""
system_key = ""
system_unlock_password = ""

root_question_SystemInfo_1 = tk.LabelFrame(root_question_frames, text="操作系统信息")
root_question_SystemInfo_1.pack(side=tk.LEFT, anchor=tk.W, padx=10, pady=10)
root_question_SystemInfo1_label1 = tk.Label(root_question_SystemInfo_1, text="操作系统名称：")
root_question_SystemInfo1_label1.pack(side=tk.LEFT, anchor=tk.W)
root_question_SystemInfo1_OSName = tk.Entry(root_question_SystemInfo_1)
root_question_SystemInfo1_OSName.pack(side=tk.LEFT, anchor=tk.W)
root_question_SystemInfo1_label2 = tk.Label(root_question_SystemInfo_1, text="操作系统密钥：")
root_question_SystemInfo1_label2.pack(side=tk.LEFT, anchor=tk.W)
root_question_SystemInfo1_OSKey = tk.Entry(root_question_SystemInfo_1)
root_question_SystemInfo1_OSKey.pack(side=tk.LEFT, anchor=tk.W)
root_question_SystemInfo1_label3 = tk.Label(root_question_SystemInfo_1, text="系统解锁密码：")
root_question_SystemInfo1_label3.pack(side=tk.LEFT, anchor=tk.W)
root_question_SystemInfo1_OSUnlockPassword1 = tk.Entry(root_question_SystemInfo_1)
root_question_SystemInfo1_OSUnlockPassword1.pack(side=tk.LEFT, anchor=tk.W)
root_question_SystemInfo1_label4 = tk.Label(root_question_SystemInfo_1, text="确认系统解锁密码：")
root_question_SystemInfo1_label4.pack(side=tk.LEFT, anchor=tk.W)
root_question_SystemInfo1_OSUnlockPassword2 = tk.Entry(root_question_SystemInfo_1)
root_question_SystemInfo1_OSUnlockPassword2.pack(side=tk.LEFT, anchor=tk.W)
def confirm_SystemInfo():
    global root_question_SystemInfo_1, system_name, system_key, system_unlock_password
    for widget in root_question_SystemInfo_1.winfo_children():
        if isinstance(widget, tk.Entry):
            if widget.get() == "":
                messagebox.showerror("错误", "请填写完整操作系统信息")
                return
            else:
                if widget == root_question_SystemInfo1_OSUnlockPassword2:
                    if widget.get() != root_question_SystemInfo1_OSUnlockPassword1.get():
                        messagebox.showerror("错误", "系统解锁密码不一致")
                        return
                else:
                    system_name = root_question_SystemInfo1_OSName.get()
                    system_key = root_question_SystemInfo1_OSKey.get()
                    system_unlock_password = root_question_SystemInfo1_OSUnlockPassword1.get()
    root_question_SystemInfo_1.pack_forget()
root_question_SystemInfo1_Confirm = tk.Button(root_question_SystemInfo_1, text="确认", command=confirm_SystemInfo)
root_question_SystemInfo1_Confirm.pack(side=tk.LEFT, anchor=tk.W)
root_button_create = tk.Button(root, text="创建操作系统", state=tk.DISABLED)
root_button_create.pack(side=tk.LEFT, anchor=tk.W)
root.mainloop()