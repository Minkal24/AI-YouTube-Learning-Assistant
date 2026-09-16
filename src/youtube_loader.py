from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url_or_id: str)->str:
  """Extract YouTube video ID from a URL or return the ID directly."""

  if "youtube.com/watch?v=" in url_or_id:
    return url_or_id.split("v=")[1].split("&")[0]

  if "youtu.be/" in url_or_id:
    return url_or_id.split("youtu.be/")[1].split("?")[0]

  return url_or_id.strip()


def load_youtube_transcript(video_id: str)->str:
  """Fetch the English or Hindi transcript of a YouTube video."""
  try:
    api = YouTubeTranscriptApi()
    transcript = api.fetch(
      video_id ,languages=['en',"hi"]
    )

    text = " ".join(snippet.text for snippet in transcript)

    return text

  except Exception as e:
    print("error: ", e)
    return ""

if __name__ == "__main__":
  video_input = input("Enter YouTube Video ID or URL: ")

  video_id = extract_video_id(video_input)

  text = load_youtube_transcript(video_id)

  if text:
    print("\nTranscript loaded successfully")
    print("Characters: ", len(text))
    print("\nFirst 500 charaters: ")
    print(text[:500])
