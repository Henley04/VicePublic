import os
import tkinter as tk
from tkinter import ttk, messagebox
import configparser
import requests
import subprocess

# 创建ConfigParser对象
config = configparser.ConfigParser()

def get_public_ip(url, retries=3):
    for _ in range(retries):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.text.strip()
        except requests.RequestException as e:
            print(f"Error fetching IP from {url}: {e}")
    return None

# 不同网站的URL列表
ip_services = [
    'https://api.ipify.org',
    'https://ifconfig.me/ip',
    'https://icanhazip.com/',
    'https://ident.me/',
    'https://checkip.amazonaws.com/'
]

# 获取并打印IP地址
ip = None
for service in ip_services:
    ip = get_public_ip(service)
    if ip:
        print(f"Your public IP from {service} is: {ip}")
        break
else:
    print("Could not retrieve IP from any service")

# 读取现有的INI文件
config_file_path = f'{os.getcwd()}/config.ini'
if os.path.exists(config_file_path):
    with open(config_file_path, 'r', encoding='ansi') as file:
        config.read_file(file)
else:
    with open(config_file_path, 'w', encoding='ansi') as configfile:
        config.write(configfile)

# 创建主窗口
root = tk.Tk()
root.title("SetServerINI")
root.geometry("800x400")

# 设置风格
style = ttk.Style(root)
style.theme_use('clam')

# 标签与输入框
def create_label_entry(parent, text, row, default_value):
    label = ttk.Label(parent, text=text)
    label.grid(row=row, column=0, padx=10, pady=10, sticky=tk.W)
    entry = ttk.Entry(parent, width=30)
    entry.grid(row=row, column=1, padx=10, pady=10, sticky=tk.W + tk.E)
    entry.insert(0, default_value)
    return entry

entry1 = create_label_entry(root, "AppID:", 0, config.get('Settings', 'Id', fallback=''))
entry2 = create_label_entry(root, "AppSecret:", 1, config.get('Settings', 'Secret', fallback=''))
entry3 = create_label_entry(root, "提示词:", 2, config.get('Settings', 'prompt', fallback=''))
entry_Auth = create_label_entry(root, "SparkAuth:", 5, config.get('Settings', 'SparkAuth', fallback=''))

label4 = ttk.Label(root, text=f'IP: {ip}')
label4.grid(row=6, column=0, padx=10, pady=10, sticky=tk.W)

# 下拉选择框
def create_combobox(parent, text, row, values, default_value):
    label = ttk.Label(parent, text=text)
    label.grid(row=row, column=0, padx=10, pady=10, sticky=tk.W)
    combobox = ttk.Combobox(parent, values=values, state='readonly')
    combobox.current(values.index(default_value))
    combobox.grid(row=row, column=1, padx=10, pady=10, sticky=tk.W + tk.E)
    return combobox

options = ['4.0Ultra', 'general', 'N/A']
combobox1 = create_combobox(root, "模型:", 3, options, config.get('Settings', 'model', fallback='4.0Ultra'))

options1 = ['是', '否']
blocksplit_value = '是' if config.get('Settings', 'BlockSplit', fallback='1') == '1' else '否'
combobox2 = create_combobox(root, "IfBlock:", 4, options1, blocksplit_value)

# 确认按钮
def on_confirm():
    input1 = entry1.get()
    input2 = entry2.get()
    input3 = entry3.get()
    selected_option = combobox1.get()
    selected_option1 = combobox2.get()
    input_Auth = entry_Auth.get()
    
    if messagebox.askokcancel("确认", "你确定要提交吗？"):
        if not config.has_section('Settings'):
            config.add_section('Settings')
        config.set('Settings', 'Id', input1)
        config.set('Settings', 'Secret', input2)
        config.set('Settings', 'model', selected_option)
        config.set('Settings', 'prompt', input3)
        config.set('Settings', 'SparkAuth', input_Auth)
        config.set('Settings', 'BlockSplit', '1' if selected_option1 == '是' else '0')
        
        with open(config_file_path, 'w', encoding='ansi') as configfile:
            config.write(configfile)
        subprocess.run([f'{os.getcwd()}/Public.exe'])

confirm_button = ttk.Button(root, text="确认", command=on_confirm)
confirm_button.grid(row=7, column=0, columnspan=2, pady=20)

# 运行主循环
root.mainloop()
