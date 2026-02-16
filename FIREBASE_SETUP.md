# Firebase Authentication Setup Guide

This application uses Firebase for secure user authentication and personalized AI interactions.

## Prerequisites

- Firebase account (free tier available at https://firebase.google.com)
- Google Cloud project

## Setup Instructions

### 1. Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com)
2. Click "Add project"
3. Enter project name (e.g., "Gemini-AI-Assistant")
4. Click "Create project"
5. Wait for project provisioning to complete

### 2. Enable Authentication

1. In Firebase Console, go to **Build** → **Authentication**
2. Click **Get started**
3. Select **Email/Password** provider
4. Enable both "Email/Password" and "Email link (passwordless sign-in)" options
5. Click **Save**

### 3. Set Up Realtime Database

1. In Firebase Console, go to **Build** → **Realtime Database**
2. Click **Create Database**
3. Choose location (closest to your users)
4. Start in **Test mode** (for development only; switch to production rules for deployment)
5. Click **Enable**

### 4. Configure Database Security Rules

Replace the default rules with:

```json
{
  "rules": {
    "users": {
      "$uid": {
        ".read": "$uid === auth.uid",
        ".write": "$uid === auth.uid",
        "profile": {
          ".validate": "newData.hasChildren(['uid', 'email', 'display_name', 'created_at', 'preferences'])"
        },
        "conversations": {
          "$timestamp": {
            ".validate": "newData.hasChildren(['timestamp', 'prompt', 'response'])"
          }
        }
      }
    }
  }
}
```

### 5. Get Firebase Credentials

1. In Firebase Console, go to **Project Settings** (gear icon)
2. Click **Service Accounts** tab
3. Click **Generate New Private Key**
4. Save the JSON file securely

### 6. Configure Application

#### Option A: Environment Variable (Recommended for Production)

1. Save the Firebase JSON file content as an environment variable:

```powershell
$json = Get-Content 'path/to/firebase-key.json' -Raw
$env:FIREBASE_CREDENTIALS_JSON = $json
```

For permanent setup (Windows):
1. Right-click "This PC" → **Properties** → **Advanced system settings**
2. Click **Environment Variables**
3. Add new User variable:
   - Variable name: `FIREBASE_CREDENTIALS_JSON`
   - Variable value: [Paste entire JSON content]

#### Option B: Streamlit Secrets (Development)

1. Create/edit `.streamlit/secrets.toml` in your project:

```toml
[firebase_credentials]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "firebase-adminsdk-xxx@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."
database_url = "https://your-project.firebaseio.com"
storage_bucket = "your-project.appspot.com"
```

> **Note**: Add `.streamlit/secrets.toml` to `.gitignore` to prevent credential leaks

### 7. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `firebase-admin`: Firebase SDK
- `google-genai`: Google Gemini API
- `streamlit`: Web framework
- `pypdf`: PDF processing

## Features Enabled

Once configured, the application provides:

### Authentication
- ✅ User signup with email and password
- ✅ Secure login with Firebase
- ✅ Account creation with display name
- ✅ Logout and account deletion

### Personalization
- ✅ User preferences (language, mode) saved to cloud
- ✅ Interaction count tracking
- ✅ Conversation history in Firebase
- ✅ Member since date tracking
- ✅ PDF upload linked to user account

### User Experience
- ✅ Profile information in sidebar
- ✅ Account settings and management
- ✅ Cloud conversation history viewer
- ✅ Local and cloud history sync
- ✅ Preferences auto-load on login

## Usage

### Running the Application

```bash
streamlit run streamlit_ui.py
```

The app will:
1. Display login/signup page
2. Authenticate user
3. Load saved preferences
4. Show personalized interface
5. Save interactions to cloud

### User Actions

**Sign Up**
- Enter email and password (min 6 characters)
- Optionally add display name
- Click "Sign Up"

**Login**
- Enter registered email
- Enter password
- Click "Login"

**Settings**
- Change response language
- Select interaction mode
- View account info
- Delete account (with confirmation)
- Logout

**Cloud History**
- View last 10 conversations
- See cloud storage status
- Monitor interaction count

## Troubleshooting

### "Firebase credentials not found"
- Ensure `FIREBASE_CREDENTIALS_JSON` environment variable is set
- OR add credentials to `.streamlit/secrets.toml`
- Restart Streamlit app

### "Sign up failed"
- Ensure password is at least 6 characters
- Check email format is valid
- Verify email not already registered

### "Connection error to Realtime Database"
- Check internet connection
- Verify database URL is correct
- Ensure database exists in Firebase Console
- Check Realtime Database security rules

### Conversations not saving to cloud
- Verify user is authenticated
- Check Firebase Realtime Database is enabled
- Review database security rules
- Look for error messages in Streamlit terminal

## Security Best Practices

1. **Never commit credentials**: Always use environment variables or secrets
2. **Use production rules**: Switch from test mode before deploying
3. **Limit API calls**: Set Realtime Database pricing alerts
4. **Regular audits**: Monitor Firebase usage in console
5. **Secure passwords**: Encourage users to use strong passwords
6. **HTTPS only**: Deploy on HTTPS in production

## File Structure

```
google_api/
├── streamlit_ui.py          # Main Streamlit app
├── firebase_auth.py         # Firebase auth module
├── gemini_api.py           # Gemini API wrapper
├── requirements.txt         # Python dependencies
├── FIREBASE_SETUP.md       # This file
└── .streamlit/
    └── secrets.toml        # (Optional) Local secrets
```

## Support

For issues:
1. Check [Firebase Documentation](https://firebase.google.com/docs)
2. Review [Streamlit Docs](https://docs.streamlit.io)
3. Check [Google Gemini API Docs](https://ai.google.dev/docs)

## Next Steps

1. ✅ Set up Firebase project
2. ✅ Configure authentication and database
3. ✅ Add credentials to environment
4. ✅ Install dependencies
5. ✅ Run Streamlit app
6. ✅ Create account and start using
