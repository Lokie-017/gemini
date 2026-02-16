# 🚀 Quick Start Guide

Run your Gemini AI assistant and dashboard in minutes!

## ⚡ 5-Minute Setup

### Step 1: Get API Key
```bash
# Get your Gemini API key from https://aistudio.google.com/apikey
# Then set environment variable:

# Windows (PowerShell)
$env:GEMINI_API_KEY = "your_api_key_here"

# Windows (Command Prompt)
set GEMINI_API_KEY=your_api_key_here

# Linux/Mac
export GEMINI_API_KEY=your_api_key_here
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Applications

**Chat Application:**
```bash
streamlit run streamlit_ui.py
```
Opens at `http://localhost:8501`

**Dashboard (separate terminal):**
```bash
streamlit run dashboard.py
```
Opens at `http://localhost:8502`

## 📊 Dashboard Features

### Metrics Shown
✅ Total users and conversations  
✅ Active users today  
✅ Language distribution  
✅ Conversation modes used  
✅ System status (Firebase, local storage)  
✅ Recent activity feed  
✅ User management  
✅ Data export options  

### Where to Go
| Page | Purpose |
|------|---------|
| `📈 Key Metrics` | Quick overview |
| `📊 Usage Analytics` | Charts and graphs |
| `👥 User Management` | View user details |
| `📥 Export Data` | Download analytics |

## 🔥 Firebase Setup (Optional)

For cloud storage and user authentication:

1. Go to https://console.firebase.google.com
2. Create new project
3. Enable Authentication (Email/Password)
4. Create Realtime Database
5. Download credentials JSON
6. Save as `firebase-credentials.json`

See [FIREBASE_SETUP.md](FIREBASE_SETUP.md) for detailed instructions.

## 📁 Important Directories

```
user_histories/           ← Per-user chat histories
├── chat_history_guest.json
└── chat_history_user123.json

knowledge_base.json       ← AI context data
firebase-credentials.json ← Firebase config (optional)
```

## 🎯 Common Tasks

### View User Chat History
1. Open Dashboard
2. Go to "User Management" tab
3. Select user from dropdown
4. View statistics and language breakdown

### Export All Data
1. Open Dashboard
2. Scroll to "Export Data"
3. Click "Export All Analytics" or "Export All Conversations"
4. Save JSON file for analysis

### Add Knowledge to AI
1. Open Chat Application
2. Edit "Knowledge Base" text area
3. Add your context (college data, FAQ, etc.)
4. It's automatically included in responses

### Change Response Mode
1. In Chat Application sidebar
2. Select "Conversation Mode":
   - **Chat**: Friendly, conversational
   - **Q&A**: Direct answers
   - **Analysis**: Deep insights

### Support Multiple Languages
1. In Chat Application sidebar
2. Select "Response Language"
3. User can send message in any language
4. AI responds in selected language

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Run on different port
streamlit run dashboard.py --server.port 8503
```

### Firebase Connection Error
- Ensure `firebase-credentials.json` exists
- Check Firebase database is created
- Verify credentials are valid
- See [FIREBASE_SETUP.md](FIREBASE_SETUP.md)

### No Data in Dashboard
- Create a chat conversation first
- Wait a few seconds for refresh
- Check `user_histories/` folder exists
- Verify JSON files are valid

### Gemini API Error
- Confirm API key is set: `echo $GEMINI_API_KEY`
- Check API key is valid at https://aistudio.google.com
- Ensure internet connection is active

## 📊 Dashboard Walkthrough

### Home Page
Shows key metrics at the top:
- 👥 Total Users
- 💬 Conversations
- 📝 Messages
- 🔥 Active Today

### Analytics Section
- Bar charts for languages used
- Mode distribution
- Real-time updates

### Recent Activity
- List of latest conversations
- Click to expand and view details
- Timestamps for each message

### User Management
- Active users list
- Per-user statistics
- Language preferences
- Character counts

### Export Section
- Download analytics as JSON
- Export all conversations
- Timestamped filenames

## 🎓 Learning Resources

- [Gemini API Docs](https://ai.google.dev)
- [Streamlit Docs](https://docs.streamlit.io)
- [Firebase Docs](https://firebase.google.com/docs)
- [Python Docs](https://docs.python.org)

## 📝 File Reference

| File | Purpose |
|------|---------|
| `streamlit_ui.py` | Main chat interface |
| `dashboard.py` | Analytics and monitoring |
| `gemini_api.py` | AI integration |
| `firebase_auth.py` | User authentication |
| `main.py` | CLI interface |

## 🚀 Next Steps

1. **Customize Knowledge Base**: Edit `knowledge_base.json` with your data
2. **Setup Firebase**: For multi-user support and cloud sync
3. **Monitor Dashboard**: Check analytics regularly
4. **Export Data**: Backup conversations periodically
5. **Add Features**: Extend the system as needed

## 🎯 Pro Tips

💡 **Tip 1**: Keep `GEMINI_API_KEY` configured in your system environment for persistence

💡 **Tip 2**: Regularly export data from dashboard for backups

💡 **Tip 3**: Use descriptive knowledge base content for better responses

💡 **Tip 4**: Check dashboard to identify popular topics/languages

💡 **Tip 5**: Test PDF uploads with different file formats

## 📞 Need Help?

| Issue | Solution |
|-------|----------|
| Keys not working | Set environment variable and restart terminal |
| Dashboard is slow | Reduce conversation limit or clear old data |
| Firebase offline | Check internet connection or disable Firebase |
| PDF not parsing | Try different PDF format or smaller files |

---

**Happy Chatting! 🚀**

For detailed documentation, see:
- [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) - Full architecture
- [DASHBOARD.md](DASHBOARD.md) - Dashboard documentation
- [FIREBASE_SETUP.md](FIREBASE_SETUP.md) - Firebase configuration
