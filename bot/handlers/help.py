from bot.keyboards.reply_keyboards import get_main_menu_keyboard

def register_help_handler(bot):
    @bot.message_handler(commands=['help'])
    @bot.message_handler(func=lambda message: message.text == "Help")
    def help_command(message):
        help_text = (
            "My dear princess, here is how I can help you: ✨\n\n"
            "💰 **Convert Currency**: I'll help you with exchange rates.\n"
            "💖 **Sweet Message**: Just because you deserve to hear something nice.\n"
            "✨ **Help**: Show this message again.\n\n"
            "You can always use the menu below! 👑"
        )
        bot.send_message(
            message.chat.id,
            help_text,
            reply_markup=get_main_menu_keyboard(),
            parse_mode="Markdown"
        )
