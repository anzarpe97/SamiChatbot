import os
import subprocess
import sys
import time
import threading
from bot.keyboards.reply_keyboards import get_main_menu_keyboard
from bot.utils.ai_handler import get_ai_response

def get_recent_changelog(num_commits=5):
    """Retrieves the last few commit messages to show what's new."""
    try:
        # Get the last few commit messages
        # • %s: bullet point followed by the subject line
        result = subprocess.check_output(
            ["git", "log", "-n", str(num_commits), "--pretty=format:• %s"],
            text=True,
            encoding='utf-8'
        ).strip()
        return result
    except Exception as e:
        print(f"Error getting changelog: {e}")
        return None

def describe_changes_with_ai(changelog):
    """Uses the AI handler to describe the changes in a sweet way."""
    if not changelog:
        return "I've made some small improvements to keep taking care of you, my queen! 💖"
    
    prompt = (
        f"I've updated the bot with these changes:\n{changelog}\n\n"
        "Please describe these changes to your girlfriend in a very sweet, clingy, and loving way. "
        "Keep it very brief but tell her what's new."
    )
    
    return get_ai_response(prompt)

def check_for_updates():
    """Checks if there are new commits in the remote repository."""
    try:
        # Fetch the latest changes from remote
        subprocess.run(["git", "fetch"], check=True, capture_output=True)
        
        # Compare local HEAD with remote HEAD
        local_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
        remote_hash = subprocess.check_output(["git", "rev-parse", "@{u}"]).decode().strip()
        
        if local_hash != remote_hash:
            print(f"Update found! Local: {local_hash}, Remote: {remote_hash}")
            return True
    except Exception as e:
        print(f"Error checking for updates: {e}")
    return False

def pull_and_restart():
    """Pulls the latest changes and restarts the bot process."""
    try:
        print("Pulling updates...")
        subprocess.run(["git", "pull"], check=True)
        
        print("Restarting bot...")
        # On PythonAnywhere Always-on tasks, exiting will trigger a restart.
        # But for local or other servers, we can use execv.
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        print(f"Error during update/restart: {e}")

def auto_update_worker(interval=600):
    """Background worker that periodically checks for updates."""
    print("Auto-update worker started.")
    while True:
        if check_for_updates():
            pull_and_restart()
        time.sleep(interval)

def send_startup_notification(bot, get_all_users):
    """Sends a sweet notification with a changelog and AI description to all users when the bot starts."""
    changelog = get_recent_changelog()
    ai_description = describe_changes_with_ai(changelog)
    
    msg = f"{ai_description}\n\n"
    if changelog:
        msg += f"*Recent updates:*\n{changelog}\n\n"
    msg += "Andi is always here for you! �✨"

    users = get_all_users()
    for chat_id in users:
        try:
            bot.send_message(
                chat_id, 
                msg, 
                parse_mode="Markdown",
                reply_markup=get_main_menu_keyboard()
            )
            print(f"Startup notification sent to {chat_id}")
        except Exception as e:
            print(f"Failed to send startup notification to {chat_id}: {e}")
