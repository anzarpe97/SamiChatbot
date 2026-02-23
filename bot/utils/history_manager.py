import json
import os
from datetime import datetime

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HISTORY_FILE = os.path.join(BASE_DIR, "bot_history.json")

def save_message(user_id, role, content, first_name=None, username=None):
    """
    Saves a message to the chat history.
    role: 'user' or 'assistant'
    """
    all_data = {}
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                all_data = json.load(f)
            except json.JSONDecodeError:
                all_data = {}

    user_key = str(user_id)
    
    # Initialize user structure if not exists or if it was the old list format
    if user_key not in all_data or isinstance(all_data[user_key], list):
        # Migrating from old list format to dict format if necessary
        old_history = all_data[user_key] if user_key in all_data and isinstance(all_data[user_key], list) else []
        all_data[user_key] = {
            "user_info": {
                "first_name": first_name,
                "username": username
            },
            "history": old_history
        }
    
    # Update user info if provided
    if first_name:
        all_data[user_key]["user_info"]["first_name"] = first_name
    if username:
        all_data[user_key]["user_info"]["username"] = username

    # Add new message
    new_msg = {
        "timestamp": datetime.now().isoformat(),
        "role": role,
        "content": content
    }
    
    all_data[user_key]["history"].append(new_msg)
    
    # Keep only the last 50 messages
    if len(all_data[user_key]["history"]) > 50:
        all_data[user_key]["history"] = all_data[user_key]["history"][-50:]
    
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

def load_history(user_id):
    """
    Loads the last messages for a specific user.
    """
    if not os.path.exists(HISTORY_FILE):
        return []
        
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        try:
            all_data = json.load(f)
            user_data = all_data.get(str(user_id), {})
            if isinstance(user_data, list):
                return user_data
            return user_data.get("history", [])
        except json.JSONDecodeError:
            return []
