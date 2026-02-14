import os
import json
import streamlit as st

from gemini_api import get_response


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


def main():
    st.set_page_config(page_title="Gemini UI", layout="wide")
    st.title("Gemini Streamlit UI")

    st.sidebar.header("Settings")
    st.sidebar.markdown(
        "Ensure `GEMINI_API_KEY` is set in your environment before running this app.\n\n"
        "This app calls `get_response(prompt)` from `gemini_api.py`."
    )

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

    if "history" not in st.session_state:
        st.session_state.history = []

    if send and prompt.strip():
        full_prompt = kb + "\n\n" + prompt if kb else prompt
        try:
            with st.spinner("Waiting for Gemini response..."):
                resp = get_response(full_prompt)
        except Exception as e:
            st.error(f"Error calling Gemini: {e}")
            resp = None

        if resp is not None:
            entry = {"prompt": prompt, "response": resp}
            st.session_state.history.insert(0, entry)

    if st.session_state.history:
        st.subheader("Conversation History")
        for i, h in enumerate(st.session_state.history[:20]):
            with st.expander(f"Turn {i+1}: {h['prompt'][:60]}"):
                st.markdown("**Prompt**")
                st.write(h["prompt"])
                st.markdown("**Response**")
                st.write(h["response"])

    st.sidebar.subheader("Export")
    if st.session_state.history:
        if st.sidebar.button("Download history as JSON"):
            st.sidebar.download_button(
                label="Download",
                data=json.dumps(st.session_state.history, ensure_ascii=False, indent=2),
                file_name="conversation_history.json",
                mime="application/json",
            )


if __name__ == "__main__":
    main()
