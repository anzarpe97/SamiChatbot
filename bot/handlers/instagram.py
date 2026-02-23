import re
import os
from bot.utils.instagram import download_instagram_video
from bot.utils.helpers import wrap_message

def register_instagram_handler(bot):
    # Regex to detect Instagram links (posts, reels, etc.)
    instagram_regex = r'https?://(?:www\.)?instagram\.com/(?:p|reels|reel|tv)/([^/?#&]+)'

    @bot.message_handler(func=lambda message: message.text and re.search(instagram_regex, message.text))
    def handle_instagram_link(message):
        # Extract the URL from the message
        match = re.search(instagram_regex, message.text)
        if not match:
            return

        url = match.group(0)
        
        # Send a "Wait" message in character
        wait_msg = bot.reply_to(message, wrap_message("Wait a second, my queen... I'm getting that video for you. 🌹"))
        
        # Show "uploading video" action
        bot.send_chat_action(message.chat.id, 'upload_video')

        # Download the video
        video_path = download_instagram_video(url)

        if video_path and os.path.exists(video_path):
            try:
                # Send the video
                with open(video_path, 'rb') as video:
                    bot.send_video(message.chat.id, video, caption=wrap_message("Here is your video, beautiful! 😘"))
                
                # Delete the temporary message
                bot.delete_message(message.chat.id, wait_msg.message_id)
            except Exception as e:
                print(f"Error sending video: {e}")
                bot.edit_message_text(wrap_message("I'm so sorry, my love... I couldn't send the video. 🥺"), message.chat.id, wait_msg.message_id)
            finally:
                # Clean up local file
                if os.path.exists(video_path):
                    os.remove(video_path)
        else:
            bot.edit_message_text(wrap_message("Oh no, honey! I couldn't download that video. Maybe it's private? 🥺"), message.chat.id, wait_msg.message_id)
