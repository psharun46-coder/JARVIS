import speech_recognition as sr
import pyttsx3
import os

# Import the new, officially supported Google GenAI SDK
from google import genai
from google.genai import types

# Configure API Key securely inside the standalone script
api_key = "AIzaSyCjGpD_mZIrUk6AdbwI_x_XBQXdOJYsVVY"
if not api_key:
    print("Please set your GEMINI_API_KEY.")
    exit(1)

# Initialize the new Client
client = genai.Client(api_key=api_key)
model_id = 'gemini-2.5-flash-lite'

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
if len(voices) > 0:
    engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 175) # Speed of speech

# UI State
chat_log = []

def ui_clear():
    # Enable ANSI escape sequences on Windows
    os.system('') 
    os.system('cls' if os.name == 'nt' else 'clear')

def redraw_ui():
    ui_clear()
    # Print sticky header in green
    print("\033[1;32m" + "=========================================================")
    print("                         JARVIS                          ")
    print("=========================================================\033[0m\n")
    
    # Print the last 15 messages in the log
    for msg in chat_log[-15:]:
        print(msg)
        print("\033[1;30m" + "-"*57 + "\033[0m")
    print("\n")

def log_message(role, text):
    if role == "Jarvis":
        chat_log.append(f"\033[1;36mJarvis:\033[0m {text}")
    elif role == "You":
        chat_log.append(f"\033[1;33mYou:\033[0m {text}")
    else:
        chat_log.append(f"\033[1;35m{text}\033[0m") # System messages
    redraw_ui()

def speak(text):
    log_message("Jarvis", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        redraw_ui()
        print("\033[1;31m[Microphone is ON] Keep quiet to cancel, or Speak now...\033[0m")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=4, phrase_time_limit=15)
            redraw_ui()
            print("\033[1;35mRecognizing audio...\033[0m")
            text = recognizer.recognize_google(audio)
            log_message("You", text)
            return text
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            return None

def main():
    log_message("System", "System initialized. Neural net connected.")
    speak("Hello, Sharun. I am online and perfectly operational.")
    
    # Initialize chat session using the new SDK
    config = types.GenerateContentConfig(
        system_instruction="You are Jarvis, the highly intelligent and witty AI assistant from Iron Man. Address the user as 'Sharun'. Keep your answers brief and conversational."
    )
    chat = client.chats.create(model=model_id, config=config)
    
    redraw_ui()
    print("How would you like to communicate?")
    print("[1] Speak to Jarvis (Voice)")
    print("[2] Type a message to Jarvis (Text)")
    print("[q] Quit System")
    
    while True:
        choice = input("\nEnter your choice (1, 2, or q): ").strip().lower()
        if choice in ['1', '2']:
            mode = 'voice' if choice == '1' else 'text'
            break
        elif choice in ['q', 'quit', 'exit']:
            speak("Powering down. Goodbye, Sharun.")
            return
        else:
            print("Invalid choice. Please enter 1, 2, or q.")
            
    while True:
        user_input = ""
        
        if mode == 'voice':
            user_input = listen()
            if user_input and user_input.lower() in ['type', 'text']:
                mode = 'text'
                log_message("System", "Switched to Text Mode")
                speak("Switched to text mode.")
                continue
        elif mode == 'text':
            redraw_ui()
            user_input = input("\033[1;33mYou (Type):\033[0m ").strip()
            if user_input.lower() == 'speak':
                mode = 'voice'
                log_message("System", "Switched to Voice Mode")
                speak("Switched to voice mode.")
                continue
            elif user_input:
                log_message("You", user_input)
                
        if not user_input:
            continue
            
        text_lower = user_input.lower()
        if text_lower in ['exit', 'quit', 'goodbye', 'stop', 'shut down', 'sleep', 'q']:
            speak("Shutting down immediately. Goodbye, Sharun.")
            break
            
        try:
            redraw_ui()
            print("\033[1;35mJarvis is thinking...\033[0m")
            # Send message using the new SDK
            response = chat.send_message(user_input)
            clean_response = response.text.replace("*", "")
            speak(clean_response)
        except Exception as e:
            log_message("System", f"API ERROR DETAILED LOG: {e}")
            speak("I am sorry, Sharun. My connection to the Google servers encountered an error.")

if __name__ == "__main__":
    main()
