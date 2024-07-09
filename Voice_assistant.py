import speech_recognition as sr
import pyttsx3
import datetime
import smtplib
import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"User said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
            return ""

def tell_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    speak(f"The current time is {current_time}")

def tell_date():
    today = datetime.datetime.now()
    current_date = today.strftime("%Y-%m-%d")
    speak(f"Today's date is {current_date}")

def send_email(to_address, subject, body):
    from_address = "your_email@example.com"
    password = "your_password"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_address, password)
    email_message = f"Subject: {subject}\n\n{body}"
    server.sendmail(from_address, to_address, email_message)
    server.quit()

def set_reminder(text, time):
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: speak(text), 'date', run_date=time)
    scheduler.start()

def get_weather(city):
    api_key = "your_openweathermap_api_key"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    if data["cod"] == 200:
        main = data["main"]
        weather = data["weather"][0]["description"]
        temperature = main["temp"] - 273.15  # Convert Kelvin to Celsius
        speak(f"The weather in {city} is {weather} with a temperature of {temperature:.1f} degrees Celsius.")
    else:
        speak("Sorry, I couldn't find the weather for that location.")

def main():
    speak("Hello! How can I assist you today?")
    while True:
        command = listen()
        if 'hello' in command:
            speak("Hi there!")
        elif 'time' in command:
            tell_time()
        elif 'date' in command:
            tell_date()
        elif 'email' in command:
            speak("Who is the recipient?")
            to_address = listen() + "@example.com"
            speak("What is the subject?")
            subject = listen()
            speak("What is the message?")
            body = listen()
            send_email(to_address, subject, body)
            speak("Email has been sent.")
        elif 'remind me to' in command:
            text = command.replace('remind me to', '').strip()
            speak("When should I remind you?")
            reminder_time = listen()
            try:
                reminder_time = datetime.datetime.strptime(reminder_time, "%Y-%m-%d %H:%M")
                set_reminder(text, reminder_time)
                speak(f"Reminder set for {reminder_time}.")
            except ValueError:
                speak("Sorry, I didn't understand the time format. Please use 'YYYY-MM-DD HH:MM'.")
        elif 'weather' in command:
            city = command.replace('weather in', '').strip()
            get_weather(city)
        elif 'bye' in command:
            speak("Goodbye!")
            break

if __name__ == "__main__":
    main()