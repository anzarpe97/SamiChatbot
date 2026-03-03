import random
from bot.utils.helpers import wrap_message
from bot.utils.ai_handler import get_ai_response
from bot.utils.history_manager import save_message, load_history

def register_sweet_handler(bot):
    @bot.message_handler(func=lambda message: message.text == "Sweet Message")
    def sweet_message_handler(message):
        # Log the button click
        save_message(
            message.chat.id, 
            "user", 
            "[Clicked Sweet Message Button]", 
            message.from_user.first_name, 
            message.from_user.username
        )
        
        prompt = "Give me a deep, romantic, and sincere compliment for my queen. Focus on her heart."
        response = get_ai_response(prompt, load_history(message.chat.id))
        
        bot.send_message(message.chat.id, wrap_message(response))
        save_message(message.chat.id, "assistant", response)


    @bot.message_handler(func=lambda message: True)
    def chat_handler(message):
        if message.text in ["Convert Currency", "Help", "Sweet Message", "⏰ Reminders", "❌ Cancel", "USD ⮕ KRW", "KRW ⮕ USD", "🇪🇸 Spanish Teacher"]:
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
        
        # Get AI response with true context
        response = get_ai_response(message.text, load_history(message.chat.id))
        
        bot.send_message(message.chat.id, wrap_message(response))
        
        # Save bot response
        save_message(message.chat.id, "assistant", response)
