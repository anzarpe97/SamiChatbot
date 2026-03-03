from bot.utils.ai_handler import get_spanish_teacher_response
from bot.utils.history_manager import save_message, load_history
from bot.keyboards.reply_keyboards import get_cancel_keyboard, get_main_menu_keyboard

def register_spanish_teacher_handlers(bot):
    @bot.message_handler(func=lambda message: message.text == "Spanish Teacher")
    def spanish_teacher_start(message):
        # Save user message
        save_message(
            message.chat.id, 
            "user", 
            "[Clicked Spanish Teacher Button]", 
            message.from_user.first_name, 
            message.from_user.username
        )
        
        msg = bot.send_message(
            message.chat.id, 
            "Claro que sí, mi amor! 💖 I'm so proud of you for learning Spanish. What would you like me to explain? (Grammar, vocabulary, or any question)\n\nType **Cancel** to stop.",
            reply_markup=get_cancel_keyboard(),
            parse_mode="Markdown"
        )
        bot.register_next_step_handler(msg, process_spanish_question, bot)

    def process_spanish_question(message, bot):
        if message.text == "❌ Cancel":
            bot.send_message(
                message.chat.id, 
                "No problem, my queen! I'm always here if you need help with anything else. 💋",
                reply_markup=get_main_menu_keyboard()
            )
            return

        bot.send_chat_action(message.chat.id, 'typing')
        
        # Save user message
        save_message(
            message.chat.id, 
            "user", 
            message.text, 
            message.from_user.first_name, 
            message.from_user.username
        )
        
        # Get response from the specialized AI handler
        history = load_history(message.chat.id)
        response = get_spanish_teacher_response(message.text, history)
        
        # Save and send response
        save_message(message.chat.id, "assistant", response)
        
        bot.send_message(
            message.chat.id, 
            response, 
            parse_mode="Markdown",
            reply_markup=get_main_menu_keyboard()
        )
