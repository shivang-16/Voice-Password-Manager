import json
import os
import speech_recognition as sr
import pyttsx3

# File paths
SECURITY_KEY_FILE = 'security_key.json'
PASSWORDS_FILE = 'passwords.json'

engine = pyttsx3.init()

preference = "text"

def speak(text):
    if preference == "voice":
        engine.say(text)
        engine.runAndWait()

def set_security_key(key):
    with open(SECURITY_KEY_FILE, 'w') as file:
        json.dump({'key': key}, file)
    return "Security Key has been set."

def check_permission():
    if not os.path.exists(SECURITY_KEY_FILE):
        speak("Security Key not set. Please set it first.")
        set_security_key(None)
        return False

    speak("Enter Security Key:")
    key = input("Enter Security Key: ")
    with open(SECURITY_KEY_FILE, 'r') as file:
        saved_key = json.load(file).get('key', None)

    if saved_key and saved_key == key:
        return True
    else:
        speak("Wrong Security Key")
        return False

def view_password():
    if check_permission():
        if not os.path.exists(PASSWORDS_FILE):
            speak("No passwords stored yet.")
            open(PASSWORDS_FILE, 'w').close()
            return

        with open(PASSWORDS_FILE, 'r') as file:
            try:
                passwords = json.load(file)
            except json.JSONDecodeError:
                passwords = {}

        if not passwords:
            speak("No passwords stored yet.")
        else:
            for account, password in passwords.items():
                speak(f"Account: {account}, Password: {password}")
    else:
        speak("Access denied. Wrong Security Key.")

def add_password():
    speak("Account name:")
    account = input("Account name: ")

    if os.path.exists(PASSWORDS_FILE):
        with open(PASSWORDS_FILE, 'r') as file:
            try:
                passwords = json.load(file)
            except json.JSONDecodeError:
                passwords = {}
    else:
        passwords = {}

    if account in passwords:
        speak(f"Account '{account}' already exists. Are you sure you want to overwrite the password? Say yes or no.")
        confirm = input(
            f"Account '{account}' already exists. Are you sure you want to overwrite the password? (yes/no): ").lower()
        if confirm != 'yes':
            speak("Password not updated.")
            return

    speak("Enter Password:")
    password = input("Enter Password: ")
    passwords[account] = password

    with open(PASSWORDS_FILE, 'w') as file:
        json.dump(passwords, file)

    speak(f"Password for account: {account} has been added/updated.")

if __name__ == "__main__":
    preference = input("Please select your preference: Voice/Text ").lower()

    if preference == 'voice':
        speak("Hi, I am your virtual password manager...")
        r = sr.Recognizer()
        if not os.path.exists(SECURITY_KEY_FILE):
            speak("Let's set up your security key first. Please provide your key.")
            try:
                with sr.Microphone() as source:
                    audio = r.listen(source, timeout=10, phrase_time_limit=5)
                    recognized_text = r.recognize_google(audio)
                    print(f"Recognized text: {recognized_text}")
                    response = set_security_key(recognized_text)
                    speak(response)
            except sr.UnknownValueError:
                speak("Google could not understand the audio.")
            except sr.RequestError:
                speak("There was an error with the request to Google.")
        else:
            while True:
                text = "What would you like to do? Say View, Add, or Exit."
                print(text)
                speak(text)
                try:
                    with sr.Microphone() as source:
                        print("Listening for command...")
                        audio = r.listen(source, timeout=10, phrase_time_limit=5)
                        command = r.recognize_google(audio).lower()
                        print(f"Recognized command: {command}")

                        if command == "view":
                            view_password()
                        elif command == "add":
                            add_password()
                        elif command == "exit":
                            speak("Exiting the password manager.")
                            break
                        else:
                            speak("Invalid command. Please say View, Add, or Exit.")
                except sr.UnknownValueError:
                    speak("Google could not understand the audio.")
                except sr.RequestError:
                    speak("There was an error with the request to Google.")
    else:
        if not os.path.exists(SECURITY_KEY_FILE):
            key = input("Set your Security Key: ")
            response = set_security_key(key)
            print(response)

        while True:
            command = input('Type what you want to do: View/Add/Exit ').lower()

            if command == "view":
                view_password()
            elif command == "add":
                add_password()
            elif command == "exit":
                print("Exiting the password manager.")
                break
            else:
                print("Invalid command")
