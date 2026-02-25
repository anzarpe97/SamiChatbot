from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from bot.utils.helpers import wrap_message
from bot.utils.reminder_manager import add_reminder, get_reminders
from bot.keyboards.reply_keyboards import get_main_menu_keyboard, get_cancel_keyboard

# In-memory dictionary to keep track of conversation state
user_data = {}

def get_frequency_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Once"), KeyboardButton("Every day"))
    markup.add(KeyboardButton("Specific Days"))
    markup.add(KeyboardButton("❌ Cancel"))
    return markup

def get_days_keyboard(selected_days):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    
    buttons = []
    for day in days:
        label = f"✅ {day}" if day in selected_days else day
        buttons.append(KeyboardButton(label))
    
    markup.add(*buttons)
    markup.add(KeyboardButton("Done"), KeyboardButton("❌ Cancel"))
    return markup

def register_reminder_handlers(bot):
    @bot.message_handler(func=lambda message: message.text == "⏰ Reminders")
    def start_reminder(message):
        text = "So sweet! 🥰\n\nWhat do you want me to remind you about? (Example: 'Take my medicine', 'Drink water', 'Sleep early')"
        bot.send_message(message.chat.id, wrap_message(text), reply_markup=get_cancel_keyboard())
        bot.register_next_step_handler(message, ask_time)

    def ask_time(message):
        if message.text == '❌ Cancel':
            bot.send_message(message.chat.id, "Operation canceled. ❌", reply_markup=get_main_menu_keyboard())
            return
            
        concept = message.text
        user_data[message.chat.id] = {'concept': concept}
        
        text = f"Got it, I will remind you: '{concept}'.\n\nAt what time do you want me to remind you? (Please use 24-hour format, example: '14:30' or '08:00')"
        bot.send_message(message.chat.id, wrap_message(text), reply_markup=get_cancel_keyboard())
        bot.register_next_step_handler(message, ask_frequency)

    def ask_frequency(message):
        if message.text == '❌ Cancel':
            bot.send_message(message.chat.id, "Operation canceled. ❌", reply_markup=get_main_menu_keyboard())
            return
            
        time_str = message.text
        if len(time_str) != 5 or ':' not in time_str:
            bot.send_message(message.chat.id, "❌ Please use a valid format like '14:30'. Let's try again.\n\nType the time:", reply_markup=get_cancel_keyboard())
            bot.register_next_step_handler(message, ask_frequency)
            return

        user_data[message.chat.id]['time'] = time_str
        
        text = "How often do you want me to send this reminder?"
        bot.send_message(message.chat.id, wrap_message(text), reply_markup=get_frequency_keyboard())
        bot.register_next_step_handler(message, handle_frequency_choice)

    def handle_frequency_choice(message):
        if message.text == '❌ Cancel':
            bot.send_message(message.chat.id, "Operation canceled. ❌", reply_markup=get_main_menu_keyboard())
            return
            
        frequency = message.text
        if frequency not in ["Once", "Every day", "Specific Days"]:
            bot.send_message(message.chat.id, "Please choose an option from the keyboard.", reply_markup=get_frequency_keyboard())
            bot.register_next_step_handler(message, handle_frequency_choice)
            return
            
        user_data[message.chat.id]['frequency'] = frequency
        
        if frequency == "Specific Days":
            user_data[message.chat.id]['days'] = []
            text = "Select the days you want me to remind you. Click 'Done' when finished!"
            bot.send_message(message.chat.id, wrap_message(text), reply_markup=get_days_keyboard([]))
            bot.register_next_step_handler(message, ask_days)
        else:
            finish_reminder(message)

    def ask_days(message):
        if message.text == '❌ Cancel':
            bot.send_message(message.chat.id, "Operation canceled. ❌", reply_markup=get_main_menu_keyboard())
            return
        
        selected_day = message.text.replace("✅ ", "")
        valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        if message.text == "Done":
            if not user_data[message.chat.id]['days']:
                bot.send_message(message.chat.id, "Please select at least one day!", reply_markup=get_days_keyboard([]))
                bot.register_next_step_handler(message, ask_days)
                return
            finish_reminder(message)
            return

        if selected_day in valid_days:
            if selected_day in user_data[message.chat.id]['days']:
                user_data[message.chat.id]['days'].remove(selected_day)
            else:
                user_data[message.chat.id]['days'].append(selected_day)
            
            bot.send_message(message.chat.id, "Toggle days and click 'Done':", reply_markup=get_days_keyboard(user_data[message.chat.id]['days']))
            bot.register_next_step_handler(message, ask_days)
        else:
            bot.send_message(message.chat.id, "Please use the keyboard to select days.", reply_markup=get_days_keyboard(user_data[message.chat.id]['days']))
            bot.register_next_step_handler(message, ask_days)

    def finish_reminder(message):
        chat_id = message.chat.id
        data = user_data.get(chat_id)
        if not data:
            bot.send_message(chat_id, "Something went wrong. Please try again.", reply_markup=get_main_menu_keyboard())
            return
            
        concept = data['concept']
        time_str = data['time']
        frequency = data['frequency']
        days = data.get('days')
        
        add_reminder(chat_id, concept, time_str, frequency, days)
        
        freq_text = frequency
        if frequency == "Specific Days":
            freq_text = f"on {', '.join(days)}"
            
        text = f"All set, beautiful! 🌹\n\nI will remind you '{concept}' at {time_str} ({freq_text}). Sami and I take good care of you! 😘"
        bot.send_message(chat_id, wrap_message(text), reply_markup=get_main_menu_keyboard())
        
        if chat_id in user_data:
            del user_data[chat_id]
