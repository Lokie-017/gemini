import os
import json
import streamlit as st
from datetime import datetime

from gemini_api import get_response

api_key = os.getenv("GEMINI_API_KEY") or st.secrets["GEMINI_API_KEY"]

HISTORY_FILE = "chat_history.json"

LANGUAGES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese": "zh",
    "Japanese": "ja",
    "Portuguese": "pt",
    "Russian": "ru",
}

MODES = {
    "Chat": "chat",
    "Q&A": "qa",
    "Analysis": "analysis",
}


def load_knowledge_base(path="knowledge_base.json"):
    if not os.path.exists(path):
        return ""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Pretty-print JSON for editing/viewing
            return json.dumps(data, indent=2, ensure_ascii=False)
    except Exception:
        # Fallback: return raw file content
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()


def load_chat_history(path=HISTORY_FILE):
    """Load chat history from file, return empty list if file doesn't exist."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.warning(f"Failed to load chat history from {path}: {e}")
        return []


def save_chat_history(history, path=HISTORY_FILE):
    """Save chat history to file."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception as e:
        st.error(f"Failed to save chat history to {path}: {e}")


def get_mode_instruction(mode):
    """Return system instruction based on mode."""
    instructions = {
        "chat": "You are a helpful, conversational AI assistant. Keep responses friendly and engaging.",
        "qa": "You are a Q&A expert. Provide clear, concise, direct answers to questions. Focus on accuracy and brevity.",
        "analysis": "You are an analytical expert. Provide deep, thorough analysis with data-driven insights and detailed explanations.",
    }
    return instructions.get(mode, instructions["chat"])


def get_language_instruction(language_code):
    """Return instruction to respond in a specific language."""
    if language_code == "en":
        return ""
    lang_names = {v: k for k, v in LANGUAGES.items()}
    return f"\n\nRespond in {lang_names.get(language_code, 'English')}."


def main():
    st.set_page_config(page_title="Gemini UI", layout="wide")
    st.title("Gemini Streamlit UI")

    st.sidebar.header("Settings")
    st.sidebar.markdown(
        "Ensure `GEMINI_API_KEY` is set in your environment before running this app.\n\n"
        "This app calls `get_response(prompt)` from `gemini_api.py`."
    )

    # Initialize session state for language and mode
    if "language" not in st.session_state:
        st.session_state.language = "en"
    if "mode" not in st.session_state:
        st.session_state.mode = "chat"

    # Sidebar controls
    st.sidebar.subheader("Language")
    selected_lang = st.sidebar.selectbox(
        "Choose response language:",
        options=list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index(next(k for k, v in LANGUAGES.items() if v == st.session_state.language))
    )
    st.session_state.language = LANGUAGES[selected_lang]

    st.sidebar.subheader("Interaction Mode")
    selected_mode = st.sidebar.selectbox(
        "Choose conversation mode:",
        options=list(MODES.keys()),
        index=list(MODES.keys()).index(next(k for k, v in MODES.items() if v == st.session_state.mode))
    )
    st.session_state.mode = MODES[selected_mode]

    st.sidebar.subheader("Reset")
    if st.sidebar.button("🔄 Reset Chat", use_container_width=True):
        st.session_state.history = []
        save_chat_history([])
        st.sidebar.success("✓ Chat reset successfully!")
        st.rerun()

    kb_text = load_knowledge_base()

    st.subheader("Knowledge Base (editable)")
    kb = st.text_area("Edit knowledge/context used with queries:", value=kb_text, height=200)

    st.subheader("Ask Gemini")
    prompt = st.text_area("Your question:", height=120)

    col1, col2 = st.columns([1, 3])
    with col1:
        send = st.button("Send")
    with col2:
        st.write("")

    # Load history from file on first app run
    if "history" not in st.session_state:
        st.session_state.history = load_chat_history()

    if send and prompt.strip():
        # Build the full prompt with knowledge base, mode, and language instructions
        mode_instruction = get_mode_instruction(st.session_state.mode)
        lang_instruction = get_language_instruction(st.session_state.language)
        full_prompt = f"{mode_instruction}\n\n" if mode_instruction else ""
        if kb:
            full_prompt += kb + "\n\n"
        full_prompt += prompt + lang_instruction
        
        try:
            with st.spinner("Waiting for Gemini response..."):
                resp = get_response(full_prompt)
        except Exception as e:
            st.error(f"Error calling Gemini: {e}")
            resp = None

        if resp is not None:
            entry = {
                "timestamp": datetime.now().isoformat(),
                "prompt": prompt,
                "response": resp,
                "mode": st.session_state.mode,
                "language": st.session_state.language,
            }
            st.session_state.history.insert(0, entry)
            # Save history to file after each new response
            save_chat_history(st.session_state.history)
            st.success("✓ Response saved to chat history!")

    if st.session_state.history:
        st.subheader("Conversation History")
        for i, h in enumerate(st.session_state.history[:20]):
            timestamp_str = h.get("timestamp", "Unknown")
            prompt_preview = h["prompt"][:60]
            mode_badge = h.get("mode", "chat").upper()
            lang_code = h.get("language", "en")
            lang_name = next((k for k, v in LANGUAGES.items() if v == lang_code), "Unknown")
            with st.expander(f"Turn {i+1} ({timestamp_str}) | Mode: {mode_badge} | Lang: {lang_name} | {prompt_preview}"):
                st.markdown("**Prompt**")
                st.write(h["prompt"])
                st.markdown("**Response**")
                st.write(h["response"])

    st.sidebar.subheader("Export & Manage")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.session_state.history:
            st.download_button(
                label="📥 Download JSON",
                data=json.dumps(st.session_state.history, ensure_ascii=False, indent=2),
                file_name="conversation_history.json",
                mime="application/json",
                use_container_width=True,
            )
    with col2:
        if st.session_state.history:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.history = []
                save_chat_history([])
                st.rerun()


if __name__ == "__main__":
    main()
