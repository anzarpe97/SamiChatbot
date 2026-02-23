from bot.utils.helpers import get_sweet_greeting
from bot.keyboards.reply_keyboards import get_main_menu_keyboard

def register_start_handler(bot):
    @bot.message_handler(commands=['start'])
    def start_command(message):
        greeting = get_sweet_greeting()
        bot.reply_to(
            message,
            f"{greeting}",
            reply_markup=get_main_menu_keyboard()
        )
