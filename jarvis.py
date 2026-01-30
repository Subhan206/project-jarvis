import pvporcupine
import pyaudio
import struct
import time
import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import wikipedia
from dotenv import load_dotenv

load_dotenv()

# --- Picovoice Access Key ---

PICOVOICE_ACCESS_KEY = os.getenv("PICOVOICE_ACCESS_KEY")

# --- Application Paths Dictionary (COMMAS FIXED) ---
app_paths = {
    "opera": "C:/Users/KIIT/AppData/Local/Programs/Opera GX/opera.exe",
    "perplexity": "C:/Users/KIIT/AppData/Local/Programs/Perplexity/Perplexity.exe",
    "office": "C:/Users/KIIT/AppData/Local/Kingsoft/WPS Office/ksolaunch.exe",
    "ubisoft": "C:/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/UbisoftConnect.exe",
    "trackmania": "steam://rungameid/2225070",
    "wallpapers": "steam://rungameid/431960",
    "spotify": "spotify:",
    "netflix": "C:/Users/KIIT/OneDrive - Manipal Academy of Higher Education/Desktop/Netflix.lnk",
    "whatsapp": "whatsapp:",
    "teams": "C:/Users/KIIT/AppData/Roaming/Microsoft/Internet Explorer/Quick Launch/User Pinned/ImplicitAppShortcuts/afc8ca6eefa68907/Microsoft Teams - Work.lnk",
    "file explorer": "explorer.exe",
    "settings": "ms-settings:",
    "calculator": "calculator:",
    "microsoft store": "ms-windows-store:",
    "valorant": "C:/Riot Games/Riot Client/RiotClientServices.exe",
    "riot": "C:/Riot Games/Riot Client/RiotClientServices.exe",
    "steam": "C:/Program Files (x86)/Steam/steam.exe",
    "ai": "C:/Users/KIIT/OneDrive - Manipal Academy of Higher Education/Desktop/ChatGPT.lnk",
    "chrome": "C:/Users/KIIT/AppData/Roaming/Microsoft/Internet Explorer/Quick Launch/User Pinned/ImplicitAppShortcuts/9501e18d7c2ab92e/Subhan - Chrome.lnk",
    "fx": "C:/Program Files/FxSound LLC/FxSound/FxSound.exe",
    "logitech": "C:/Program Files/LGHUB/system_tray/lghub_system_tray.exe",
}

# --- Core Functions ---

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Calibrating for ambient noise...")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening for command...")
        audio = r.listen(source)
    try:
        print("Recognizing command with Whisper...")
        query = r.recognize_whisper(audio, model="base", language="english")
        print(f"User said: {query}\n")
        return query
    except sr.UnknownValueError:
        return "None"
    except sr.RequestError as e:
        speak("Whisper error; {0}".format(e))
        return "None"

# --- Skill Functions ---

def tell_time():
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"Sir, the current time is {strTime}")

def open_youtube():
    speak("Opening YouTube, sir.")
    webbrowser.open("https://www.youtube.com")

def open_application(query):
    app_name = query.replace("launch", "").strip()
    path = app_paths.get(app_name)
    if path:
        speak(f"Launching {app_name}, sir.")
        try:
            os.startfile(path)
        except Exception as e:
            speak(f"Sorry sir, I could not launch {app_name}.")
    else:
        speak(f"Sorry sir, I don't have the path for {app_name}.")

def search_google(query):
    search_term = query.replace("search google for", "").replace("search for", "").strip()
    speak(f"Searching Google for {search_term}.")
    url = f"https://www.google.com/search?q={search_term}"
    webbrowser.open(url)

def search_wikipedia(query):
    speak("Searching Wikipedia...")
    try:
        search_term = query.replace("search wikipedia for", "").replace("who is", "").strip()
        summary = wikipedia.summary(search_term, sentences=2)
        speak(f"According to Wikipedia, {search_term} is")
        print(summary)
        speak(summary)
    except Exception as e:
        speak(f"Sorry sir, I could not find any results for {search_term}.")

# --- Main Command Processor ---
def process_command(query):
    if 'hello' in query:
        speak("Hello sir. How can I be of service today?")
    elif 'the time' in query:
        tell_time()
    elif 'open youtube' in query:
        open_youtube()
    elif 'launch' in query:
        open_application(query)
    elif 'search wikipedia for' in query or 'who is' in query:
        search_wikipedia(query)
    elif 'search google for' in query or 'search for' in query:
        search_google(query)
    # NOTE: The 'goodbye' command is handled differently in the main loop to exit follow-up mode
    else:
        speak("I don't understand that command.")

# --- Main Execution Block ---

if __name__ == "__main__":
    porcupine = None
    pa = None
    audio_stream = None
    try:
        # Initialize Porcupine
        porcupine = pvporcupine.create(
            access_key=PICOVOICE_ACCESS_KEY,
            keywords=['jarvis']
        )
        # Initialize PyAudio
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )
        print("Wake word engine is running. Say 'Jarvis' to activate.")
        speak("Jarvis is online.")
        
        # Main wake word loop
        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            result = porcupine.process(pcm)
            
            if result >= 0:
                print("Wake word detected!")
                speak("Yes, sir?")
                last_activity_time = time.time()
                
                # --- Start of the Follow-up Mode loop ---
                while time.time() - last_activity_time < 30:
                    query = listen().lower()
                    if query != "none":
                        last_activity_time = time.time() # Reset timer
                        
                        if 'goodbye' in query or 'exit' in query:
                            speak("Goodbye, sir.")
                            break # Breaks the inner follow-up loop
                        
                        process_command(query) # Process all other commands
                else:
                    print("Follow-up timeout. Awaiting wake word.")
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()