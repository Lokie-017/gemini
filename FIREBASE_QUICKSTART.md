# Firebase Authentication Quick Start

## 🚀 Quick Setup (5 minutes)

### 1. Create Firebase Project
- Go to https://console.firebase.google.com
- Create a new project named "Gemini-AI-Assistant"

### 2. Enable Services
- **Authentication**: Email/Password provider
- **Realtime Database**: Test mode

### 3. Get Credentials
- Project Settings → Service Accounts → Generate Private Key
- Save the JSON file

### 4. Set Environment Variable (Windows PowerShell)
```powershell
# Temporary
$json = Get-Content 'C:\path\to\firebase-credentials.json' -Raw
$env:FIREBASE_CREDENTIALS_JSON = $json

# Or use .streamlit/secrets.toml for development
```

### 5. Install & Run
```bash
pip install -r requirements.txt
streamlit run streamlit_ui.py
```

### 6. Create Account
- Sign up with email/password
- Start using the app!

## 📚 Features

✅ **Secure Authentication** - Email/password signup and login  
✅ **Personalized Settings** - Save language and conversation mode preferences  
✅ **Cloud History** - All conversations synced to Firebase  
✅ **User Profile** - Track interactions and member status  
✅ **Account Management** - Update profile or delete account  

## 🔐 Security Rules (Copy to Firebase Console)

1. Go to Realtime Database → Rules
2. Replace with:

```json
{
  "rules": {
    "users": {
      "$uid": {
        ".read": "$uid === auth.uid",
        ".write": "$uid === auth.uid"
      }
    }
  }
}
```

## ❌ If Firebase Not Configured

The app will still work with local history only:
- No cloud sync
- No cross-device history
- Preferences reset on logout

## 📖 Full Setup Guide

See [FIREBASE_SETUP.md](FIREBASE_SETUP.md) for detailed instructions.
