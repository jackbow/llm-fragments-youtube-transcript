import re
from datetime import datetime
from urllib.parse import urlparse, parse_qs

import llm
from yt_dlp import YoutubeDL
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

@llm.hookimpl
def register_fragment_loaders(register):
    register("yt", transcript_loader)

def transcript_loader(url: str) -> llm.Fragment:
    """
    Use yt-dlp to fetch and convert a video transcript to plain text.

    Example usage:
      llm -f 'yt:https://youtube.com/watch?v=...' Summarize this video.
    """
    video_info = []
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError("Invalid YouTube URL: Unable to extract video ID.")
    raw_transcript = YouTubeTranscriptApi().fetch(video_id)
    transcript = TextFormatter().format_transcript(raw_transcript)
    transcript = transcript.replace('\n', ' ').replace('[Music]', '')
    transcript = re.sub(
        r'\s\s+',
        ' ',
        transcript)
    video_info.append("Transcript: " + transcript)
        
    try:
        ydl_opts = {'extract_flat': 'discard_in_playlist',
            'fragment_retries': 10,
            'ignoreerrors': 'only_download',
            'retries': 10,
            'skip_download': True,
            'writeautomaticsub': True,
            'quiet': True,
            'no_warnings': True,
            'subtitleslangs': ['en']} 
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get('title', None)
            channel = info_dict.get('channel', None)
            date = datetime.strptime(info_dict.get('upload_date', None), "%Y%m%d")
            date = date.strftime("%B %d, %Y")
            description: str = info_dict.get('description', None)
            video_info.append("Description: " + description.replace('\n', ' '))
            video_info.append("Date: " + date)
            video_info.append("Uploader: " + channel)
            video_info.append("Title: " + title)
    except Exception:
        video_info.append("There was an error in extracting video title, channel, date, and description.")
        pass
    video_info.append("Video Information:")
    video_info.reverse()
    return llm.Fragment("\n".join(video_info), source=url)

def extract_video_id(url):
    """
    Extracts the video id from YouTube or youtu.be URLs.

    Args:
        url (str): The URL to process.

    Returns:
        str: The youtube video id
    """
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        if domain == "www.youtube.com" or domain == "youtube.com":
            if parsed_url.path == "/watch":
                query_params = parse_qs(parsed_url.query)
                return query_params.get('v', [None])[0]
            elif parsed_url.path.startswith("/embed/"):
                return parsed_url.path.split("/")[2]
            elif parsed_url.path.startswith("/shorts/"):
                return parsed_url.path.split("/")[2]
        elif domain == "youtu.be":
            return parsed_url.path.lstrip('/')
        return None
    except Exception:
        return None
