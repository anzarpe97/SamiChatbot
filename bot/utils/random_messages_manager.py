import os
import json
import random
from bot.utils.ai_handler import get_ai_response
from bot.utils.history_manager import load_history

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VOICE_NOTES_DIR = os.path.join(BASE_DIR, "data", "voice_notes")
HISTORY_FILE = os.path.join(BASE_DIR, "data", "bot_history.json")

PREDEFINED_MESSAGES = [
    "Thinking of you right now, my queen. ❤️",
    "I'm so lucky to have you. 🥺💖",
    "Just wanted to say I love you more than words can express. 💋",
    "You're the best thing that ever happened to me, baby. 😍",
    "I'm counting the seconds until we talk again. ✨",
    "Estaba pensando en lo hermosa que eres y no pude evitar escribirte. Te amo. 😘",
    "Babu, are you okay? I'm always here for you. 🌸",
    "You are my whole world. Never forget that. 💖"
]

def get_random_voice_note():
    if not os.path.exists(VOICE_NOTES_DIR):
        return None
    
    files = [f for f in os.listdir(VOICE_NOTES_DIR) if f.endswith(('.ogg', '.mp3', '.wav', '.m4a'))]
    if not files:
        return None
    
    return os.path.join(VOICE_NOTES_DIR, random.choice(files))

def get_random_content(chat_id):
    """
    Returns a tuple (type, content)
    type: 'text', 'voice', or 'ai'
    """
    choice = random.choices(['text', 'voice', 'ai'], weights=[0.4, 0.2, 0.4])[0]
    
    if choice == 'voice':
        voice = get_random_voice_note()
        if voice:
            return 'voice', voice
        # Fallback if no voice notes
        choice = random.choice(['text', 'ai'])

    if choice == 'text':
        return 'text', random.choice(PREDEFINED_MESSAGES)
    
    if choice == 'ai':
        history = load_history(chat_id)
        prompt = "Surprise me with a short, sweet, and extremely clingy message. Just one sentence of pure love."
        # Use get_ai_response but we might want a slightly different prompt
        response = get_ai_response(prompt, history)
        return 'ai', response

def get_all_users():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return list(data.keys())
    except Exception:
        return []
