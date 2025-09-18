import streamlit as st
from database.retriever import search_transcript_chunks
from loaders.youtube_loader import build_document, fetch_video_transcript

# --- Configuration de la page ---
st.set_page_config(page_title="YouTube Transcript Search", page_icon="🎬")

st.title("YouTube Transcript Search")
st.write("Enter a YouTube video ID and a query to search its transcript chunks.")



with st.sidebar:
    st.header("Configuration")
    query = st.text_input("Search query", placeholder="Enter text to search in transcript")
    chunk_size = st.number_input("Chunk size (seconds)", min_value=5, max_value=60, value=15, step=5)
    number_of_chunks = st.number_input("Number chunk result you want ", min_value=2, max_value=10, value=5, step=1)

video_id = st.text_input("YouTube Video ID", placeholder="e.g., vCF1kqw1fWs")

button = st.button("Search")
if video_id and query and button:
    with st.spinner("Searching..."):
        try:
            # Récupérer et chunker le transcript
            transcript_chunks = fetch_video_transcript(video_id, chunk_size=chunk_size)
            documents = build_document(transcript_chunks)

            # Rechercher les chunks correspondant à la query
            chunks = search_transcript_chunks(documents, query=query, k=1)

            # Afficher les résultats
            if chunks:
                url_video = "https://www.youtube.com/watch?v="
                with st.expander("Transcript Chunks"):
                    for idx, doc in enumerate(chunks, start=1):
                       with st.expander(f"Chunk {idx}"):
                           st.write(f"**Chunk {idx} [{doc.metadata['start']}s - {doc.metadata['end']}s]:**")
                           st.write(doc.page_content)
                           st.video(doc.metadata['url'], start_time=doc.metadata['start'],
                                    autoplay=True)

            else:
                st.info("No matching transcript chunks found.")

        except Exception as e:
            st.error(f"Error fetching or processing video transcript: {e}")
else:
    st.info("Please enter a YouTube video ID and a search query.")
