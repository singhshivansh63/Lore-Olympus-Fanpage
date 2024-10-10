import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import webbrowser
import os
import re
from datetime import timedelta
import pyautogui
import time
import pyaudio
import json
import subprocess
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PIL import ImageGrab
import speech_recognition as sr  # Added for speech recognition

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set voice properties
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # Change index for different voices if needed

def talk(text):
    engine.say(text)
    engine.runAndWait()

# Initialize speech recognizer using Google Web Speech API
listener = sr.Recognizer()

def take_command():
    command = ""
    try:
        with sr.Microphone() as source:
            print("Listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice).lower()
            print(f"Command received: {command}")
    except sr.UnknownValueError:
        print("Sorry, I did not hear the command.")
    except sr.RequestError:
        print("Sorry, there's a problem with the speech recognition service.")
    return command

def perform_calculation(expression):
    try:
        result = eval(expression)
        talk(f"The result is {result}")
    except Exception as e:
        talk(f"Error in calculation: {str(e)}")

def fetch_weather(api_key, location):
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    try:
        response = requests.get(url)
        data = response.json()
        temp_c = data['current']['temp_c']
        condition = data['current']['condition']['text']
        talk(f"The current temperature in {location} is {temp_c} degrees Celsius with {condition}.")
    except Exception as e:
        talk(f"Failed to fetch weather: {str(e)}")

def fetch_news(api_key):
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        headlines = [article['title'] for article in data['articles'][:5]]
        for headline in headlines:
            talk(headline)
    except Exception as e:
        talk(f"Failed to fetch news: {str(e)}")

def send_email(smtp_server, smtp_port, username, password, to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
        talk("Email sent successfully.")
    except Exception as e:
        talk(f"Failed to send email: {str(e)}")

def run_jarvis():
    command = take_command()
    if not command:
        return

    # Open JARVIS command
    if "open jarvis" in command:
        talk("Hello Shivansh sir, I am your JARVIS sir. What can I do for you sir?")
        return

    # Close JARVIS command
    if "close jarvis" in command:
        talk("Goodbye Shivansh sir. Closing JARVIS.")
        return True

    if "play" in command:
        song = command.replace("play", "").strip()
        talk(f"Playing {song}")
        pywhatkit.playonyt(song)

    elif "time" in command:
        time_str = datetime.datetime.now().strftime("%I:%M %p")
        talk(f"The current time is {time_str}")

    elif "tell me about" in command:
        person = command.replace("tell me about", "").strip()
        try:
            info = wikipedia.summary(person, 1)
            talk(info)
        except wikipedia.exceptions.PageError:
            talk("Sorry, I couldn't find any information on that topic.")
        except wikipedia.exceptions.DisambiguationError as e:
            talk("There are multiple results for that topic. Please be more specific.")

    elif "your favourite artist" in command:
        talk("My favorite artist is Mr. Worldwide, aka Pitbull.")

    elif "joke" in command:
        talk(pyjokes.get_joke())

    elif "open website" in command:
        url = command.replace("open website", "").strip()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        webbrowser.open(url)
        talk(f"Opening {url}")

    elif "shutdown" in command:
        talk("Shutting down the system.")
        os.system("shutdown /s /t 1")

    elif "send whatsapp message" in command:
        match = re.search(r"to (\+?\d+)", command)
        if match:
            phone_number = match.group(1)
            message = command.replace(f"send whatsapp message to {phone_number}", "").strip()
            talk(f"Sending message to {phone_number}")
            pywhatkit.sendwhatmsg_instantly(phone_number, message)
        else:
            talk("Please provide a phone number with the message.")

    elif "set reminder" in command:
        match = re.search(r"remind me to (.+) in (\d+) (minute|hour|hours|minutes)", command)
        if match:
            task = match.group(1)
            quantity = int(match.group(2))
            unit = match.group(3)
            reminder_time = datetime.datetime.now() + timedelta(**{unit: quantity})
            talk(f"Reminder set for {task} at {reminder_time.strftime('%I:%M %p')}")
            time.sleep(quantity * 60 if unit == "minute" else quantity * 3600)
            talk(f"Reminder: {task}")
        else:
            talk("Please specify the task and time correctly.")

    elif "search" in command:
        query = command.replace("search", "").strip()
        talk(f"Searching for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    elif "open application" in command:
        app_name = command.replace("open application", "").strip()
        talk(f"Opening {app_name}")
        try:
            if os.name == 'nt':  # For Windows
                subprocess.Popen([app_name])
            elif os.name == 'posix':  # For Unix-based OS
                subprocess.Popen([app_name])
            else:
                talk("Unsupported OS.")
        except Exception as e:
            talk(f"Failed to open application: {str(e)}")

    elif "create file" in command:
        match = re.search(r"create file named (.+)", command)
        if match:
            file_name = match.group(1)
            try:
                with open(file_name, 'w') as f:
                    f.write("")
                talk(f"File {file_name} created successfully.")
            except Exception as e:
                talk(f"Failed to create file: {str(e)}")
        else:
            talk("Please specify the file name.")

    elif "delete file" in command:
        match = re.search(r"delete file named (.+)", command)
        if match:
            file_name = match.group(1)
            try:
                os.remove(file_name)
                talk(f"File {file_name} deleted successfully.")
            except Exception as e:
                talk(f"Failed to delete file: {str(e)}")
        else:
            talk("Please specify the file name.")

    elif "rename file" in command:
        match = re.search(r"rename file named (.+) to (.+)", command)
        if match:
            old_name = match.group(1)
            new_name = match.group(2)
            try:
                os.rename(old_name, new_name)
                talk(f"File renamed from {old_name} to {new_name}.")
            except Exception as e:
                talk(f"Failed to rename file: {str(e)}")
        else:
            talk("Please specify the old and new file names.")

    elif "take screenshot" in command:
        screenshot_path = "screenshot_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)
            talk(f"Screenshot taken and saved as {screenshot_path}.")
        except Exception as e:
            talk(f"Failed to take screenshot: {str(e)}")

    elif "open photos" in command:
        talk("Opening Photos")
        try:
            if os.name == 'nt':
                subprocess.Popen("explorer shell:::{F02C1A0D-BE21-4350-8B85-CCF4B2052D0F}")  # Photos folder path
            elif os.name == 'posix':
                subprocess.Popen(["xdg-open", "/path/to/photos"])  # Update with correct path
            else:
                talk("Unsupported OS.")
        except Exception as e:
            talk(f"Failed to open Photos: {str(e)}")

    elif "open videos" in command:
        talk("Opening Videos")
        try:
            if os.name == 'nt':
                subprocess.Popen("explorer shell:::{F02C1A0D-BE21-4350-8B85-CCF4B2052D0F}\\Videos")  # Videos folder path
            elif os.name == 'posix':
                subprocess.Popen(["xdg-open", "/path/to/videos"])  # Update with correct path
            else:
                talk("Unsupported OS.")
        except Exception as e:
            talk(f"Failed to open Videos: {str(e)}")

    elif "open paint" in command:
        talk("Opening Paint")
        try:
            if os.name == 'nt':
                subprocess.Popen("mspaint")
            elif os.name == 'posix':
                subprocess.Popen(["gimp"])  # GIMP as an example for Unix-based OS
            else:
                talk("Unsupported OS.")
        except Exception as e:
            talk(f"Failed to open Paint: {str(e)}")

    elif "open instagram" in command:
        talk("Opening Instagram")
        webbrowser.open("https://www.instagram.com")

    elif "take a picture" in command:
        talk("Opening Camera")
        try:
            if os.name == 'nt':
                subprocess.Popen("start microsoft.windows.camera:")
            elif os.name == 'posix':
                subprocess.Popen(["cheese"])  # Cheese for Unix-based OS
            else:
                talk("Unsupported OS.")
        except Exception as e:
            talk(f"Failed to open Camera: {str(e)}")

    elif "send a message on instagram" in command:
        talk("Please provide the message content and recipient.")
        # Implementation for sending a message on Instagram using an appropriate API

    else:
        talk("I am not sure how to help with that.")

# Main loop
while True:
    if run_jarvis():
        break






