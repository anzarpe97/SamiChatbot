import telebot
import threading
import time
import random
from datetime import datetime
from config import TOKEN, BOT_TIMEZONE
from bot.handlers.start import register_start_handler
from bot.handlers.help import register_help_handler
from bot.handlers.sweet import register_sweet_handler
from bot.conversation.currency_conv import register_currency_handlers
from bot.handlers.reminder import register_reminder_handlers
from bot.utils.reminder_manager import load_reminders, update_reminder_last_sent
from bot.utils.random_messages_manager import get_random_content, get_all_users
from bot.handlers.admin import register_admin_handlers
from bot.handlers.spanish_teacher import register_spanish_teacher_handlers

def random_message_worker(bot):
    """ Sends a random sweet message to users every few hours. """
    while True:
        try:
            # Check every hour
            users = get_all_users()
            for chat_id in users:
                # 20% chance of sending a message every hour
                if random.random() < 0.20:
                    msg_type, content = get_random_content(chat_id)
                    
                    if msg_type in ['text', 'ai']:
                        bot.send_message(chat_id, content)
                    elif msg_type == 'voice':
                        try:
                            with open(content, 'rb') as voice:
                                bot.send_voice(chat_id, voice)
                        except telebot.apihelper.ApiTelegramException as e:
                            if "VOICE_MESSAGES_FORBIDDEN" in str(e):
                                print(f"Voice forbidden for {chat_id}, falling back to text.")
                                # Fallback to a sweet text message if voice is blocked
                                _, fallback_content = get_random_content(chat_id)
                                # Ensure we don't recursive loop into voice again
                                if _ == 'voice': fallback_content = random.choice(PREDEFINED_MESSAGES)
                                bot.send_message(chat_id, fallback_content)
                            else:
                                raise e
                            
                    print(f"Sent random {msg_type} message to {chat_id}")
        except Exception as e:
            print(f"Error in random message worker: {e}")
            
        # Wait 1 hour
        time.sleep(3600)

def reminder_worker(bot):
    while True:
        try:
            now = datetime.now(BOT_TIMEZONE)
            current_time = now.strftime("%H:%M")
            current_date = now.strftime("%Y-%m-%d")
            
            reminders = load_reminders()
            for chat_id, user_reminders in reminders.items():
                for r in user_reminders:
                    if r['time'] == current_time and r.get("last_sent") != current_date:
                        # Check frequency logic
                        should_send = False
                        if r['frequency'] == "Once" or r['frequency'] == "Every day":
                            should_send = True
                        elif r['frequency'] == "Specific Days" and r.get("days"):
                            # weekday() returns 0 for Monday, 6 for Sunday
                            # Python's strftime %A returns 'Monday', 'Tuesday', etc.
                            current_day_name = now.strftime("%A")
                            if current_day_name in r['days']:
                                should_send = True

                        if should_send:
                            try:
                                msg = f"🔔 *Sweet Reminder:*\n\nBabu! It's time to: {r['concept']} 💖"
                                bot.send_message(chat_id, msg, parse_mode="Markdown")
                                update_reminder_last_sent(chat_id, r['id'], current_date)
                            except Exception as e:
                                print(f"Error sending reminder to {chat_id}: {e}")
        except Exception as e:
            print(f"Error in reminders worker: {e}")
            
        time.sleep(60 - datetime.now(BOT_TIMEZONE).second)

from bot.utils.update_manager import auto_update_worker, send_startup_notification

def main():
    bot = telebot.TeleBot(TOKEN)

    # Register all handlers
    register_start_handler(bot)
    register_help_handler(bot)
    register_currency_handlers(bot)
    register_reminder_handlers(bot)
    register_admin_handlers(bot)
    register_spanish_teacher_handlers(bot)
    register_sweet_handler(bot)

    # Send startup notification to all users
    send_startup_notification(bot, get_all_users)

    # Start the reminder thread
    reminder_thread = threading.Thread(target=reminder_worker, args=(bot,), daemon=True)
    reminder_thread.start()

    # Start the random messages thread
    random_thread = threading.Thread(target=random_message_worker, args=(bot,), daemon=True)
    random_thread.start()

    # Start the auto-update thread (checks every 10 minutes)
    update_thread = threading.Thread(target=auto_update_worker, args=(600,), daemon=True)
    update_thread.start()

    print("The bot running using pyTelegramBotAPI")
    
    # Custom polling loop for better error resilience
    while True:
        try:
            # We use polling instead of infinity_polling to manage the loop ourselves
            # non_stop=True ensures it doesn't stop on internal errors
            bot.polling(non_stop=True, timeout=60, long_polling_timeout=20)
        except Exception as e:
            error_msg = str(e).lower()
            # If it's a network error (DNS failure, connection timeout, etc.)
            if any(key in error_msg for key in ["getaddrinfo", "nameresolution", "connection pool", "timeout", "connectionerror"]):
                print(f"Network error detected: {e}")
                print("Waiting 30 seconds before retrying to allow connection to stabilize...")
                time.sleep(30)
            else:
                # For other errors, log and wait briefly
                print(f"Polling error: {e}")
                time.sleep(10)

if __name__ == '__main__':
    main()
