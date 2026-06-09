import os
import sys
from voice_engine import speak


def _get_default_search_path():
    """Return a sensible default search root for the current OS."""
    if sys.platform == "win32":
        return "C:\\"
    elif sys.platform == "darwin":
        return os.path.expanduser("~")
    else:
        return os.path.expanduser("~")


def search_file(filename, search_path=None):
    if search_path is None:
        search_path = _get_default_search_path()

    filename_lower = filename.lower()

    try:
        for root, dirs, files in os.walk(search_path):
            # Skip hidden/system directories to speed up search
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('Windows', 'System32', '$Recycle.Bin')]
            for file in files:
                if filename_lower in file.lower():
                    return os.path.join(root, file)
        return None

    except PermissionError:
        return None
    except Exception as e:
        print(f"Search error: {e}")
        return None


def open_file(filename):
    if not filename or not filename.strip():
        speak("File name was not clear.")
        return

    speak("Searching for the file. Please wait.")
    path = search_file(filename)

    if path:
        speak(f"File found at {path}. Opening it.")
        try:
            if sys.platform == "win32":
                os.startfile(path)
            elif sys.platform == "darwin":
                os.system(f"open '{path}'")
            else:
                os.system(f"xdg-open '{path}'")
        except Exception as e:
            print(f"Open error: {e}")
            speak("I found the file but could not open it.")
    else:
        speak(f"Sorry, I could not find a file named {filename}.")
