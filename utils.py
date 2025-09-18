from constants import YOUTUBE_SHORT_URL, YOUTUBE_V_PARAM
def get_id_for_youtube_video(youtube_url):
    """
    Extract the unique video ID from a YouTube URL.

    This function supports standard YouTube URLs (e.g., "https://www.youtube.com/watch?v=VIDEO_ID")
    as well as shortened URLs (e.g., "https://youtu.be/VIDEO_ID"). If the input does not match
    these formats, the original URL is returned.

    Args:
        youtube_url (str): The YouTube URL from which to extract the video ID.

    Returns:
        str: The extracted video ID if recognized; otherwise, returns the original URL.

    Example:
        >>> get_id_for_youtube_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        'dQw4w9WgXcQ'

        >>> get_id_for_youtube_video("https://youtu.be/dQw4w9WgXcQ")
        'dQw4w9WgXcQ'
    """
    if YOUTUBE_V_PARAM in youtube_url:
        return youtube_url.split(YOUTUBE_V_PARAM)[-1]
    elif YOUTUBE_SHORT_URL in youtube_url:
        return youtube_url.split(YOUTUBE_SHORT_URL)[-1]
    return youtube_url


