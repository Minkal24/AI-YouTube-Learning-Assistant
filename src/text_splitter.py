from youtube_loader import load_youtube_transcript
from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(video_id:str):
  text = load_youtube_transcript(video_id)

  if not text:
    return []

  text_splitter = RecursiveCharacterTextSplitter(
  chunk_size =2000,
  chunk_overlap = 200
  )

  chunks = text_splitter.create_documents([text])

  return chunks




