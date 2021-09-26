from gtts import gTTS
import gradio as gr
import os
import speech_recognition as sr
from googletrans import Translator, constants
from pprint import pprint
# pip install moviepy
#pip3 install googletrans
from moviepy.editor import *


def video_to_translate(file_obj,initial_language,final_language):
# Insert Local Video File Path
    videoclip = VideoFileClip(file_obj.name)
    # Insert Local Audio File Path
    videoclip.audio.write_audiofile("test.wav",codec='pcm_s16le')
# initialize the recognizer
    r = sr.Recognizer()
    # open the file
    with sr.AudioFile("test.wav") as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data, language = "en-US")

    if final_language == "English":
        lang='en'
    elif final_language == "Italian":
        lang='it'
    elif final_language == "Spanish":
        lang='es'
    elif final_language == "Russian":
        lang='ru'
    elif final_language == "German":
        lang='de'

    print(lang)
    # init the Google API translator
    translator = Translator()
    translation = translator.translate(text, dest=lang)
    #translation.text
    trans=translation.text


    myobj = gTTS(text=trans, lang=lang, slow=False) 
    myobj.save("audio.wav") 

    # loading audio file
    audioclip = AudioFileClip("audio.wav")
    
    # adding audio to the video clip
    new_audioclip = CompositeAudioClip([audioclip])
    videoclip.audio = new_audioclip
    videoclip.write_videofile("new_filename.mp4")
    #return 'audio.wav'
    return 'new_filename.mp4'


examples = [
    [os.path.abspath("obama.mp4")],
    [os.path.abspath("steve.mp4")]
]


initial_language = gr.inputs.Dropdown(["English"])
final_language = gr.inputs.Dropdown([ "Russian","Italian","Spanish","German","English"])


gr.Interface(fn = video_to_translate,
            inputs = ['file',initial_language,final_language],
            outputs = 'video', 
            verbose = True,
            title = 'Video Translator',
            description = 'A simple application that translate English video files  to  Italian, Spanish, Russian or English Audio . Upload your own file, or click one of the examples to load them. Wait one minute to process.',
             article = 
                        '''<div>
                            <p style="text-align: center"> All you need to do is to upload the pdf file and hit submit, then wait for compiling. After that click on Play/Pause for listing to the video. The video is saved in a mp4 format.</p>
                        </div>''',
                     examples=examples
            ).launch()

        

