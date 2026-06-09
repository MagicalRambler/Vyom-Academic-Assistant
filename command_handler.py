import datetime
import webbrowser

from voice_engine import speak, take_command
from semester_planner import add_task, show_all_task, show_upcoming_task, clear_semester_task, suggest_study
from reminder_system import add_reminder, show_reminders, clear_reminders
from study_tracker import start_study, stop_study, set_study_goal, check_study_goal
from file_search import open_file


# ── Helpers ───────────────────────────────────────────────────────────────────

def get_valid_input(prompt, retries=3):
    """Keep prompting until we get a non-empty voice response."""
    for _ in range(retries):
        speak(prompt)
        response = take_command()
        if response and response.strip():
            return response
        speak("I did not catch that. Please try again.")
    speak("I could not get your input. Cancelling.")
    return None


def words_to_number(text):
    """Convert spoken number words to float."""
    number_words = {
        "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8,
        "nine": 9, "ten": 10
    }
    text = text.strip().lower()
    if text in number_words:
        return float(number_words[text])
    try:
        return float(text)
    except ValueError:
        return None


# ── Command Router ────────────────────────────────────────────────────────────

def handle_command(command):
    if not command:
        return True

    print("Command received:", command)

    # ── Time ──────────────────────────────────────────────────────────────────
    if "time" in command:
        now = datetime.datetime.now()
        speak("The current time is " + now.strftime("%I:%M %p"))

    # ── Exit ──────────────────────────────────────────────────────────────────
    elif "exit" in command or "shutdown" in command or "bye" in command:
        speak("Shutting down Vyom. Goodbye!")
        return False

    # ── Study Tracker ─────────────────────────────────────────────────────────
    elif "start study" in command:
        start_study()

    elif "stop study" in command:
        stop_study()

    elif "set study goal" in command:
        hours_str = get_valid_input("How many hours do you want to study today?")
        if hours_str:
            hours = words_to_number(hours_str)
            if hours is not None:
                set_study_goal(hours)
            else:
                speak("I could not understand the number. Please say something like two or three.")

    elif "check study goal" in command or "study goal" in command:
        check_study_goal()

    # ── Reminders ─────────────────────────────────────────────────────────────
    elif "add reminder" in command:
        reminder_text = get_valid_input("What should I remember?")
        if reminder_text:
            add_reminder(reminder_text)

    elif "show reminders" in command or "my reminders" in command:
        show_reminders()

    elif "clear reminders" in command:
        clear_reminders()

    # ── Websites ──────────────────────────────────────────────────────────────
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube.")

    elif "open google" in command:
        webbrowser.open("https://google.com")
        speak("Opening Google.")

    # ── File Search ───────────────────────────────────────────────────────────
    elif "open file" in command:
        filename = get_valid_input("Tell me the file name.")
        if filename:
            open_file(filename)

    # ── Semester Tasks ────────────────────────────────────────────────────────
    elif "add semester task" in command or ("semester" in command and "add" in command):
        subject = get_valid_input("Tell me the subject.")
        if not subject:
            return True

        title = get_valid_input("Tell me the title of the task.")
        if not title:
            return True

        task_type = get_valid_input("Is it an assignment or an exam?")
        if not task_type:
            return True

        deadline = get_valid_input("Tell me the deadline in year dash month dash date format. For example, 2026 dash 08 dash 15.")
        if not deadline:
            return True

        # Convert spoken "dash" to actual hyphen
        deadline = deadline.replace("dash", "-").replace(" ", "")
        add_task(subject, title, task_type, deadline)

    elif "show semester task" in command or "show tasks" in command:
        show_all_task()

    elif "upcoming task" in command:
        show_upcoming_task()

    elif "clear semester" in command:
        clear_semester_task()

    elif "suggest study" in command:
        suggest_study()

    # ── Unknown ───────────────────────────────────────────────────────────────
    else:
        speak("I did not recognise that command. Please try again.")

    return True
