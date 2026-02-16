# 🚀 Gemini AI Assistant - Complete Project Overview

## Project Description

A multilingual AI-powered assistant built with Google's Gemini API, Firebase authentication, and Streamlit UI. The system supports per-user chat history, PDF processing, multiple conversation modes, and comprehensive analytics through a dedicated dashboard.

## 🏗️ Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit UI Layer                      │
├─────────────────────────────────────────────────────────────┤
│  streamlit_ui.py         │  dashboard.py                    │
│  (Chat Interface)        │  (Analytics & Monitoring)        │
└──────────┬───────────────┴──────────────────┬───────────────┘
           │                                  │
           └──────────────┬───────────────────┘
                          │
    ┌─────────────────────┴──────────────────┬────────────────┐
    │                                        │                 │
┌───▼──────────────┐              ┌──────────▼─────┐   ┌────────▼──┐
│   Gemini API     │              │    Firebase    │   │   Local   │
│  gemini_api.py   │              │  firebase_auth │   │ Storage   │
│                  │              │    .py         │   │           │
│ • Text Gen       │              │                │   │ • User    │
│ • PDF Parse      │              │ • Auth         │   │   History │
│ • Multi-lang     │              │ • Database     │   │ • KB      │
└────────────────────┘              └─────────────────┘   └──────────┘
```

## 📁 Project Structure

```
google_api/
├── 📄 Main Files
│   ├── main.py                      # CLI version
│   ├── streamlit_ui.py              # Main Streamlit chat application
│   └── dashboard.py                 # Analytics dashboard
│
├── 🔧 Core Modules
│   ├── gemini_api.py                # Gemini API integration
│   └── firebase_auth.py             # Firebase authentication & DB
│
├── 📦 Configuration & Data
│   ├── firebase-credentials.json     # Firebase config (gitignored)
│   ├── knowledge_base.json           # AI context data
│   ├── chat_history.json             # Legacy global history
│   └── requirements.txt              # Python dependencies
│
├── 📚 Documentation
│   ├── FIREBASE_SETUP.md             # Firebase configuration guide
│   ├── FIREBASE_QUICKSTART.md        # Quick setup reference
│   ├── DASHBOARD.md                  # Dashboard documentation
│   └── PROJECT_OVERVIEW.md           # This file
│
├── 💾 Runtime Directories
│   ├── user_histories/               # Per-user chat history files
│   │   ├── chat_history_guest.json
│   │   ├── chat_history_user123.json
│   │   └── ...
│   └── __pycache__/                  # Python bytecode cache
│
└── 🔗 Version Control
    └── .git/                         # Git repository
```

## 🔑 Key Features

### 1. **Multi-Personality Chat** 
- **Chat Mode**: Conversational and friendly responses
- **Q&A Mode**: Direct, concise answers
- **Analysis Mode**: Deep, data-driven insights

### 2. **Multilingual Support**
- 8 languages: English, Spanish, French, German, Chinese, Japanese, Portuguese, Russian
- Automatic language detection and response adaptation
- Per-conversation language setting

### 3. **User Management**
- Firebase email/password authentication
- Per-user chat history isolation
- User profiles with metadata
- Guest mode for unauthenticated access

### 4. **Knowledge Base**
- Customizable context for all conversations
- Real-time editing in UI
- Supports college/organization data
- Embedded in Gemini prompts

### 5. **PDF Processing**
- PDF upload and text extraction
- Context integration with conversations
- Multiple file format support
- Full-page or selective processing

### 6. **Chat History Management**
- Per-user local JSON storage (`user_histories/`)
- Firebase cloud storage (for authenticated users)
- Searchable conversation logs
- Export capabilities

### 7. **Analytics Dashboard**
- Real-time statistics and metrics
- User activity tracking
- Language and mode usage breakdown
- System health monitoring
- Data export functionality

## 📊 Data Flow

### Chat Conversation Flow
```
User Input
    ↓
Mode Selection (Chat/Q&A/Analysis)
    ↓
Language Setting
    ↓
Create Prompt with Context
    ├─ Knowledge Base
    ├─ User Message
    ├─ Conversation History
    └─ PDF (optional)
    ↓
Send to Gemini API
    ↓
Receive Response
    ↓
Save to History
    ├─ Local file: user_histories/chat_history_{user_id}.json
    └─ Firebase: users/{uid}/conversations/{timestamp}
    ↓
Display to User
```

### Authentication Flow
```
User Action
    ↓
┌───────────────────────────┐
│ Firebase Available?       │
└─────────┬────────┬────────┘
          Yes      No
          │        │
    Firebase    Guest Mode
    Auth        Local File
    │           │
    │           └─→ user_histories/chat_history_guest.json
    │
    Users/{uid}/
    profile/
    conversations/
```

## 🔌 Core Modules

### `gemini_api.py`
**Purpose**: Handle Gemini API communication
```python
get_client()              # Initialize Gemini client
get_response(prompt)      # Get AI response
extract_text_from_pdf()   # Parse PDF files
```

### `firebase_auth.py`
**Purpose**: Handle Firebase operations
```python
initialize_firebase()              # Setup Firebase app
firebase_login(email, password)    # User login
firebase_signup(email, pwd, name)  # User registration
load_user_history_from_firebase()  # Get cloud conversations
save_user_history_to_firebase()    # Save to cloud
```

### `streamlit_ui.py`
**Purpose**: Web interface and main application logic
```python
show_login_page()              # Authentication UI
load_chat_history(user_id)     # Load per-user history
save_chat_history(user_id)     # Save per-user history
get_response(prompt)           # Process user input
main()                         # Application entry point
```

### `dashboard.py`
**Purpose**: Analytics and monitoring
```python
calculate_stats()              # Compute metrics
get_recent_conversations()     # Fetch latest chats
show_user_management()         # User analytics
show_export_section()          # Data export
```

## 🚀 Getting Started

### 1. Installation
```bash
# Clone repository
git clone <repo-url>
cd google_api

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

#### Set Gemini API Key
```bash
# Windows
set GEMINI_API_KEY=your_api_key_here

# Linux/Mac
export GEMINI_API_KEY=your_api_key_here
```

#### Setup Firebase (Optional)
1. Create Firebase project at [console.firebase.google.com](https://console.firebase.google.com)
2. Download credentials JSON
3. Save as `firebase-credentials.json` in project root
4. See [FIREBASE_SETUP.md](FIREBASE_SETUP.md) for detailed instructions

### 3. Run Applications

#### Chat Application
```bash
streamlit run streamlit_ui.py
# Opens at http://localhost:8501
```

#### CLI Version
```bash
python main.py
```

#### Dashboard
```bash
python run_dashboard.py
# Or: streamlit run dashboard.py
# Opens at http://localhost:8502
```

## 📋 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| google-genai | latest | Gemini API client |
| streamlit | >= 1.0 | Web UI framework |
| pypdf | latest | PDF text extraction |
| firebase-admin | latest | Firebase services |

See `requirements.txt` for exact versions.

## 💾 Storage Architecture

### Local Storage
**Location**: `user_histories/`
**Format**: JSON files per user
**Structure**:
```json
[
  {
    "timestamp": "2026-02-15T12:31:18.913135",
    "prompt": "What is the HOD of CSE?",
    "response": "The HOD of CSE is Dr. Ramesh Kumar.",
    "mode": "chat",
    "language": "en"
  },
  ...
]
```

**Pros**:
- No cloud dependency
- Fast local access
- Works offline
- Easy backup

**Cons**:
- Not synced across devices
- Limited to single machine

### Firebase Storage
**Path**: `users/{uid}/conversations/{timestamp}`
**Format**: Each timestamp key contains a conversation object
**Scope**:
- Authenticated users only
- Real-time sync
- Cloud backup

**Pros**:
- Multi-device sync
- Cloud backup
- Scalable
- Real-time updates

**Cons**:
- Requires authentication
- Network dependent
- Firebase costs

## 🔐 Security

### Authentication
- Firebase handles password hashing
- Email verification ready
- Session management via Streamlit

### Data Privacy
- Per-user isolated histories
- No shared conversation data
- Local fallback for offline use

### Best Practices
1. Never commit `firebase-credentials.json`
2. Keep `GEMINI_API_KEY` in environment
3. Use HTTPS in production
4. Implement rate limiting
5. Regular backups of `user_histories/`

## 📊 Dashboard Metrics

### Available Analytics
- **User Metrics**: Total users, active today, new users
- **Conversation Metrics**: Total conversations, messages per user
- **Language Analytics**: Distribution by language
- **Mode Analytics**: Usage of different conversation modes
- **Response Metrics**: Average response length, token usage
- **System Status**: Firebase connection, storage usage

### Exports
- JSON format for all data
- Timestamp-based naming
- Preserves structure for analysis

## 🔄 Workflow Examples

### Example 1: New User Chat
```
1. User signs up with email/password
2. Firebase creates user record
3. First message is sent
4. Response saved to 3 places:
   - Session memory
   - Local file: user_histories/chat_history_{uid}.json
   - Firebase: users/{uid}/conversations/{timestamp}
5. Dashboard updates automatically
```

### Example 2: Guest Chat
```
1. User clicks "Guest" button
2. Session ID = "guest"
3. Chat proceeds normally
4. History saved to:
   - user_histories/chat_history_guest.json
5. Clears on logout (unless configured otherwise)
```

### Example 3: PDF Analysis
```
1. User uploads PDF
2. System extracts text
3. Text added to prompt context
4. Conversation includes PDF context
5. Responses reference PDF content
6. Entire exchange saved with PDF flag
```

## 🐛 Troubleshooting

### "GEMINI_API_KEY not set"
```bash
# Set the environment variable and restart
echo $GEMINI_API_KEY  # Verify it's set
```

### Firebase "Permission Denied"
1. Check database rules in Firebase Console
2. Verify user is authenticated
3. Check UID matches in database path

### "chat_history.json not found"
- This is normal on first run
- Will be created automatically
- Or use per-user files instead

### Dashboard shows no data
1. Ensure conversations have been created
2. Check `user_histories/` directory exists
3. Verify JSON file format is correct

## 📈 Performance Optimization

### Current Optimizations
- Lazy Firebase initialization
- Client-side session caching
- Local file operations
- Streamlit widget memoization

### Potential Improvements
1. Implement conversation pagination
2. Add search indexing
3. Cache Gemini responses
4. Background history sync
5. Database query optimization

## 🔮 Future Enhancements

- [ ] Voice input/output
- [ ] Image processing
- [ ] Advanced search
- [ ] Conversation threading
- [ ] User ratings/feedback
- [ ] API rate limiting
- [ ] Advanced analytics
- [ ] Mobile app
- [ ] Team collaboration
- [ ] Custom knowledge base management UI

## 📝 Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| GEMINI_API_KEY | Gemini API authentication | `abc123...` |
| FIREBASE_CREDENTIALS_JSON | Firebase credentials (optional) | JSON string |

## 🤝 Contributing

1. Create feature branch
2. Make changes to appropriate module
3. Update documentation
4. Test in dashboard
5. Commit with clear message

## 📄 License

[Add your license here]

## 📞 Support

- **Firebase Issues**: See [FIREBASE_SETUP.md](FIREBASE_SETUP.md)
- **Dashboard Help**: See [DASHBOARD.md](DASHBOARD.md)
- **API Issues**: Check Gemini API documentation

## 🎯 Quick Reference

| Task | File | Function |
|------|------|----------|
| Chat | streamlit_ui.py | main() |
| Dashboard | dashboard.py | main() |
| API | gemini_api.py | get_response() |
| Auth | firebase_auth.py | firebase_login() |
| History | streamlit_ui.py | load_chat_history() |

---

**Last Updated**: February 15, 2026
**Version**: 1.0.0
**Status**: Production Ready
