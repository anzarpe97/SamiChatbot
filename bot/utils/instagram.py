import yt_dlp
import os
import uuid

def download_instagram_video(url):
    """
    Downloads an Instagram video using yt-dlp and returns the local file path.
    """
    temp_filename = f"temp_video_{uuid.uuid4().hex}.mp4"
    output_path = os.path.join("downloads", temp_filename)
    
    # Ensure downloads directory exists
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    ydl_opts = {
        'format': 'best[ext=mp4]/best',  # Prefer a single mp4 file to avoid merging
        'outtmpl': output_path,
        'quiet': True,
        'no_warnings': True,
        # Check for cookies.txt to bypass rate-limits/authentication
        'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
        # Instagram often needs these to avoid bot detection
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        if os.path.exists(output_path):
            return output_path
        return None
    except Exception as e:
        print(f"Error downloading Instagram video: {e}")
        return None
