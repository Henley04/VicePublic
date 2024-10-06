import os
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import configparser

# 创建主窗口
root = tk.Tk()
root.title("SetServerINI")
root.geometry("800x400")  # 设置窗口大小

# 设置风格
style = ttk.Style(root)
style.theme_use('clam')  # 使用'clam'主题，还有其他如'aqua', 'alt', 'default', 'classic'

# 标签与输入框1
label1 = ttk.Label(root, text="AppID:")
label1.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

entry1 = ttk.Entry(root, width=30)
entry1.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W+tk.E)

# 标签与输入框2
label2 = ttk.Label(root, text="AppSecret:")
label2.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

entry2 = ttk.Entry(root, width=30)
entry2.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W+tk.E)

label3 = ttk.Label(root, text="提示词:")
label3.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

entry3 = ttk.Entry(root, width=30)
entry3.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W+tk.E)

# 下拉选择框
# 第一个下拉选择框
label3 = ttk.Label(root, text="模型:")
label3.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)

options = ['Spark4.0Ultra', 'N/A', 'N/A']
combobox1 = ttk.Combobox(root, values=options, state='readonly')
combobox1.current(0)  # 默认选中第一个选项
combobox1.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W+tk.E)

# 第二个下拉选择框
label4 = ttk.Label(root, text="IfBlock:")
label4.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)  # 改为第3行

options1 = ['是', '否']
combobox2 = ttk.Combobox(root, values=options1, state='readonly')
combobox2.current(0)  # 默认选中第一个选项
combobox2.grid(row=4, column=1, padx=10, pady=10, sticky=tk.W+tk.E)  # 改为第3行
# 确认按钮
def on_confirm():
    # 收集输入信息
    input1 = entry1.get()
    input2 = entry2.get()
    input3 = entry3.get()
    selected_option = combobox1.get()
    selected_option1 = combobox2.get()


    # 显示确认对话框
    if messagebox.askokcancel("确认", "你确定要提交吗？"):
        # 打印收集到的数据
        print(f"输入框1: {input1}")
        print(f"输入框2: {input2}")
        print(f"输入框3: {input3}")
        print(f"选择的选项: {selected_option}")
        print(f"选择的选项2: {selected_option1}")
        # 创建ConfigParser对象
        config = configparser.ConfigParser()

        # 读取现有的INI文件
        config.read(f'{os.getcwd()}/config.ini')

        # 修改或添加新的键值对
        # 如果section不存在，则会创建新的section
        if not config.has_section('Settings'):
            config.add_section('Settings')
        config.set('Settings', 'Id', input1)  # 修改现有选项
        config.set('Settings', 'Secret', input2)  # 添加新选项
        config.set('Settings', 'model', selected_option)  # 添加新选项
        config.set('Settings', 'prompt', input3)  # 添加新选项

        if selected_option1 == '是':
            config.set('Settings', 'BlockSplit', '1')
        else:
            config.set('Settings', 'BlockSplit', '0')

        # 同样可以修改其他section
        if not config.has_section('Section2'):
            config.add_section('Section2')
        config.set('Section2', 'optionA', 'modified_valueA')  # 修改现有选项

        # 写回文件
        with open('example.ini', 'w') as configfile:
            config.write(configfile)
        subprocess.run(f'{os.getcwd()}/Public.exe')


confirm_button = ttk.Button(root, text="确认", command=on_confirm)
confirm_button.grid(row=5, column=0, columnspan=2, pady=20)

# 运行主循环
root.mainloop()