import json
import datetime
from voice_engine import speak

FILE_NAME = "semester_data.json"


def _load_data():
    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _save_data(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)


def _parse_deadline(deadline_str):
    """
    Try to parse a deadline string into a datetime object.
    Returns None if the format is invalid.
    """
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y"):
        try:
            return datetime.datetime.strptime(deadline_str.strip(), fmt)
        except ValueError:
            continue
    return None


# ── Task Management ───────────────────────────────────────────────────────────

def add_task(subject, title, task_type, deadline):
    # Validate deadline before saving
    if _parse_deadline(deadline) is None:
        speak("I could not understand the deadline format. Please use year dash month dash date, for example 2026 dash 08 dash 15.")
        return

    data = _load_data()
    task = {
        "subject": subject.strip(),
        "title": title.strip(),
        "type": task_type.strip(),
        "deadline": deadline.strip()
    }
    data.append(task)
    _save_data(data)
    speak(f"Task added: {title} for {subject}, due on {deadline}.")


def show_all_task():
    data = _load_data()

    if not data:
        speak("No semester tasks found.")
        return

    speak(f"You have {len(data)} semester tasks.")

    for i, task in enumerate(data, start=1):
        message = f"{i}. {task['subject']} — {task['title']}, {task['type']}, due on {task['deadline']}"
        print(message)
        speak(message)


def show_upcoming_task():
    data = _load_data()

    if not data:
        speak("No semester tasks found.")
        return

    today = datetime.datetime.today()
    found = False

    for task in data:
        deadline_dt = _parse_deadline(task["deadline"])
        if deadline_dt is None:
            continue  # skip corrupted entries

        days_left = (deadline_dt - today).days

        if 0 <= days_left <= 7:
            found = True
            message = f"{task['subject']} {task['type']} '{task['title']}' is due in {days_left} days."
            print(message)
            speak(message)

    if not found:
        speak("No upcoming deadlines in the next 7 days.")


def clear_semester_task():
    _save_data([])
    speak("All semester tasks have been cleared.")


def suggest_study():
    tasks = _load_data()

    if not tasks:
        speak("You have no semester tasks to study for.")
        return

    today = datetime.date.today()
    nearest_task = None
    nearest_days = float("inf")

    for task in tasks:
        deadline_dt = _parse_deadline(task["deadline"])
        if deadline_dt is None:
            continue

        days_left = (deadline_dt.date() - today).days

        if days_left < nearest_days:
            nearest_days = days_left
            nearest_task = task

    if nearest_task:
        speak(
            f"You should study {nearest_task['subject']}. "
            f"The task '{nearest_task['title']}' is due in {nearest_days} days."
        )
    else:
        speak("I could not determine a study suggestion. Please check your task deadlines.")
