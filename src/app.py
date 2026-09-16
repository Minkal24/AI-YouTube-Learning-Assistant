import streamlit as st

from youtube_loader import extract_video_id
from vector_store import create_vector_store
from rag_chain import ask_question


# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="AI YouTube Learning Assistant",
    page_icon="🎥",
    layout="wide"
)


# Session State
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "video_id" not in st.session_state:
    st.session_state.video_id = None



# Title
# -----------------------------

st.title("🎥 AI YouTube Learning Assistant")

st.write(
    "Ask questions about any YouTube video using RAG."
)



# Sidebar
# -----------------------------

with st.sidebar:

    st.header("⚙️ Video Settings")

    video_input = st.text_input(
        "YouTube Video URL / ID",
        placeholder="Paste YouTube URL here..."
    )

    load_video = st.button(
        "📥 Load Video",
        use_container_width=True
    )

    clear_chat = st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    )

    if clear_chat:
        st.session_state.messages = []
        st.session_state.sources = []
        st.rerun()



# Load Video
# -----------------------------

if load_video:

    if not video_input:

        st.warning(
            "Please enter a YouTube Video URL or ID."
        )

    else:

        video_id = extract_video_id(video_input)

        if not video_id:

            st.error(
                "❌ Invalid YouTube Video ID or URL."
            )

        else:

            st.session_state.video_id = video_id

            with st.spinner(
                "Processing video... Please wait."
            ):

                vectorstore = create_vector_store(
                    video_id
                )

            if vectorstore:

                st.session_state.vectorstore = vectorstore
                st.session_state.messages = []

                st.success(
                    "✅ Video processed successfully!"
                )

            else:

                st.session_state.vectorstore = None

                st.error(
                    "❌ Could not load the transcript. "
                    "Please check the video or try another video."
                )


# Current Video
# -----------------------------

if st.session_state.video_id:

    st.info(
        f"🎬 Loaded Video ID: "
        f"{st.session_state.video_id}"
    )


# Chat History
# -----------------------------

for message in st.session_state.messages:

    if message["role"] == "user":

        with st.chat_message("user"):
            st.write(message["content"])

    else:

        with st.chat_message("assistant"):
            st.write(message["content"])




# -----------------------------
# Chat Input
# -----------------------------

question = st.chat_input(
    "Ask a question about the video..."
)


if question:

    if not st.session_state.vectorstore:

        st.warning(
            "Please load a video first."
        )

    else:

        # Create chat history BEFORE adding current question
        chat_history = "\n".join(
            f"{message['role']}: {message['content']}"
            for message in st.session_state.messages
        )

        # Save user question
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.spinner("🤖 Generating answer..."):

            answer, docs = ask_question(
                question,
                st.session_state.vectorstore,
                chat_history
            )

        # Save AI answer
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        # Save retrieved sources
        st.session_state.sources = docs

        st.rerun()


# -----------------------------
# Retrieved Sources
# -----------------------------

if st.session_state.get("sources"):

    st.subheader("📚 Retrieved Sources")

    for i, doc in enumerate(st.session_state.sources):
        with st.expander(f"Source {i + 1}"):
            st.write(doc.page_content)
