import os
import openai

import json
import time
import sys


def chat_init(history):
    return history

def chat_one(prompt,model=None):
    conversation = [
        {"role":"system","content":prompt}
    ]
    response = openai.ChatCompletion.create(
    # engine="Feynmind-GPT35",  # The deployment name you chose when you deployed the ChatGPT or GPT-4 model.
    model='gpt-3.5-turbo-16k-0613',
    messages=conversation
)
    # 记录token
    
    # 获取当前脚本所在的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 获取项目根目录的路径
    project_root = os.path.abspath(os.path.join(current_dir, "../../"))
    # 将项目根目录添加到Python路径
    sys.path.append(project_root)
    record_file = "token_record.json"
    if not os.path.exists(record_file):
        with open("token_record.json","w",encoding="utf-8") as f:
            json.dump({"latest_time":"","prompt_tokens":0,"completion_tokens":0,"total_tokens":0},f,ensure_ascii=False,indent=2)
    
    with open("token_record.json",encoding="utf-8") as f:
        record = json.load(f)
        # 获取当前时间戳
        timestamp = time.time()
        # 将时间戳转换为本地时间
        local_time = time.localtime(timestamp)
        # 格式化本地时间
        formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        # 输出当前时间
        record["latest_time"] = formatted_time
        record["prompt_tokens"] += response["usage"]["prompt_tokens"]
        record["completion_tokens"] += response["usage"]["completion_tokens"]
        record["total_tokens"] += response["usage"]["total_tokens"]
        
    with open("token_record.json","w",encoding="utf-8") as f:
        json.dump(record,f,ensure_ascii=False,indent=2)
    conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
    
    return response['choices'][0]['message']['content'].replace("\n", "\n\n")



def load_model(config):
    openai.api_base = ""
    openai.api_key = ""
    return None,None

class Lock:
    def __init__(self):
        pass

    def get_waiting_threads(self):
        return 0

    def __enter__(self): 
        pass

    def __exit__(self, exc_type, exc_val, exc_tb): 
        pass

if __name__ == "__main__":
    model,tokenizer = load_model([])
    # print(openai.api_base,openai.api_key)
    print(chat_one("你好"))