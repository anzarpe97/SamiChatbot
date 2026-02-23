import telebot
from config import TOKEN
from bot.handlers.start import register_start_handler
from bot.handlers.help import register_help_handler
from bot.handlers.sweet import register_sweet_handler
from bot.handlers.instagram import register_instagram_handler
from bot.conversation.currency_conv import register_currency_handlers

def main():
    bot = telebot.TeleBot(TOKEN)

    # Register all handlers
    register_start_handler(bot)
    register_help_handler(bot)
    register_instagram_handler(bot)  # Registered before sweet_handler
    register_currency_handlers(bot)
    register_sweet_handler(bot)

    print("The bot running using pyTelegramBotAPI")
    bot.infinity_polling()

if __name__ == '__main__':
    main()
