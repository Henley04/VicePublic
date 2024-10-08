# QQBot VICE created by Henley_EvoSphere
# See https://q.qq.com/qqbot/#/developer/
# See https://github.com/Henley04/VicePublic/
import time
import os
import configparser
import re
import botpy
from botpy.types.message import Message
import requests
import json

# 指定 INI 文件路径
file_path = f'{os.getcwd()}/config.ini'

# 创建 ConfigParser 对象
config = configparser.ConfigParser()

# 读取 INI 文件
with open(file_path, 'r', encoding='ansi') as file:
    config.read_file(file)

# 如果没有默认的 section，添加一个
if config.has_section('Settings'):
    # 读取并打印现有值
    print(f"Original prompt: {config.get('Settings', 'prompt', fallback='default_value')}")
    print(f"Original model: {config.get('Settings', 'model', fallback='default_value')}")
    print(f"Original BlockSplit: {config.getint('Settings', 'BlockSplit', fallback=1)}")
    print(f"Original Id: {config.get('Settings', 'Id', fallback='default_value')}")
    print(f"Original Secret: {config.get('Settings', 'Secret', fallback='default_value')}")
    print(f"Original Auth: {config.get('Settings', 'SparkAuth', fallback='default_value')}")
    print("INI 文件已成功读取。")
else:
    print('ErrorINISectionNotFound:[Settings]')
    print("INI 读取失败。")

# 将修改后的配置写回文件
with open(file_path, 'w', encoding='ansi') as configfile:
    config.write(configfile)


if config.getint('Settings', 'BlockSplit', fallback=1) == 1:
    IfUseBlock = True
Prompt = config.get('Settings', 'prompt', fallback='default_value')
AppId = config.get('Settings', 'Id', fallback='default_value')
AppSecret = config.get('Settings', 'Secret', fallback='default_value')
Model = config.get('Settings', 'model', fallback='default_value')
SparkAuth = config.get('Settings', 'SparkAuth', fallback='default_value')
class Chat(botpy.Client):
    async def on_at_message_create(self, message: Message):
        global SparkAiResponse
        global MsgTxt

        cid = message.channel_id
        GuildID = message.guild_id
        Message = message.content
        print(f'Message={Message}')
        print(f'GuildId={GuildID}')
        user_mentions = re.findall(r'<@!(\d+)>', Message)
        user_ids = [mention for mention in user_mentions]
        for user_id in user_ids:
            MsgTxt = Message.replace(f"<@!{user_id}>", "")
        print(f'MessageTxt={MsgTxt}')
        # Check Message OK
        def filter_bad_words(text, bad_words):
            """
            过滤文本中的不良词汇，并返回过滤后的文本和一个布尔值表示是否检测到违禁词

            :param text: str, 霮要过滤的文本
            :param bad_words: list, 包含不良词汇的列表
            :return: tuple, (过滤后的文本, 是否检测到违禁词)
            """
            detected = False  # 初始化布尔变量，表示是否检测到违禁词

            for word in bad_words:
                if word in text:
                    detected = True  # 如果找到违禁词，将布尔变量设置为 True
                    text = text.replace(word, '*' * len(word))  # 替换违禁词

            return text, detected

        # 示例
        text = MsgTxt
        bad_words = ["垃圾", "恶心", "脑残"]
        if IfUseBlock:
            bad_words = []
        filtered_text, has_bad_words = filter_bad_words(text, bad_words)
        MsgTxt = filtered_text
        if has_bad_words:
            print('BadWordsDetected')
            print(f'OriginalMessage:{text}')
            await self.api.post_message(channel_id=cid, content=f"警告,UesrId=={user_ids}用户！你发送的{MsgTxt}含有不良信息！", msg_id="WARN_POSSIBLE_SPLIT")
        else:
            #Api_Spark

            # 定义全局变量
            SparkAiResponse = ""
            def fetch_and_store_response(MsgTxt):
                print(f'SparkAiGetTxt:{MsgTxt}')
                global SparkAiResponse  # 声明使用全局变量
                SparkAiResponse = ""  # 在开始获取新的响应之前清空变量
                url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
                data = {
                    "max_tokens": 2048,
                    "top_k": 5,
                    "temperature": 0.8,
                    "messages": [
                        {
                            "role": "system",
                            "content": Prompt
                        },
                        {
                            "role": "user",
                            "content": MsgTxt
                        }
                    ],
                    "model": Model,
                    "stream": True
                }
                header = {
                    "Authorization": SparkAuth
                }

                response = requests.post(url, headers=header, json=data, stream=True)

                if response.status_code == 200:
                    # 流式响应解析
                    for line in response.iter_lines():
                        if line:  # 确保line不是空的
                            # 自动检测编码
                            detected_encoding = 'utf-8'
                            decoded_line = line.decode(detected_encoding or 'utf-8', errors='replace')

                            # 去除可能存在的BOM
                            if decoded_line.startswith('\ufeff'):
                                decoded_line = decoded_line[1:]

                            # 将每行响应添加到全局变量中
                            SparkAiResponse += decoded_line + "\n"  # 可以选择是否加上换行符
                            print(decoded_line)  # 打印出来查看
                else:
                    print(f"请求失败，状态码: {response.status_code}")

            if __name__ == '__main__':
                # 调用函数并传入消息文本
                message_text = MsgTxt  # 这应该替换为实际的消息文本
                fetch_and_store_response(message_text)
                # 此时SparkAiResponse包含了整个流式响应的内容
                print("最终响应:", SparkAiResponse)
            if user_mentions:
                for user_id in user_mentions:
                    print(f"UserID: {user_id}")
                    # 你可以在这里使用 user_id 进行其他操作
                    # await self.send_channel_message(message.channel_id, f"你提到的用户ID是: {user_id}")
            else:
                print('NoUserMentioned')
                #await self.send_channel_message(message.channel_id, "没有找到用户提及。")
            try:
                data_string = SparkAiResponse
                # 提取 content 内容并拼接成完整句子
                full_content = ''
                lines = data_string.strip().split('\n')  # 分割成多行
                for line in lines:
                    if line.startswith('data: '):
                        # 移除 'data: ' 前缀
                        json_str = line[6:]
                        try:
                            data = json.loads(json_str)
                            for choice in data.get('choices', []):
                                content = choice.get('delta', {}).get('content')
                                if content:
                                    full_content += content
                        except json.JSONDecodeError as e:
                            print(f"JSON 解码错误: {e}")
                    elif line == '[DONE]':
                        break  # 遇到 [DONE] 结束

                # 输出拼接的内容
                print(full_content)
                await self.api.post_message(channel_id=cid, content=f"你好！", msg_id="AtResponse")
                await self.api.post_message(channel_id=cid, content=full_content, msg_id="AtResponse")
                UserID = message.author.id
                print(f'UserId={UserID}')
                # await self.api.create_dms(guild_id="1", user_id=UserID)
                # await self.api.post_dms(guild_id="1", content="你好，有什么想问薇丝的吗？")
            except():
                print(ConnectionRefusedError)
                await self.api.post_message(channel_id=cid, content=f"QQBot_Error!MsgSendRequestFailed{ConnectionError}",
                                            msg_id="Error")


# 设置意图，这里我们关心公域频道的消息和私聊消息
intents = botpy.Intents(public_guild_messages=True, direct_message=True)

client = Chat(intents=intents)
client.run(appid=AppId, secret=AppSecret)
print(AppId, AppSecret)