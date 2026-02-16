# 🚀 Gemini AI Assistant

A multilingual AI-powered assistant built with Google's Gemini API, Firebase authentication, and Streamlit. Features per-user chat history, PDF processing, multiple conversation modes, and comprehensive analytics.

## ✨ Features

- **AI-Powered Chat**: Powered by Google's Gemini API with advanced language understanding
- **User Authentication**: Secure Firebase authentication with email/password support
- **PDF Processing**: Extract and analyze content from PDF documents
- **Multilingual Support**: Communicate in multiple languages
- **Chat History**: Persistent per-user conversation history with Firebase database
- **Knowledge Base**: Integrated knowledge base for enhanced context
- **Analytics Dashboard**: Real-time metrics and user analytics
- **Multiple Modes**: Support for different conversation modes and use cases

## 🏗️ Architecture

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
├── 📄 Core Applications
│   ├── main.py                      # CLI version
│   ├── streamlit_ui.py              # Main Streamlit chat application
│   ├── dashboard.py                 # Analytics dashboard
│   └── run_dashboard.py             # Dashboard launcher script
│
├── 🔧 Core Modules
│   ├── gemini_api.py                # Gemini API integration & PDF processing
│   └── firebase_auth.py             # Firebase authentication & database
│
├── 📦 Configuration & Data
│   ├── firebase-credentials.json     # Firebase config (⚠️ keep private)
│   ├── knowledge_base.json           # AI context and knowledge data
│   ├── chat_history.json             # Chat history storage
│   └── requirements.txt              # Python dependencies
│
└── 📚 Documentation
    ├── README.md                     # This file
    ├── QUICKSTART.md                 # Quick setup guide
    ├── PROJECT_OVERVIEW.md           # Detailed project documentation
    ├── FIREBASE_SETUP.md             # Firebase configuration guide
    └── FIREBASE_QUICKSTART.md        # Firebase quick reference
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)
- Firebase account (optional, for authentication features)

### Installation

1. **Clone or download** this repository

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Gemini API Key**:
   ```powershell
   # Windows PowerShell
   $env:GEMINI_API_KEY = "your_api_key_here"
   ```
   ```bash
   # Linux/Mac
   export GEMINI_API_KEY=your_api_key_here
   ```

4. **Run the Chat Application**:
   ```bash
   streamlit run streamlit_ui.py
   ```
   Opens at `http://localhost:8501`

5. **Run the Dashboard** (in a separate terminal):
   ```bash
   streamlit run dashboard.py
   ```
   Opens at `http://localhost:8502`

## 📊 Dashboard Features

The analytics dashboard provides:

- **Total Users & Conversations**: Track overall usage metrics
- **Active Users Today**: Real-time user activity monitoring
- **Language Distribution**: See which languages are being used
- **Conversation Modes**: Monitor usage of different conversation modes
- **System Status**: Check Firebase and local storage health
- **Recent Activity Feed**: View recent user interactions
- **User Management**: Manage and monitor user accounts

## 🔐 Firebase Setup (Optional)

For persistent authentication and cloud database features:

1. Create a Firebase project at [Firebase Console](https://console.firebase.google.com)
2. Enable Email/Password authentication
3. Set up Realtime Database
4. Download service account credentials as `firebase-credentials.json`
5. Place `firebase-credentials.json` in the project root

See [FIREBASE_SETUP.md](FIREBASE_SETUP.md) for detailed instructions.

## 📖 Usage

### Chat Application

1. Open the Streamlit UI (`http://localhost:8501`)
2. Authenticate with Firebase credentials (if configured)
3. Start a conversation with the AI
4. Upload PDFs for analysis (if available)
5. Switch languages as needed
6. View chat history

### CLI Application

```bash
python main.py
```

Runs the command-line version of the AI assistant.

## 🔧 Configuration

### Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `FIREBASE_PROJECT_ID`: Firebase project ID (optional)
- `FIREBASE_DATABASE_URL`: Firebase database URL (optional)

### Knowledge Base

Edit `knowledge_base.json` to customize the AI's context and behavior.

### Chat History

- Local storage: `chat_history.json`
- Cloud storage: Firebase Realtime Database (when configured)

## 📚 Module Documentation

### `gemini_api.py`
Handles all interactions with Google's Gemini API:
- Text generation
- PDF document parsing
- Language support
- Context management

### `firebase_auth.py`
Manages Firebase operations:
- User authentication
- Database operations
- User session management
- Cloud storage integration

### `streamlit_ui.py`
Main user interface:
- Chat interface
- File upload and processing
- User authentication
- History management

### `dashboard.py`
Analytics and monitoring:
- Usage metrics
- User analytics
- System health monitoring
- Activity tracking

## 🐛 Troubleshooting

### API Key Issues
- Ensure `GEMINI_API_KEY` environment variable is set correctly
- Verify key is active at [Google AI Studio](https://aistudio.google.com/apikey)

### Firebase Connection Issues
- Check `firebase-credentials.json` exists and is valid
- Verify Firebase project is properly configured
- Check database rules allow access

### Streamlit Issues
- Clear browser cache: `CTRL+SHIFT+DEL`
- Restart Streamlit: `CTRL+C` and run command again
- Check port availability (default: 8501 for UI, 8502 for dashboard)

## 📋 Requirements

See [requirements.txt](requirements.txt) for the complete list of dependencies:
- `google-genai`: Google Gemini API client
- `streamlit`: Web UI framework
- `pypdf`: PDF document processing
- `firebase-admin`: Firebase integration

## 📄 Documentation

- [QUICKSTART.md](QUICKSTART.md) - 5-minute quick start guide
- [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) - Detailed architecture and features
- [FIREBASE_SETUP.md](FIREBASE_SETUP.md) - Complete Firebase configuration guide
- [FIREBASE_QUICKSTART.md](FIREBASE_QUICKSTART.md) - Firebase quick reference

## 🔒 Security Notes

- Never commit `firebase-credentials.json` to version control
- Keep API keys private and use environment variables
- Use Firebase security rules for production deployments
- Regularly rotate credentials and keys

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs and issues
- Suggest new features
- Improve documentation
- Submit pull requests

## 📝 License

This project is provided as-is for personal and educational use.

## 💡 Support

For issues and questions:
1. Check the documentation files in this repository
2. Review the troubleshooting section above
3. Check Firebase and Google AI Studio documentation

## 🚀 Next Steps

- [Quick Start Guide](QUICKSTART.md)
- [Firebase Setup](FIREBASE_SETUP.md)
- [Project Overview](PROJECT_OVERVIEW.md)

---

**Happy coding! 🎉**
