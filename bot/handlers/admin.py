import os
import sys
from bot.utils.update_manager import pull_and_restart

def register_admin_handlers(bot):
    @bot.message_handler(commands=['restart'])
    def restart_command(message):
        # You might want to restrict this to a specific user ID
        # For now, let's keep it simple as it's a personal bot
        bot.reply_to(message, "Restarting for you, my love")
        pull_and_restart()

    @bot.message_handler(commands=['update_now'])
    def update_now_command(message):
        bot.reply_to(message, "Checking for updates immediately")
        from bot.utils.update_manager import check_for_updates
        if check_for_updates():
            bot.send_message(message.chat.id, "Update found! Applying and restarting")
            pull_and_restart()
        else:
            bot.send_message(message.chat.id, "You are already up to date, princess! No updates found. 🌸")
