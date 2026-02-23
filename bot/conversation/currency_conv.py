from bot.utils.api_client import get_exchange_rate
from bot.utils.helpers import wrap_message, format_currency
from bot.keyboards.reply_keyboards import get_main_menu_keyboard, get_cancel_keyboard, get_currency_direction_keyboard

# Dictionary to store temporary user data for conversion
user_data = {}

def register_currency_handlers(bot):
    @bot.message_handler(commands=['convert'])
    @bot.message_handler(func=lambda message: message.text == "Convert Currency")
    def start_currency_conv(message):
        user_data[message.chat.id] = {}
        msg = bot.send_message(
            message.chat.id,
            "My princess, How much would you like to convert? 💰",
            reply_markup=get_cancel_keyboard()
        )
        bot.register_next_step_handler(msg, get_amount, bot)

    def get_amount(message, bot):
        if message.text == "❌ Cancel":
            return cancel(message, bot)
        try:
            amount = float(message.text)
            user_data[message.chat.id]['amount'] = amount
            msg = bot.send_message(
                message.chat.id,
                "Lovely! Now, tell me the direction of the conversion 🌸",
                reply_markup=get_currency_direction_keyboard()
            )
            bot.register_next_step_handler(msg, perform_conversion, bot)
        except ValueError:
            msg = bot.send_message(
                message.chat.id,
                "I'm sorry darling, please enter a valid number for the amount ✨"
            )
            bot.register_next_step_handler(msg, get_amount, bot)

    def perform_conversion(message, bot):
        if message.text == "❌ Cancel":
            return cancel(message, bot)
        
        direction = message.text
        data = user_data.get(message.chat.id, {})
        amount = data.get('amount')

        if direction == "USD ⮕ KRW":
            from_curr, to_curr = "USD", "KRW"
        elif direction == "KRW ⮕ USD":
            from_curr, to_curr = "KRW", "USD"
        else:
            msg = bot.send_message(
                message.chat.id,
                "Please use the buttons below, my princess 🥺",
                reply_markup=get_currency_direction_keyboard()
            )
            bot.register_next_step_handler(msg, perform_conversion, bot)
            return

        rate = get_exchange_rate(from_curr, to_curr)
        
        if rate:
            result = amount * rate
            res_msg = f"There you go, princess! {format_currency(amount, from_curr)} is worth approximately {format_currency(result, to_curr)}"
            bot.send_message(
                message.chat.id,
                wrap_message(res_msg),
                reply_markup=get_main_menu_keyboard()
            )
        else:
            bot.send_message(
                message.chat.id,
                "I'm so sorry, darling. I couldn't find the exchange rate for that. Please try again later 🥺",
                reply_markup=get_main_menu_keyboard()
            )
        
        if message.chat.id in user_data:
            del user_data[message.chat.id]

    def cancel(message, bot):
        bot.send_message(
            message.chat.id,
            "No problem at all, my love. We can do it whenever you feel like it. 💖",
            reply_markup=get_main_menu_keyboard()
        )
        if message.chat.id in user_data:
            del user_data[message.chat.id]
