import requests
import json
import time
from colorama import Fore, Style, init

MODEL = "deepseek-coder"
URL = "http://localhost:11434/api/generate"

history = []
memory_db = {}

init(autoreset=True)

def ask(prompt):

    history.append("User: " + prompt)
    full_prompt = "\n".join(history) + "\nAssistant:"

    response = requests.post(URL, json={
        "model": MODEL,
        "prompt": full_prompt,
        "stream": True
    }, stream=True)

    reply = ""

    print(Fore.CYAN + "\nAttessa: ", end="", flush=True)

    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode())
            text = data.get("response", "")

            for char in text:  # typing animation
                print(Fore.GREEN + char, end="", flush=True)
                time.sleep(0.01)

            reply += text

            if data.get("done"):
                break

    print(Style.RESET_ALL + "\n")

    history.append("Assistant: " + reply)
    memory_db[prompt] = reply

    return reply

print("Attessa ready (type quit to exit)")
print("Commands: /read filename.py")

while True:

    user = input(Fore.YELLOW + "You: " + Style.RESET_ALL)

    if user.lower() == "quit":
        break

    # file reader command
    if user.startswith("/read "):
        filename = user.split(" ",1)[1]
        try:
            with open(filename) as f:
                code = f.read()

            ask(f"Analyze this code and suggest improvements:\n{code}")
        except:
            print(Fore.RED + "File not found")
        continue

    # error mode
    if "error" in user.lower():
        ask(f"Fix this error and explain:\n{user}")
        continue

    # cached response
    if user in memory_db:
        print("\nAttessa (cached):", memory_db[user], "\n")
        continue

    ask(user)
