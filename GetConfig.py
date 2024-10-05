import configparser

# 指定 INI 文件路径
file_path = 'path/to/your/file.ini'

# 创建 ConfigParser 对象
config = configparser.ConfigParser()

# 读取 INI 文件
config.read(file_path)

# 如果没有默认的 section，添加一个
if not config.has_section('DEFAULT'):
    config.add_section('DEFAULT')

# 读取并打印现有值
print(f"Original prompt: {config.get('DEFAULT', 'prompt', fallback='default_value')}")
print(f"Original model: {config.get('DEFAULT', 'model', fallback='default_value')}")
print(f"Original BlockSplit: {config.getint('DEFAULT', 'BlockSplit', fallback=1)}")

# 修改值
config.set('DEFAULT', 'prompt', 'you are a superman')
config.set('DEFAULT', 'model', 'SparkPlus')
config.set('DEFAULT', 'BlockSplit', '2')

# 将修改后的配置写回文件
with open(file_path, 'w') as configfile:
    config.write(configfile)

print("INI 文件已成功修改。")
