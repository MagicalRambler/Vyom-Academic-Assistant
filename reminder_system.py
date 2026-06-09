import json
from voice_engine import speak

FILE_NAME = "reminders.json"


def _load_reminders():
    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _save_reminders(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)


def add_reminder(text):
    if not text or not text.strip():
        speak("Reminder text was empty. Nothing saved.")
        return

    data = _load_reminders()
    data.append(text.strip())
    _save_reminders(data)
    speak("Reminder saved successfully.")


def show_reminders():
    data = _load_reminders()

    if not data:
        speak("You have no reminders.")
        return

    speak(f"You have {len(data)} reminder{'s' if len(data) > 1 else ''}.")

    for index, reminder in enumerate(data, start=1):
        message = f"Reminder {index}: {reminder}"
        print(message)
        speak(message)


def clear_reminders():
    _save_reminders([])
    speak("All reminders have been cleared.")
