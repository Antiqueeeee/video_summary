import gradio
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from pydub.utils import mediainfo
import os

from llm.llm_openai import chat_one,load_model
_,_ = load_model([])

inference_pipeline = pipeline(
    task=Tasks.auto_speech_recognition,
    model='damo/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
    model_revision="v1.2.4")

def mp4_to_mp3(input_file, output_file):
    video = VideoFileClip(input_file)
    audio = video.audio
    audio.write_audiofile(output_file)

def convert_wav_to_mp3(input_file, output_file):
    audio = AudioSegment.from_wav(input_file)
    audio.export(output_file, format="mp3")

def convert_some_to_mp3(input_file,output_file):
    # 使用pydub加载音频文件
    audio = AudioSegment.from_file(input_file)
    # 将音频文件导出为MP3格式
    audio.export(output_file, format="mp3")

def button_function_apply(file_input):
    file = file_input.split("\\")[-1]
    file_name, file_type = ".".join(file.split(".")[:-1]), file.split(".")[-1]
    mp3_file_path = os.path.join("resource",file_name+".mp3")
    if file_type == "mp3":
        pass
    elif file_type == "mp4":
        mp4_to_mp3(file_input,mp3_file_path)
    else:
        try:
            convert_some_to_mp3(file_input,mp3_file_path)
        except:
            return ("Error",file)
    rec_result = inference_pipeline(audio_in=mp3_file_path)["text"]
    prompt = '''
我会给你一份会议记录，里面记录着所有人在会议中说过的话，会议中会提到很多事情，我需要你帮我把记录当中所有提到的事情，以及具体细节都以Markdown的格式记录下来。比如：
会议记录：
数据库你只有一个库就太少了。根据上面的那些内容啊，构建五个库。嗯，好，那我会加的。
Markdown记录：
1. 数据库太少
当前数据库太少了，需要构建五个库。
'''
    sub_prompt = f'''会议记录：\n{rec_result}'''

    return chat_one(prompt + sub_prompt)


with gradio.Blocks() as demo:
    with gradio.Tab("视频/音频总结"):
        with gradio.Row():
            file_input = gradio.File()
        with gradio.Row():
            button_apply = gradio.Button("提交")
        with gradio.Row():
            text_output = gradio.TextArea(label="总结内容",interactive=True)
        button_apply.click(button_function_apply,inputs=file_input,outputs=text_output)
    with gradio.Tab("使用须知"):
        gradio.Markdown(
            '''
            功能：   
                   上传会议记录，生成会议纪要，主要用于记录会议过程中提及的目标。   
            使用方式：   
                   1. 点击上传文件按钮，上传音频、视频类型的会议记录（mp3、m4a、mp4）；   
                   2. 待上传完成后点击提交按钮；   
                   3. 等待会议记录生成，生成的内容会填入在页面下方文本框内。   
'''
        )
        

app,local_url,share_url = demo.launch()
# demo.queue().launch(share=True,server_name='0.0.0.0',server_port=7680,show_error=True)