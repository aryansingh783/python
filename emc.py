import requests
import json
import time
import random

API_KEYS = [
    "AIzaSyDb35kSVqN2zXnvKzcS7SVgch7SwFjoM-M",
    "AIzaSyCbUuz7DQHKxp882uYfzKwpUKV83GpQo9E",
    "AIzaSyC21T_UjQVjpWL91lfk1945t_78_pyNTBs",
    "AIzaSyCTg2PYp2yQ50a2NEPb8PSSuBXleESW4yI",
    "AIzaSyDj2dzP95s-sKRJAC8-mglQTglh6KPXLuk",
    "AIzaSyAtr7D-CRqAd1ki2-QIho_Lzh7hXRJ9dAw",
    ""
]

MODEL = "gemini-2.5-flash"


with open("emc.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

chat_history = []

def type_print(text):
    for ch in text:
        time.sleep(random.uniform(0.01, 0.04))
        print(ch, end="", flush=True)
    print()

print("DELL EMC")

while True:
    user_input = input("You: ")

    if user_input.lower() == "bye":
        type_print("Windows 10: Bye, phir milte hain 👋")
        break

    contents = []

    for msg in chat_history[-6:]:
        contents.append({
            "role": msg["role"],
            "parts": [{"text": msg["text"]}]
        })

    contents.append({
        "role": "user",
        "parts": [{"text": user_input}]
    })

    data = {
        "system_instruction": {
            "parts": [{"text": SYSTEM_PROMPT}]
        },
        "contents": contents
    }

    success = False

    for api_key in API_KEYS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={api_key}"

        try:
            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(data),
                timeout=15
            )

            if response.status_code == 200:
                result = response.json()
                reply = result["candidates"][0]["content"]["parts"][0]["text"]

                chat_history.append({"role": "user", "text": user_input})
                chat_history.append({"role": "model", "text": reply})

                print("Windows 10: ", end="")
                type_print(reply)

                success = True
                break

            elif response.status_code == 429:
                print(".")
                time.sleep(2)

            else:
                print(f"⚠️ Key failed ({response.status_code}), trying next...")

        except Exception as e:
            print("==============================================")

    if not success:
        type_print("Server: Sab API keys exhausted 😵 thoda ruk ke try karo...")
        time.sleep(10)
