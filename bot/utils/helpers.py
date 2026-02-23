import random

def get_sweet_greeting():
    greetings = [
        "Pookie, you are so gorgeous, how don't you get tired of being so beautiful? 😍",
        "Hi darling, I hope your day is as bright as your smile 😘",
        "My lady, how can I serve you today? 💋",
        "Baby,how do you look so radiant today?, tell me your secret 🥺",
        "Honey, what do you need today? 🥺",
        "Pookie ask me anything that you need, i'm your slave 😏",
        "Your wish is my command, my love. Just tell me what you need 🥺",
        "I'm here for you, whatever you need, my queen 💋",
        "Whatever you want to do today, I'm there. Even if it's just watching you shine 🥹",
        "My time is already yours. What can I do for you, Pookie? 😘",
        "My owner my only job is to please you 🥺",
        "I'm at your mercy, and I wouldn't have it any other wa 💋",
        "Whatever you decide, I'll follow. You're in charge, beautiful 😘",
        "I'm a empty body unless I'm serving my queen. What do you need? 💖"
    ]
    return random.choice(greetings)

def wrap_message(text):
    return f"{text}"

def format_currency(amount, currency):
    symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥",
        "KRW": "₩"
    }
    symbol = symbols.get(currency.upper(), currency.upper())
    return f"{symbol}{amount:,.2f}"
