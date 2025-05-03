from flask import Flask, request
import requests
import re
import random
import time
import threading

TOKEN = '8141321315:AAGqrZ7tZ5j6rkVKfS9oeoxF_-ZViLSyCYQ'
bot_url = f'https://api.telegram.org/bot{TOKEN}/'
app = Flask(__name__)

# 30 stylish designs
decorations = [
    "𓆰𓏲!𓂃ֶꪳ{name} 𓆩〭〬🦋𓆪ꪾ", "꧁༒☬{name}☬༒꧂", "★彡[{name}]彡★",
    "♛〔✯{name}✯〕♛", "꧁𓆩{name}𓆪꧂", "{name}❥︎𓆩︎︎︎︎𝑬𝒎𝒐︎︎︎︎𓆪", "𒆜{name}𒆜",
    "ᘜ{name}ᘚ", "๖ۣۜ{name}ۜ", "✞{name}✞", "⫷{name}⫸", "✿{name}✿",
    "꧁ঔৣ☬{name}☬ঔৣ꧂", "☬{name}☬", "★·.·´¯`·.·★ {name} ★·.·´¯`·.·★",
    "◥꧁{name}꧂◤", "⫷⫷{name}⫸⫸", "♡{name}♡", "{name}シ", "彡☆{name}☆彡",
    "⌯{name}⌯", "ᯓ★{name}★ᯓ", "➶➶{name}➷➷", "꧁༺{name}༻꧂", "⸻{name}⸻",
    "⋆｡°✩{name}✩°｡⋆", "༒︎︎{name}༒︎︎", "⌈{name}⌋", "⟆{name}⟇", "༄{name}༄"
]

def make_human_text(text):
    clean = re.sub(r'[.,_\-!":*&?]', '', text)
    clean = re.sub(r'\s+', ' ', clean).strip()
    starters = ['Bro', 'Sun na', 'Arey yaar', 'Suno', 'Hmm', 'Waise', 'Dekho']
    enders = ['samjhe?', 'bas yahi tha', 'thik hai?', 'hai na?', 'fir milte', 'chal theek hai']
    final = f"{random.choice(starters)}, {clean.capitalize()}... {random.choice(enders)}"
    return final

def send_message(chat_id, text):
    url = bot_url + 'sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, json=payload)

def delayed_design(chat_id, name):
    time.sleep(2.5)
    styled = random.choice(decorations).replace('{name}', name.upper())
    send_message(chat_id, styled)

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if 'message' in data and 'text' in data['message']:
        msg = data['message']
        chat_id = msg['chat']['id']
        user_text = msg['text']

        if user_text.startswith('/human'):
            clean_input = user_text.replace('/human', '', 1).strip()
            if clean_input:
                human_text = make_human_text(clean_input)
                send_message(chat_id, human_text)
            else:
                send_message(chat_id, "Bhai, /human ke baad kuch text to likh!")

        elif user_text.startswith('/design'):
            name = user_text.replace('/design', '', 1).strip()
            if name:
                loading_texts = ["Designing your style...", "Crafting your fancy vibe...", "Loading aesthetic energy..."]
                send_message(chat_id, random.choice(loading_texts))
                threading.Thread(target=delayed_design, args=(chat_id, name)).start()
            else:
                send_message(chat_id, "Naam to de bhai /design ke baad!")

    return 'ok'
