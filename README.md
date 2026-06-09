# 🎓 Vyom — Voice-Based Academic Assistant

Vyom is a Python voice assistant built for students to manage academic tasks hands-free.
It supports study tracking, semester task planning, reminders, and more — all controlled by voice.

---

## Features

- ⏱️ **Study Tracker** — Start/stop study sessions and log your time
- 🎯 **Study Goal** — Set a daily study hour goal and check progress
- 📅 **Semester Planner** — Add, view, and get upcoming deadline alerts for assignments/exams
- 📝 **Reminders** — Add and review voice reminders
- 📂 **File Search** — Find and open files by name using your voice
- 🌐 **Quick Launch** — Open YouTube, Google by voice

---

## Setup

### Prerequisites
- Python 3.8+
- Windows (uses SAPI5 for TTS); macOS/Linux supported with minor changes
- A working microphone

### Install dependencies

```bash
pip install -r requirements.txt
```

> **Note for Windows:** You may also need to install [PyAudio](https://pypi.org/project/PyAudio/) separately:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

### Run

```bash
python main.py
```

---

## Voice Commands

| Command | Action |
|---|---|
| `"what's the time"` | Tells current time |
| `"start study"` | Starts a study session timer |
| `"stop study"` | Stops the timer and logs the session |
| `"set study goal"` | Set a daily study hour target |
| `"check study goal"` | See how much you've studied vs your goal |
| `"add reminder"` | Save a voice reminder |
| `"show reminders"` | Read all reminders aloud |
| `"clear reminders"` | Delete all reminders |
| `"add semester task"` | Add an assignment/exam with a deadline |
| `"show semester tasks"` | List all semester tasks |
| `"upcoming tasks"` | Tasks due within 7 days |
| `"clear semester tasks"` | Remove all tasks |
| `"suggest study"` | Recommends what to study based on nearest deadline |
| `"open file"` | Search for and open a file by name |
| `"open youtube"` | Opens YouTube in browser |
| `"open google"` | Opens Google in browser |
| `"exit"` / `"shutdown"` | Closes Vyom |

---

## Project Structure

```
vyom/
├── main.py               # Entry point
├── command_handler.py    # Routes voice commands to functions
├── voice_engine.py       # Speech recognition & TTS
├── study_tracker.py      # Study session timer + goal tracking
├── semester_planner.py   # Task management & suggestions
├── reminder_system.py    # Reminder storage
├── file_search.py        # File search & open
├── requirements.txt
└── README.md
```

---

## Known Limitations

- Date entry must follow the format `YYYY-MM-DD` (spoken as "year dash month dash date")
- Voice recognition requires an internet connection (uses Google Speech API)
- TTS uses SAPI5 (Windows built-in); Linux/macOS may need `espeak` or another backend

---

## Built With

- [`SpeechRecognition`](https://pypi.org/project/SpeechRecognition/)
- [`pyttsx3`](https://pypi.org/project/pyttsx3/)
- Python standard library (`datetime`, `json`, `os`, `webbrowser`)

---

*Made by Atharva — MMCOE Pune, Academic Year 2025-26*
