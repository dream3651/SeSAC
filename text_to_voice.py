#pip install gTTS
#pip install langdetect
#pip install pydub
#pip install pygame
import tkinter as tk
from tkinter import ttk
from gtts import gTTS            # Google Text-to-Speech
import os
from langdetect import detect   # 언어를 감지하기 위한 라이브러리
#from pydub import AudioSegment  # 오디오 처리와 재생을 위한 라이브러리
#from pydub.playback import play  # pydub를 사용하여 음성을 바로 재생
import pygame
from datetime import datetime  # 현재시간을 얻기 위해 datetime 모듈 임포트

app = tk.Tk()
app.title("텍스트를 음성으로 변환")
app.geometry("500x100")

# pygame 초기화
pygame.init()

def convert_and_play():
    text = text_entry.get()
    
    detected_lang = detect(text)
    
    if detected_lang == 'ko':
        tts = gTTS(text, lang='ko')
    else:
        tts = gTTS(text, lang='en')

# 현재 시간을 이용하여 파일 이름을 생성        
    current_time=datetime.now().strftime("%Y-%m-%d-%H-%M-%S")    
    output_file = f'output_{current_time}.mp3'    
    tts.save(os.path.expanduser(output_file))
    
# 저장된 음성 파일을 읽고 바로 재생
#     sound = AudioSegment.from_mp3("output.mp3")
#     play(sound)

    pygame.mixer.music.load(output_file)   # 음성파일 재생
    pygame.mixer.music.play()

label = ttk.Label(app, text="문장 입력", width=13, relief='raised', anchor='center')
label.pack(pady=10)

text_entry = ttk.Entry(app, width=68)
text_entry.pack()

convert_button = ttk.Button(app, text="재생", command=convert_and_play)
convert_button.pack(pady=5)

app.mainloop()
