import time
from voice_engine import speak, take_command
from command_handler import handle_command

speak("Hello! I am Vyom, your personal academic assistant. How can I help you?")
time.sleep(1.5)

running = True

while running:
    command = take_command()

    if not command or command.strip() == "":
        continue

    running = handle_command(command)
