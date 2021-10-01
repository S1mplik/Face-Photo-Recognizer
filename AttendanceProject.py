import ctypes
import json
import smtplib
import subprocess
import webbrowser
from urllib.request import urlopen

import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime, time

import pyjokes as pyjokes
import pyttsx3
import requests
import speech_recognition as sr
import winshell as winshell
import wolframalpha
from cryptography.hazmat.backends.openssl import ec
from wikipedia import wikipedia

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


path = 'ImageAtendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')






encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

while True:
    sucess, img = cap.read()
    imgS = cv2.resize(img,(0, 0), None, 0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace,faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        print(faceDis)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (255, 0, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)
            cv2.imshow('Webcam', img)
            cv2.waitKey(1)

            if(name == "ELON MUSK"):
                def wish():
                    hour = int(datetime.now().hour)
                    if hour >= 0 and hour < 12:
                        speak("Good Morning Sir !")

                    elif hour >= 12 and hour < 18:
                        speak("Good Afternoon Sir !")

                    else:
                        speak("Good Evening Sir !")

                    speak("I am your Assistant. What can i do ?")


                def takeCommand():

                    r = sr.Recognizer()

                    with sr.Microphone() as source:

                        print("Listening...")
                        r.pause_threshold = 1
                        audio = r.listen(source)

                    try:
                        print("Recognizing...")
                        query = r.recognize_google(audio, language='en-US')
                        print(f"Said: {query}\n")

                    except Exception as e:
                        print(e)
                        print("Unable to Recognize your voice.")
                        return "matches"

                    return query


                def sendEmail(to, content):
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.ehlo()
                    server.starttls()

                    server.login('your email id', 'your email password')
                    server.sendmail('your email id', to, content)
                    server.close()


                if __name__ == '__main__':
                    clear = lambda: os.system('cls')


                    clear()
                    wish()

                    while True:

                        query = takeCommand().lower()


                        if 'wikipedia' in query:
                            speak('Searching Wikipedia...')
                            query = query.replace("wikipedia", "")
                            results = wikipedia.summary(query, sentences=3)
                            speak("According to Wikipedia")
                            print(results)
                            speak(results)

                        elif 'open youtube' in query:
                            speak("Here you go to Youtube\n")
                            webbrowser.open("youtube.com")

                        elif 'open google' in query:
                            speak("Here you go to Google\n")
                            webbrowser.open("google.com")

                        elif 'open stackoverflow' in query:
                            speak("Here you go to Stack Over flow.Happy coding")
                            webbrowser.open("stackoverflow.com")

                        elif 'play music' in query or "play song" in query:
                            speak("Here you go with music")
                            # music_dir = "G:\\Song"
                            music_dir = "C:\\Users\\GAURAV\\Music"
                            songs = os.listdir(music_dir)
                            print(songs)
                            random = os.startfile(os.path.join(music_dir, songs[1]))

                        elif 'the time' in query:
                            strTime = datetime.datetime.now().strftime("% H:% M:% S")
                            speak(f"Sir, the time is {strTime}")

                        elif 'open edge' in query:
                            codePath = r"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
                            os.startfile(codePath)

                        elif 'email to dan' in query:
                            try:
                                speak("What should I say?")
                                content = takeCommand()
                                to = "Receiver email address"
                                sendEmail(to, content)
                                speak("Email has been sent !")
                            except Exception as e:
                                print(e)
                                speak("I am not able to send this email")

                        elif 'send a mail' in query:
                            try:
                                speak("What should I say?")
                                content = takeCommand()
                                speak("who should i send it")
                                to = input()
                                sendEmail(to, content)
                                speak("Email has been sent !")
                            except Exception as e:
                                print(e)
                                speak("I am not able to send this email")

                        elif 'how are you' in query:
                            speak("I am fine, Thank you")
                            speak("How are you, Sir")

                        elif 'fine' in query or "good" in query:
                            speak("It's good to know that your fine")

                        elif 'exit' in query:
                            speak("Thanks for giving me your time")
                            exit()

                        elif "who made you" in query or "who created you" in query:
                            speak("I have been created by Gaurav.")

                        elif 'joke' in query:
                            speak(pyjokes.get_joke())

                        elif "calculate" in query:

                            app_id = "Wolframalpha api id"
                            client = wolframalpha.Client(app_id)
                            indx = query.lower().split().index('calculate')
                            query = query.split()[indx + 1:]
                            res = client.query(' '.join(query))
                            answer = next(res.results).text
                            print("The answer is " + answer)
                            speak("The answer is " + answer)

                        elif 'search' in query or 'play' in query:

                            query = query.replace("search", "")
                            query = query.replace("play", "")
                            webbrowser.open(query)

                        elif "who i am" in query:
                            speak("If you talk then definitely your human.")

                        elif 'change background' in query:
                            ctypes.windll.user32.SystemParametersInfoW(20,
                                                                           0,
                                                                           "Location of wallpaper",
                                                                           0)
                            speak("Background changed successfully")

                        elif 'news' in query:

                            try:
                                jsonObj = urlopen(
                                    '''https://newsapi.org / v1 / articles?source = the-times-of-india&sortBy = top&apiKey =\\times of India Api key\\''')
                                data = json.load(jsonObj)
                                i = 1

                                speak('here are some top news from the times of india')
                                print('''=============== TIMES OF INDIA ============''' + '\n')

                                for item in data['articles']:
                                    print(str(i) + '. ' + item['title'] + '\n')
                                    print(item['description'] + '\n')
                                    speak(str(i) + '. ' + item['title'] + '\n')
                                    i += 1
                            except Exception as e:

                                print(str(e))


                        elif 'lock window' in query:
                            speak("locking the device")
                            ctypes.windll.user32.LockWorkStation()

                        elif 'shutdown system' in query:
                            speak("Hold On a Sec ! Your system is on its way to shut down")
                            subprocess.call('shutdown / p /f')

                        elif 'empty recycle bin' in query:
                            winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
                            speak("Recycle Bin Recycled")

                        elif "don't listen" in query or "stop listening" in query:
                            speak("for how much time you want to stop assistant from listening commands")
                            a = int(takeCommand())
                            time.sleep(a)
                            print(a)

                        elif "where is" in query:
                            query = query.replace("where is", "")
                            location = query
                            speak("User asked to Locate")
                            speak(location)
                            webbrowser.open("https://www.google.nl / maps / place/" + location + "")

                        elif "camera" in query or "take a photo" in query:
                            ec.capture(0, " Camera ", "img.jpg")

                        elif "restart" in query:
                            subprocess.call(["shutdown", "/r"])

                        elif "hibernate" in query or "sleep" in query:
                            speak("Hibernating")
                            subprocess.call("shutdown / h")

                        elif "log off" in query or "sign out" in query:
                            speak("Make sure all the application are closed before sign-out")
                            time.sleep(5)
                            subprocess.call(["shutdown", "/l"])

                        elif "write a note" in query:
                            speak("What should i write, sir")
                            note = takeCommand()
                            file = open('voice.txt', 'w')
                            speak("Sir, Should i include date and time")
                            snfm = takeCommand()
                            if 'yes' in snfm or 'sure' in snfm:
                                strTime = datetime.datetime.now().strftime("% H:% M:% S")
                                file.write(strTime)
                                file.write(" :- ")
                                file.write(note)
                            else:
                                file.write(note)

                        elif "show note" in query:
                            speak("Showing Notes")
                            file = open("voice.txt", "r")
                            print(file.read())
                            speak(file.read(6))

                        elif "weather" in query:


                            api_key = "Api key"
                            base_url = "http://api.openweathermap.org / data / 2.5 / weather?"
                            speak(" City name ")
                            print("City name : ")
                            city_name = takeCommand()
                            complete_url = base_url + "appid =" + api_key + "&q =" + city_name
                            response = requests.get(complete_url)
                            x = response.json()

                            if x["cod"] != "404":
                                y = x["main"]
                                current_temperature = y["temp"]
                                current_pressure = y["pressure"]
                                current_humidiy = y["humidity"]
                                z = x["weather"]
                                weather_description = z[0]["description"]
                                print(" Temperature (in kelvin unit) = " + str(
                                    current_temperature) + "\n atmospheric pressure (in hPa unit) =" + str(
                                    current_pressure) + "\n humidity (in percentage) = " + str(
                                    current_humidiy) + "\n description = " + str(weather_description))

                            else:
                                speak(" City Not Found ")

                        elif "send message " in query:
                            # You need to create an account on Twilio to use this service
                            account_sid = 'Account Sid key'
                            auth_token = 'Auth token'
                            client = wolframalpha.Client(account_sid, auth_token)

                            message = client.messages \
                                .create(
                                body=takeCommand(),
                                from_='Sender No',
                                to='Receiver No'
                            )

                            print(message.sid)

                        elif "wikipedia" in query:
                            webbrowser.open("wikipedia.com")






#faceLoc = face_recognition.face_locations(imgElon_Musk)[0]
#encodeElon = face_recognition.face_encodings(imgElon_Musk)[0]
#cv2.rectangle(imgElon_Musk,(faceLoc[3], faceLoc[0]),(faceLoc[1], faceLoc[2]),(255, 0, 0),2)
#faceLocTest = face_recognition.face_locations(imgTest)[0]
#encodeTest = face_recognition.face_encodings(imgTest)[0]
#cv2.rectangle(imgTest,(faceLocTest[3], faceLocTest[0]),(faceLocTest[1], faceLocTest[2]),(255, 0, 0),2)
#results = face_recognition.compare_faces([encodeElon],encodeTest)
#faceDis = face_recognition.face_distance([encodeElon],encodeTest)
