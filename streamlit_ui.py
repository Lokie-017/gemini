import os
import json
import streamlit as st
from datetime import datetime
from gemini_api import get_response, extract_text_from_pdf

# Try to load Firebase credentials from file if available
FIREBASE_CREDS_FILE = "firebase-credentials.json"
HAS_LOCAL_FIREBASE = os.path.exists(FIREBASE_CREDS_FILE)

# Page config
st.set_page_config(page_title="Gemini AI Assistant", layout="wide")

HISTORY_DIR = "user_histories"
HISTORY_FILE = "chat_history.json"  # Legacy global file

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


def ensure_user_history_dir():
    """Ensure user history directory exists."""
    if not os.path.exists(HISTORY_DIR):
        os.makedirs(HISTORY_DIR, exist_ok=True)


def get_user_history_path(user_id):
    """Get the chat history file path for a specific user."""
    ensure_user_history_dir()
    return os.path.join(HISTORY_DIR, f"chat_history_{user_id}.json")


def init_firebase():
    """Initialize Firebase if credentials are available."""
    try:
        import firebase_admin
        from firebase_admin import credentials, auth, db
        
        if firebase_admin._apps:
            return True, None
        
        # Try loading from local file
        if HAS_LOCAL_FIREBASE:
            with open(FIREBASE_CREDS_FILE, "r") as f:
                creds_dict = json.load(f)
            cred = credentials.Certificate(creds_dict)
            firebase_admin.initialize_app(cred, {
                'databaseURL': creds_dict.get('database_url', ''),
            })
            return True, None
        else:
            return False, "Firebase credentials file not found"
    except Exception as e:
        return False, str(e)


def load_knowledge_base(path="knowledge_base.json"):
    """Load knowledge base from JSON file."""
    if not os.path.exists(path):
        return ""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return json.dumps(data, indent=2, ensure_ascii=False)
    except Exception:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()


def load_chat_history(user_id=None, path=None):
    """Load chat history from file.
    
    If user_id is provided, loads user-specific history.
    If path is provided, uses that path instead.
    Falls back to global history file if neither is provided.
    """
    if path is None:
        if user_id:
            path = get_user_history_path(user_id)
        else:
            path = HISTORY_FILE
    
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def load_user_history_from_firebase(uid):
    """Load user's conversation history from Firebase database."""
    try:
        from firebase_admin import db
        snapshot = db.reference(f'users/{uid}/conversations').get()
        
        # Check if snapshot exists first
        if snapshot is None:
            return []
        
        conversations = snapshot.val()
        if not conversations:
            return []
        
        # Convert dict to list of conversations
        conv_list = []
        for timestamp, conv in conversations.items():
            conv['timestamp'] = timestamp
            conv_list.append(conv)
        
        # Sort by timestamp (newest first)
        conv_list.sort(key=lambda x: x['timestamp'], reverse=True)
        st.info(f"✓ Loaded {len(conv_list)} conversations from Firebase")
        return conv_list
    except Exception as e:
        st.error(f"Firebase load failed: {e}")
        return []


def save_user_history_to_firebase(uid, conversation):
    """Save a single conversation to user's Firebase profile."""
    try:
        from firebase_admin import db
        timestamp = datetime.now().isoformat()
        # Store without timestamp in data (timestamp is the key)
        data = {
            "prompt": conversation.get("prompt", ""),
            "response": conversation.get("response", ""),
            "mode": conversation.get("mode", "chat"),
            "language": conversation.get("language", "en"),
        }
        path = f'users/{uid}/conversations/{timestamp}'
        db.reference(path).set(data)
        st.info(f"✓ Saved to Firebase: {uid}")
        return True
    except Exception as e:
        st.error(f"Firebase save failed: {e}")
        return False



def save_chat_history(history, user_id=None, path=None):
    """Save chat history to file.
    
    If user_id is provided, saves to user-specific file.
    If path is provided, uses that path instead.
    Falls back to global history file if neither is provided.
    """
    if path is None:
        if user_id:
            path = get_user_history_path(user_id)
        else:
            path = HISTORY_FILE
    
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception as e:
        st.error(f"Error saving history: {e}")



def firebase_login(email, password):
    """Authenticate with Firebase."""
    try:
        from firebase_admin import auth
        user = auth.get_user_by_email(email)
        # Note: admin SDK can't verify passwords directly
        # This simulates a login - in production use REST API
        return True, user.uid, user.display_name or email.split('@')[0]
    except Exception as e:
        return False, None, str(e)


def firebase_signup(email, password, display_name=""):
    """Create Firebase user."""
    try:
        from firebase_admin import auth, db
        user = auth.create_user(email=email, password=password, display_name=display_name)
        # Create user profile
        db.reference(f'users/{user.uid}/profile').set({
            'email': email,
            'display_name': display_name or email.split('@')[0],
            'created_at': datetime.now().isoformat(),
        })
        return True, user.uid, None
    except Exception as e:
        return False, None, str(e)


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


def show_login_page():
    """Display login/signup interface."""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🔐 Gemini AI")
        st.markdown("---")
        
        # Check Firebase status
        firebase_ok, firebase_error = init_firebase()
        
        if not firebase_ok:
            st.info("📂 Firebase not configured - using guest mode")
            st.write(f"Status: {firebase_error}")
            
            if st.button("🚀 Continue as Guest", use_container_width=True, type="primary"):
                st.session_state.user_id = "guest"
                st.session_state.user_name = "Guest"
                st.session_state.user_email = "guest@local"
                st.session_state.firebase_enabled = False
                st.rerun()
            return
        
        # Firebase is available
        st.session_state.firebase_enabled = True
        
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            st.subheader("Login")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_pwd")
            
            if st.button("Login", use_container_width=True, type="primary"):
                if email and password:
                    success, uid, name_or_error = firebase_login(email, password)
                    if success:
                        st.session_state.user_id = uid
                        st.session_state.user_name = name_or_error
                        st.session_state.user_email = email
                        st.session_state.firebase_enabled = True
                        st.success(f"Welcome {name_or_error}!")
                        st.rerun()
                    else:
                        st.error(f"Login failed: {name_or_error}")
        
        with tab2:
            st.subheader("Create Account")
            new_email = st.text_input("Email", key="signup_email")
            new_name = st.text_input("Display Name", key="signup_name")
            new_pwd = st.text_input("Password", type="password", key="signup_pwd")
            new_pwd_confirm = st.text_input("Confirm Password", type="password", key="signup_pwd2")
            
            if st.button("Sign Up", use_container_width=True):
                if not new_email or not new_pwd:
                    st.error("Email and password required")
                elif new_pwd != new_pwd_confirm:
                    st.error("Passwords don't match")
                elif len(new_pwd) < 6:
                    st.error("Password must be 6+ characters")
                else:
                    success, uid, error = firebase_signup(new_email, new_pwd, new_name)
                    if success:
                        st.success("Account created! Please login.")
                        st.rerun()
                    else:
                        st.error(f"Signup failed: {error}")


def main():
    st.title("🚀 Gemini AI Assistant")
    
    # Initialize session
    if "user_id" not in st.session_state:
        show_login_page()
        return
    
    if "pdf_text" not in st.session_state:
        st.session_state.pdf_text = ""
    if "pdf_name" not in st.session_state:
        st.session_state.pdf_name = ""
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    if "firebase_enabled" not in st.session_state:
        st.session_state.firebase_enabled = st.session_state.user_id != "guest"
    if "history" not in st.session_state:
        # Load user's history from Firebase if not guest
        firebase_ok = st.session_state.user_id != "guest"
        if firebase_ok:
            history = load_user_history_from_firebase(st.session_state.user_id)
            st.session_state.history = history if history else []
        else:
            # Load local per-user history file
            st.session_state.history = load_chat_history(user_id=st.session_state.user_id)

    # Sidebar
    with st.sidebar:
        # User Info
        user_type = "👤 " if st.session_state.user_id != "guest" else "👥 "
        st.write(f"{user_type}**{st.session_state.user_name}**")
        st.caption(st.session_state.user_email)
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()
        
        st.divider()
        st.header("⚙️ Settings")
        st.divider()
        
        # Language
        st.subheader("Language")
        selected_lang = st.selectbox("Response language:", list(LANGUAGES.keys()), index=0)
        language_code = LANGUAGES[selected_lang]
        
        # Mode
        st.subheader("Mode")
        selected_mode = st.selectbox("Conversation mode:", list(MODES.keys()), index=0)
        mode = MODES[selected_mode]
        
        st.divider()
        
        # Cloud History for authenticated users
        if st.session_state.user_id != "guest" and st.session_state.firebase_enabled:
            with st.expander("☁️ Cloud History"):
                st.caption(f"Saved to Firebase: {st.session_state.user_email}")
                cloud_convs = load_user_history_from_firebase(st.session_state.user_id)
                if cloud_convs:
                    st.info(f"✓ {len(cloud_convs)} conversations in cloud")
                    for i, conv in enumerate(cloud_convs[:5]):
                        ts = conv.get('timestamp', '')[:10]
                        prompt = conv.get('prompt', '')[:45]
                        st.caption(f"{i+1}. {ts}: {prompt}")
                else:
                    st.caption("No conversations yet")
        
        st.divider()
        
        # Debug Panel
        with st.expander("🔧 Firebase Debug"):
            st.write(f"User ID: `{st.session_state.user_id}`")
            st.write(f"Firebase Enabled: `{st.session_state.firebase_enabled}`")
            
            if st.button("🔄 Reload from Firebase", key="reload_firebase"):
                history = load_user_history_from_firebase(st.session_state.user_id)
                st.session_state.history = history if history else []
                st.rerun()
            
            if st.button("📤 View Raw Firebase Data", key="view_firebase"):
                try:
                    from firebase_admin import db
                    snapshot = db.reference(f'users/{st.session_state.user_id}/conversations').get()
                    if snapshot.val():
                        st.json(snapshot.val())
                    else:
                        st.warning("No data in Firebase for this user")
                except Exception as e:
                    st.error(f"Error reading Firebase: {e}")
        
        st.divider()
        
        if st.button("🔄 Reset Chat", use_container_width=True):
            st.session_state.history = []
            save_chat_history([], user_id=st.session_state.user_id)
            st.success("✓ Cleared")
            st.rerun()

    # Main Area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📚 Knowledge Base")
        kb = st.text_area("Add context:", value=load_knowledge_base(), height=100)
    
    with col2:
        st.subheader("📄 PDF")
        pdf_file = st.file_uploader("Upload PDF", type="pdf")
        if st.button("Clear", use_container_width=True):
            st.session_state.pdf_text = ""
            st.session_state.pdf_name = ""
            st.rerun()

    # Process PDF
    if pdf_file:
        try:
            with st.spinner("Loading..."):
                st.session_state.pdf_text = extract_text_from_pdf(pdf_file)
                st.session_state.pdf_name = pdf_file.name
            st.success(f"✓ {pdf_file.name}")
        except Exception as e:
            st.error(f"Error: {e}")
    elif st.session_state.pdf_text:
        st.info(f"Using: {st.session_state.pdf_name}")

    # Chat
    st.subheader("💬 Chat")
    prompt = st.text_area("Your message:", height=100)
    
    send = st.button("🚀 Send", use_container_width=True, type="primary")
    
    if send and prompt.strip():
        # Build prompt
        full_prompt = get_mode_instruction(mode)
        if kb.strip():
            full_prompt += f"\n\nContext:\n{kb}\n\n"
        if st.session_state.pdf_text:
            full_prompt += f"\n\nPDF:\n{st.session_state.pdf_text}\n\n"
        full_prompt += prompt + get_language_instruction(language_code)
        
        try:
            with st.spinner("Getting response..."):
                response = get_response(full_prompt)
            
            # Save entry
            entry = {
                "timestamp": datetime.now().isoformat(),
                "prompt": prompt,
                "response": response,
                "mode": mode,
                "language": language_code,
            }
            st.session_state.history.insert(0, entry)
            
            # Save to Firebase if available, otherwise save to per-user file
            if st.session_state.user_id != "guest" and st.session_state.firebase_enabled:
                save_user_history_to_firebase(st.session_state.user_id, entry)
            else:
                # Save to per-user local file
                save_chat_history(st.session_state.history, user_id=st.session_state.user_id)
            
            st.success("✓ Saved")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")

    # History
    if st.session_state.history:
        st.divider()
        st.subheader("📜 History")
        
        for i, h in enumerate(st.session_state.history[:10]):
            timestamp = h.get("timestamp", "")[:16]
            preview = h["prompt"][:40]
            with st.expander(f"#{i+1} ({timestamp}) - {preview}"):
                st.write("**Q:** " + h["prompt"])
                st.write("**A:** " + h["response"])

    # Export
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.history:
            st.download_button(
                "📥 Export",
                data=json.dumps(st.session_state.history, ensure_ascii=False, indent=2),
                file_name="history.json",
                mime="application/json",
                use_container_width=True
            )
    
    with col2:
        if st.session_state.history:
            if st.button("🗑️ Delete All", use_container_width=True):
                st.session_state.history = []
                save_chat_history([], user_id=st.session_state.user_id)
                st.rerun()


if __name__ == "__main__":
    main()
