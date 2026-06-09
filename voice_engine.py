import speech_recognition as sr
import pyttsx3
import sys

# Initialize TTS engine safely
try:
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    if voices:
        engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 170)
except Exception as e:
    print(f"[WARNING] TTS engine failed to initialize: {e}")
    engine = None


def speak(text):
    print("VYOM:", text)
    if engine:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"[TTS ERROR] {e}")


def take_command():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)

        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()

    except sr.WaitTimeoutError:
        print("Listening timed out.")
        return ""
    except sr.UnknownValueError:
        print("Sorry, could not understand.")
        return ""
    except sr.RequestError as e:
        print(f"Speech recognition service error: {e}")
        return ""
    except Exception as e:
        print(f"Microphone error: {e}")
        return ""
