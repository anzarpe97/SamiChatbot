import json
import os
import uuid

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REMINDERS_FILE = os.path.join(BASE_DIR, 'data', 'reminders.json')

def load_reminders():
    if not os.path.exists(REMINDERS_FILE):
        return {}
    try:
        with open(REMINDERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def save_reminders(data):
    with open(REMINDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_reminder(chat_id, concept, time_str, frequency, days=None):
    data = load_reminders()
    chat_id_str = str(chat_id)
    
    if chat_id_str not in data:
        data[chat_id_str] = []
        
    data[chat_id_str].append({
        "id": str(uuid.uuid4()),
        "concept": concept,
        "time": time_str,
        "frequency": frequency,
        "days": days, # New field for specific days
        "last_sent": ""
    })
    
    save_reminders(data)
    
def get_reminders(chat_id):
    data = load_reminders()
    return data.get(str(chat_id), [])

def update_reminder_last_sent(chat_id, reminder_id, date_str):
    data = load_reminders()
    chat_id_str = str(chat_id)
    
    if chat_id_str in data:
        reminders = data[chat_id_str]
        for r in reminders:
            if r["id"] == reminder_id:
                if r["frequency"] == "Once":
                    reminders.remove(r)
                else:
                    r["last_sent"] = date_str
                break
        save_reminders(data)
