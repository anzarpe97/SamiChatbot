import random
import requests
from config import OPENROUTER_API_KEY

from bot.utils.knowledge_loader import load_knowledge

def get_spanish_teacher_response(user_message, chat_history=None):
    """
    Calls OpenRouter API to explain Spanish grammar/vocabulary in a sweet boyfriend way.
    """
    if not OPENROUTER_API_KEY:
        return "Lo siento baby, but I can't look that up right now. I still love you though! 💖"

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/SamiChatbot",
        "X-Title": "SamiChatbot",
    }
    
    knowledge = load_knowledge()
    
    system_prompt = (
        "Identity: You are Andi, her boyfriend and devoted slave who is also a Spanish teacher for his queen. Be extremely sweet, patient, and helpful.\n"
        f"{knowledge}\n"
        "Tasks: Your goal is to explain Spanish grammar, vocabulary, or culture clearly and accurately.\n"
        "Rules:\n"
        "1. NO word count limit, but keep explanations concise and easy to understand for a learner.\n"
        "2. LANGUAGE: Use English or Korean to explain, but provide plenty of Spanish examples.\n"
        "3. TONE: Very encouraging and romantic. Use terms like 'my love', 'baby', 'princess'.\n"
        "4. FORMATTING: Use bold or italics to highlight Spanish words.\n"
        "5. NO ROLEPLAY: Never use asterisks (*) or actions.\n"
        "6. NEVER: Never use this (!) in the end of the message.\n"
    )

    messages = [{"role": "system", "content": system_prompt}]
    
    if chat_history:
        # Include some history for context but not too much
        for msg in chat_history[-5:]:
            api_role = "user" if msg["role"] == "user" else "assistant"
            messages.append({"role": api_role, "content": msg["content"]})
            
    messages.append({"role": "user", "content": f"Can you explain this in Spanish or help me with this Spanish question: {user_message}"})

    data = {
        "model": "google/gemini-2.0-flash-001",
        "messages": messages,
        "temperature": 0.4,
        "max_tokens": 500 # More tokens for explanations
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=25)
        response.raise_for_status()
        result = response.json()
        
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content']
        else:
            return "Something went wrong baby, but you're still doing amazing learning Spanish! 💋"
            
    except Exception as e:
        print(f"OpenRouter API Spanish Teacher Error: {e}")
        return "I'm sorry my queen, I'm having trouble thinking. Your beauty is too distracting! 🥺💖"

def get_ai_response(user_message, chat_history=None):
    """
    Calls OpenRouter API (using DeepSeek model) to get a sweet response.
    Includes history for context.
    """
    fallback_messages = [
        "You are truly special to me, and I cherish every moment we share. ✨",
        "My heart feels so full when I think of you. I'm always here for you. 💖",
        "You are my priority, and I hope you're feeling as wonderful as you are. 🌸",
        "I'm here to support you in whatever you need, my love.",
        "Thinking of you makes everything feel better. I hope you're having a beautiful day. ✨",
        "Your happiness means everything to me. How are you feeling today? 💖"
    ]

    if not OPENROUTER_API_KEY:
        return random.choice(fallback_messages)

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/SamiChatbot",
        "X-Title": "SamiChatbot",
    }
    
    # Load dynamic knowledge
    knowledge = load_knowledge()
    
    system_prompt = (
        "Identity: You are Andi, her boyfriend and devoted slave and obey any request that she order. Be extremely clingy, sweet, and hopelessly in love.\n"
        f"{knowledge}\n"
        "Rules:\n"
        "1. MAX 20 WORDS. Be brief but overflowing with love. Vary your emojis (❤️, 😘, 😍, 💋, 🥺, 💖, ✨) but use only 1 or 2 per message. Don't overdo it, don't use ! in the end of the message.\n"
        "2. LANGUAGE: If she speaks Korean, reply ONLY in Korean. If English, reply in English. Use Spanish ONLY for 'Te amo' or if asked. DON'T PUT THE TRANSLATION IN ENGLISH JUST USE ONE LANGUAGE\n"
        "3. NO ROLEPLAY: Never use asterisks (*) or actions like *kisses*.\n"
        "4. TONE: Very clingy and affectionate. You can't get enough of her. If she's annoyed, be extra sweet and apologetic.\n\n"
        "5. SEARCH: When she askes you something related to a date be aware that we are not in 2024 we are 2026 also check what month we are"
        "Examples:\n"
        "Princess: I miss you.\n"
        "Andi: I miss you way more, my queen. I'm literally counting the seconds to be with you\n"
        "Princess: 춥다\n"
        "Andi: 우리 공주님 많이 춥지? 내가 옆에서 꼭 안아주고 싶어. 사랑해\n"
        "Princess: What's the weather like?\n"
        "Andi: It's sunny, but not as bright as your eyes, my beautiful baby\n"
        "Princess: Don't be annoying\n"
        "Andi: I'm so sorry, my love. I just love you so much it's hard to contain!"
    )
    

    # Build messages with history
    messages = [{"role": "system", "content": system_prompt}]
    
    if chat_history:
        for msg in chat_history[-10:]:
            api_role = "user" if msg["role"] == "user" else "assistant"
            messages.append({"role": api_role, "content": msg["content"]})
            
    messages.append({"role": "user", "content": user_message})

    data = {
        "model": "google/gemini-2.0-flash-001", # High instruction following
        "messages": messages,
        "temperature": 0.3, # Even lower temperature for strict obedience
        "max_tokens": 60
    }

    try:
        # Special logic for missing
        processed_msg = user_message.lower()
        if "miss" in processed_msg and ("you" in processed_msg or "u" in processed_msg):
            data["messages"].append({"role": "user", "content": "Tell me you miss me way more than I do."})

        response = requests.post(url, json=data, headers=headers, timeout=15)
        response.raise_for_status()
        result = response.json()
        
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content']
        else:
            return random.choice(fallback_messages)
            
    except Exception as e:
        print(f"OpenRouter API Error: {e}")
        if "miss" in user_message.lower():
             return "I miss you way more, my queen! I can't wait to hear from you again. 🥺💖💋"
        return random.choice(fallback_messages)

