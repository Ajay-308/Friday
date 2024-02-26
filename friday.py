import pyttsx3
import speech_recognition as sr
from datetime import date
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import pyautogui
import sys
import os
from os import listdir
from os.path import isfile, join
import smtplib
import wikipedia
#import Gesture_Controller
#import Gesture_Controller_Gloved as Gesture_Controller
import app
from threading import Thread


# -------------Object Initialization---------------
today = date.today()
r = sr.Recognizer()
keyboard = Controller()
engine = pyttsx3.init('sapi5')
engine.setProperty('voice', engine.getProperty('voices')[1].id)

# ----------------Variables------------------------
file_exp_status = False
files =[]
path = ''
is_awake = True  #Bot status

# ------------------Functions----------------------
def reply(audio):
    app.ChatBot.addAppMsg(audio)

    print(audio)
    engine.say(audio)
    engine.runAndWait()


def wish():
    hour = int(datetime.datetime.now().hour)

    if hour>=0 and hour<12:
        reply("Good Morning Ajay!")
    elif hour>=12 and hour<18:
        reply("Good Afternoon Ajay!")   
    else:
        reply("Good Evening Ajay!")  
        
    reply("I am Friday, What can i do for you!")

# Set Microphone parameters
with sr.Microphone() as source:
        r.energy_threshold = 500 
        r.dynamic_energy_threshold = False

# Audio to String
def record_audio():
    with sr.Microphone() as source:
        try:
            r.pause_threshold = 0.8
            voice_data = ''
            print("Listening...")
            audio = r.listen(source, phrase_time_limit=5)
            print("Recognizing...")
            voice_data = r.recognize_google(audio)
            return voice_data.lower()
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except Exception as e:
            print(f"An error occurred during audio recording; {e}")
        return ''


def respond(voice_data):
    global file_exp_status, files, is_awake, path
    print(voice_data)
    voice_data = voice_data.lower().replace('friday', '')
    app.eel.addUserMsg(voice_data)

    if is_awake==False:
        if 'wake up' in voice_data:
            is_awake = True
            wish()

    elif 'hello' in voice_data:
        wish()

    elif 'what is your name' in voice_data:
        reply('My name is friday i am build by Ajay!')
    
    elif 'i love you' in voice_data:
        reply('I too love you Ajay!')

    elif 'date' in voice_data:
        reply(today.strftime("%B %d, %Y"))

    elif 'time' in voice_data:
        reply(str(datetime.datetime.now()).split(" ")[1].split('.')[0])

    elif 'search' in voice_data:
        reply('Searching for ' + voice_data.split('search')[1])
        url = 'https://google.com/search?q=' + voice_data.split('search')[1]
        try:
            webbrowser.get().open(url)
            reply('This is what I found Ajay')
        except:
            reply('Please check your Internet')
    elif 'open' in voice_data and ('google' in voice_data or 'amazon' in voice_data or 'brave' in voice_data):
        website = voice_data.split('open')[-1].strip()
        url = f'https://{website}.com'
        try:
            webbrowser.get().open(url)
            reply(f'Opening {website} for you, Ajay')
        except:
            reply('Please check your Internet')

    elif 'explain' in voice_data:
        reply("don't warry Ajay, I will explain for you!")
    
    elif 'location' in voice_data:
        reply('Which place are you looking for?📍')
        temp_audio = record_audio()
        app.eel.addUserMsg(temp_audio)
        reply('Locating...')
        url = 'https://google.nl/maps/place/' + temp_audio + '/&amp;'
        try:
            webbrowser.get().open(url)
            reply('This is what I found Ajay')
        except:
            reply('Please check your Internet')

    elif ('bye' in voice_data) or ('by' in voice_data):
        reply("Good bye Ajay! Have a nice day.")
        is_awake = False
    elif ("sleep" in voice_data) or ('slap' in voice_data) or ('sleeeep' in voice_data):
        reply("firday is not dumb like u ")
        if 'sleep' in voice_data:
            time.sleep(5)

    
    elif 'copy' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('c')
            keyboard.release('c')
        reply('Copied')
          
    elif 'page' in voice_data or 'pest'  in voice_data or 'paste' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('v')
            keyboard.release('v')
        reply('Pasted')

        
    # File Navigation (Default Folder set to C://)
    elif 'list' in voice_data:
        counter = 0
        path = 'y://'
        files = listdir(path)
        filestr = ""
        for f in files:
            counter+=1
            print(str(counter) + ':  ' + f)
            filestr += str(counter) + ':  ' + f + '<br>'
        file_exp_status = True
        reply('These are the files in your root directory')
        app.ChatBot.addAppMsg(filestr)
        
    elif file_exp_status == True:
        counter = 0   
        if 'open' in voice_data:
            if isfile(join(path,files[int(voice_data.split(' ')[-1])-1])):
                os.startfile(path + files[int(voice_data.split(' ')[-1])-1])
                file_exp_status = False
            else:
                try:
                    path = path + files[int(voice_data.split(' ')[-1])-1] + '//'
                    files = listdir(path)
                    filestr = ""
                    for f in files:
                        counter+=1
                        filestr += str(counter) + ':  ' + f + '<br>'
                        print(str(counter) + ':  ' + f)
                    reply('Files are listed')
                    app.ChatBot.addAppMsg(filestr)
                    
                except:
                    reply('I do not have permission to access this folder')
            
                                    
        if 'back' in voice_data:
            filestr = ""
            if path == 'C://':
                reply('Sorry, this is the root directory')
            else:
                a = path.split('//')[:-2]
                path = '//'.join(a)
                path += '//'
                files = listdir(path)
                for f in files:
                    counter+=1
                    filestr += str(counter) + ':  ' + f + '<br>'
                    print(str(counter) + ':  ' + f)
                reply('ok')
                app.ChatBot.addAppMsg(filestr)
                   
    else: 
        reply('I am not functioned to do this !')

# ------------------Driver Code--------------------

t1 = Thread(target = app.ChatBot.start)
t1.start()

# Lock main thread until Chatbot has started
while not app.ChatBot.started:
    time.sleep(0.5)

wish()
voice_data = None
exit_command_given = False
while not exit_command_given:
    # take input from GUI
    if app.ChatBot.isUserInput():
        voice_data = app.ChatBot.popUserInput()
    else:
        # take input from Voice
        voice_data = record_audio()

    # process voice_data
    if 'friday' in voice_data:
        try:
            # Handle sys.exit()
            respond(voice_data)
            if 'exit' in voice_data:
                exit_command_given = True
        except SystemExit:
            reply("Exit Successful")
            break
        except:
            # some other exception got raised
            print("EXCEPTION raised while closing.")
            break

    # Add a delay before the next listening attempt
    time.sleep(1)

# Clean up and exit
app.ChatBot.stop()
t1.join()