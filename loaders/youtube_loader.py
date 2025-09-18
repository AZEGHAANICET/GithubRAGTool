from youtube_transcript_api._errors import TranscriptsDisabled, VideoUnavailable
from typing import Any
from youtube_transcript_api import YouTubeTranscriptApi
import whisper
from pytube import YouTube
from typing import List, Dict
from langchain_core.documents import Document

def fetch_video_transcript(video_id: str, chunk_size:int=30) -> list[Dict]:
    """
    Fetch the transcript of a YouTube video using its video ID.

    Args:
        video_id (str): The unique identifier of the YouTube video.

    Returns:
        list[dict]: A list of transcript entries, where each entry contains:
            - 'text' (str): The spoken text.
            - 'start' (float): The start time in seconds.
            - 'duration' (float): The duration in seconds.

    Raises:
        TranscriptsDisabled: If the video does not have transcripts available.
        VideoUnavailable: If the video is unavailable or removed.
        RuntimeError: If fetching the transcript fails due to an unexpected error.
    """
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"

        transcript_api = YouTubeTranscriptApi()
        transcript_data = transcript_api.fetch(video_id, languages=["en", "fr"])
        transcript_chunks = []
        current_chunk = {"start":None, "end":None, "text":"", "url":url}

        accumaled_time = 0.0

        for transcript in transcript_data:
            start_time  = transcript.start
            end_time = transcript.duration
            text = transcript.text

            if current_chunk["start"] is None:
                current_chunk["start"] = start_time

            if accumaled_time + end_time > chunk_size and current_chunk["text"]:
                current_chunk["end"] = start_time
                transcript_chunks.append(current_chunk)

                current_chunk = {"start":start_time, "end":None, "text":text, "url":url}
                accumaled_time = end_time
            else:
                current_chunk["text"] +=(" " if current_chunk["text"] else "") + text
                accumaled_time +=end_time
            if current_chunk["text"]:
                current_chunk["end"] = current_chunk["start"]+accumaled_time
                transcript_chunks.append(current_chunk)
            unique_transcript = [dict(t) for t in {tuple(d.items()) for d in transcript_chunks}]
        return sorted(unique_transcript, key=lambda t: t["start"])
    except (TranscriptsDisabled, VideoUnavailable) as known_error:
        raise known_error
    except Exception as unexpected_error:
        raise RuntimeError(f"Failed to fetch transcript for video '{video_id}': {unexpected_error}")



def build_document(transcript_chunks: List[Dict]) -> List[Document]:
    """
    Convert a list of transcript chunks into LangChain Document objects
    with start and end timestamps as metadata.

    Args:
        transcript_chunks (List[Dict]): A list of transcript chunks,
            where each chunk is a dictionary containing:
                - "text" (str): The transcript text.
                - "start" (float): Start time in seconds.
                - "end" (float): End time in seconds.

    Returns:
        List[Document]: A list of LangChain Document objects with the
        transcript text as `page_content` and `start`/`end` as metadata.
    """
    documents = []
    for chunk in transcript_chunks:
        document = Document(
            page_content=chunk["text"],
            metadata={
                "start": chunk["start"],
                "end": chunk["end"],
                "url": chunk["url"]
            }
        )
        documents.append(document)
    return documents

