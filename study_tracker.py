import time
import json
from voice_engine import speak

STUDY_FILE = "study_data.json"
GOAL_FILE = "study_goal.json"

start_time = None


def _load_json(filepath, default):
    """Helper to safely load a JSON file."""
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def _save_json(filepath, data):
    """Helper to safely save a JSON file."""
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)


# ── Study Session ─────────────────────────────────────────────────────────────

def start_study():
    global start_time

    if start_time is not None:
        speak("A study session is already running.")
        return

    start_time = time.time()
    speak("Study session started. Good luck!")


def stop_study():
    global start_time

    if start_time is None:
        speak("No study session is currently running.")
        return

    end_time = time.time()
    total_seconds = int(end_time - start_time)
    start_time = None

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    session_data = {
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds,
        "total_seconds": total_seconds
    }

    data = _load_json(STUDY_FILE, [])
    data.append(session_data)
    _save_json(STUDY_FILE, data)

    speak(f"Study session ended. You studied for {hours} hours, {minutes} minutes, and {seconds} seconds.")


# ── Study Goal ────────────────────────────────────────────────────────────────

def set_study_goal(hours):
    _save_json(GOAL_FILE, {"goal_hours": hours})
    speak(f"Daily study goal set to {hours} hours.")


def check_study_goal():
    goal_data = _load_json(GOAL_FILE, None)

    if not goal_data:
        speak("No study goal has been set. Say 'set study goal' to set one.")
        return

    goal_hours = goal_data.get("goal_hours", 0)

    sessions = _load_json(STUDY_FILE, [])

    if not sessions:
        speak("No study sessions recorded today.")
        return

    # FIX: was doing sum() on a list of dicts — now correctly sums total_seconds
    total_seconds = sum(s.get("total_seconds", 0) for s in sessions)
    total_hours = round(total_seconds / 3600, 2)
    remaining = round(goal_hours - total_hours, 2)

    if remaining > 0:
        speak(f"You have studied {total_hours} hours today. {remaining} hours remaining to reach your goal.")
    else:
        speak("Congratulations! You have reached your daily study goal.")
