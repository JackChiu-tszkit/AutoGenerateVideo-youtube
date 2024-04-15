from gtts import gTTS
import os

def text_to_speech(text,filename="output.mp3"):
    tts = gTTS(text=text,lang="en")
    tts.save(filename)
    print(os.path.realpath(__file__))
    print(os.path.dirname(os.path.realpath(__file__)))
    
    dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    os.system(dir_path+"\\AutoTube"+"\\"+filename)



if __name__ == "__main__":
    text="This is the text I want to convert to voice"
    text_to_speech(text)

   