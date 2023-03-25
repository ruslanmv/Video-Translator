# coding=utf8
from gtts import gTTS
import gradio as gr
import os
import speech_recognition as sr
from googletrans import Translator, constants
from pprint import pprint
from moviepy.editor import *
def video_to_translate(file_obj,initial_language,final_language):
# Insert Local Video File Path
    videoclip = VideoFileClip(file_obj.name)
    # Insert Local Audio File Path
    videoclip.audio.write_audiofile("test.wav",codec='pcm_s16le')
# initialize the recognizer
    r = sr.Recognizer()

    if initial_language == "English":
        lang_in='en-US'
    elif initial_language == "Italian":
        lang_in='it-IT'
    elif initial_language == "Spanish":
        lang_in='es-MX'
    elif initial_language == "Russian":
        lang_in='ru-RU'
    elif initial_language == "German":
        lang_in='de-DE'
    elif initial_language == "Japanese":
        lang_in='ja-JP'
    elif initial_language == "Portuguese":
        lang_in='pt-BR'
    # open the file
    with sr.AudioFile("test.wav") as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data, language = lang_in)

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
    elif final_language == "Japanese":
        lang='ja'
    elif final_language == "Portuguese":
        lang='pt'                  
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
    new_video="video_translated_"+lang+".mp4"
    videoclip.write_videofile(new_video)
    #return 'audio.wav'
    return new_video

initial_language = gr.inputs.Dropdown(["English","Italian","Japanese","Russian","Spanish","German","Portuguese"])
final_language = gr.inputs.Dropdown([ "Russian","Italian","Spanish","German","English","Japanese","Portuguese"])


gr.Interface(fn = video_to_translate,
            inputs = ['file',initial_language,final_language],
            outputs = 'video', 
            verbose = True,
            title = 'Video Translator',
            description = 'A simple application that translates from English, Italian, Japanese, Russian, Spanish, and German video files to  Italian, Spanish, Russian, English and Japanese. Upload your own file, or click one of the examples to load them. Wait one minute to process.',
            article = 
                        '''<div>
                            <p style="text-align: center"> All you need to do is to upload the mp4 file and hit submit, then wait for compiling. After that click on Play/Pause for listing to the video. The video is saved in an mp4 format.
                            For more information visit <a href="https://ruslanmv.com/">ruslanmv.com</a>
                            </p>
                        </div>''',
            examples=[['obama.mp4',"English",'Spanish'],
                      ['obama.mp4',"English",'Italian'],
                      ['obama.mp4',"English",'German'],
                      ['obama.mp4',"English",'Japanese'],
                      ['obama.mp4',"English",'Portuguese']
                    ]         
            ).launch()