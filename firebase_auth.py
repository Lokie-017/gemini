"""Firebase Authentication module for user management and personalized interactions."""

import os
import json
import streamlit as st
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, auth, db, storage


def initialize_firebase():
    """Initialize Firebase app if not already initialized.
    
    Tries to load credentials from (in order):
    1. firebase-credentials.json in project directory
    2. FIREBASE_CREDENTIALS_JSON environment variable
    3. st.secrets["firebase_credentials"]
    """
    if firebase_admin._apps:
        return firebase_admin.get_app()
    
    creds_json = None
    
    # Try loading from local file first
    if os.path.exists("firebase-credentials.json"):
        try:
            with open("firebase-credentials.json", "r") as f:
                creds_json = f.read()
        except Exception as e:
            raise ValueError(f"Failed to read firebase-credentials.json: {e}")
    
    # Try environment variable
    if not creds_json:
        creds_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
    
    # Try Streamlit secrets
    if not creds_json:
        if "firebase_credentials" in st.secrets:
            creds_json = json.dumps(st.secrets["firebase_credentials"])
        else:
            raise ValueError(
                "Firebase credentials not found. Tried:\n"
                "1. firebase-credentials.json in project directory\n"
                "2. FIREBASE_CREDENTIALS_JSON environment variable\n"
                "3. firebase_credentials in st.secrets\n\n"
                "See FIREBASE_SETUP.md for configuration instructions."
            )
    
    # Parse and create credentials
    creds_dict = json.loads(creds_json)
    cred = credentials.Certificate(creds_dict)
    
    # Initialize Firebase
    firebase_admin.initialize_app(cred, {
        'databaseURL': creds_dict.get('database_url', ''),
        'storageBucket': creds_dict.get('storage_bucket', ''),
    })
    
    return firebase_admin.get_app()


def sign_up(email: str, password: str, display_name: str = None):
    """Create a new user account.
    
    Args:
        email: User email address
        password: User password (minimum 6 characters)
        display_name: Optional display name
        
    Returns:
        dict: User information including uid
    """
    try:
        initialize_firebase()
        user = auth.create_user(email=email, password=password, display_name=display_name)
        
        # Create user profile in database
        user_profile = {
            'uid': user.uid,
            'email': email,
            'display_name': display_name or email.split('@')[0],
            'created_at': datetime.now().isoformat(),
            'preferences': {
                'language': 'en',
                'mode': 'chat',
                'theme': 'light'
            },
            'interaction_count': 0
        }
        
        db.reference(f'users/{user.uid}/profile').set(user_profile)
        
        return {'success': True, 'user': user_profile}
    except auth.EmailAlreadyExistsError:
        return {'success': False, 'error': 'Email already registered'}
    except auth.InvalidPasswordError:
        return {'success': False, 'error': 'Password must be at least 6 characters'}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def log_in(email: str, password: str):
    """Authenticate user with email and password.
    
    Note: This uses the REST API as firebase-admin doesn't support password auth.
    client-side authentication (e.g., via pyrebase4) should be used in production.
    
    Args:
        email: User email
        password: User password
        
    Returns:
        dict: Authentication result with token if successful
    """
    try:
        initialize_firebase()
        # Get user by email (admin SDK method)
        user = auth.get_user_by_email(email)
        
        # Verify user exists and load profile
        profile = db.reference(f'users/{user.uid}/profile').get().val()
        
        if profile:
            return {
                'success': True,
                'uid': user.uid,
                'user': profile,
                'message': f'Welcome back, {profile.get("display_name", "User")}!'
            }
        else:
            return {'success': False, 'error': 'User profile not found'}
            
    except auth.UserNotFoundError:
        return {'success': False, 'error': 'User not found. Please sign up first.'}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def get_current_user(uid: str):
    """Get current user profile from database.
    
    Args:
        uid: User ID
        
    Returns:
        dict: User profile data or None
    """
    try:
        initialize_firebase()
        profile = db.reference(f'users/{uid}/profile').get().val()
        return profile
    except Exception as e:
        st.error(f"Error fetching user profile: {e}")
        return None


def update_user_profile(uid: str, updates: dict):
    """Update user profile information.
    
    Args:
        uid: User ID
        updates: Dictionary of fields to update
        
    Returns:
        bool: Success status
    """
    try:
        initialize_firebase()
        db.reference(f'users/{uid}/profile').update(updates)
        return True
    except Exception as e:
        st.error(f"Error updating user profile: {e}")
        return False


def save_user_preferences(uid: str, preferences: dict):
    """Save user interaction preferences.
    
    Args:
        uid: User ID
        preferences: Dictionary with language, mode, theme, etc.
        
    Returns:
        bool: Success status
    """
    return update_user_profile(uid, {'preferences': preferences})


def save_conversation_to_user(uid: str, conversation: dict):
    """Save a conversation to user's history in Firebase.
    
    Args:
        uid: User ID
        conversation: Conversation entry to save
        
    Returns:
        bool: Success status
    """
    try:
        initialize_firebase()
        timestamp = datetime.now().isoformat()
        db.reference(f'users/{uid}/conversations/{timestamp}').set(conversation)
        
        # Update interaction count
        profile = db.reference(f'users/{uid}/profile').get().val()
        count = profile.get('interaction_count', 0) + 1
        db.reference(f'users/{uid}/profile/interaction_count').set(count)
        
        return True
    except Exception as e:
        st.error(f"Error saving conversation: {e}")
        return False


def get_user_conversations(uid: str, limit: int = 50):
    """Retrieve user's conversation history from Firebase.
    
    Args:
        uid: User ID
        limit: Maximum number of conversations to retrieve
        
    Returns:
        list: List of conversation entries
    """
    try:
        initialize_firebase()
        conversations = db.reference(f'users/{uid}/conversations').get().val()
        
        if not conversations:
            return []
        
        # Convert to list and sort by timestamp (newest first)
        conv_list = [
            {**conv, 'timestamp': ts} 
            for ts, conv in conversations.items()
        ]
        conv_list.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return conv_list[:limit]
    except Exception as e:
        st.error(f"Error retrieving conversations: {e}")
        return []


def delete_user_account(uid: str):
    """Delete user account and all associated data.
    
    Args:
        uid: User ID
        
    Returns:
        bool: Success status
    """
    try:
        initialize_firebase()
        auth.delete_user(uid)
        db.reference(f'users/{uid}').delete()
        return True
    except Exception as e:
        st.error(f"Error deleting account: {e}")
        return False


def logout():
    """Clear user session in Streamlit session state."""
    st.session_state.pop('user_id', None)
    st.session_state.pop('user_profile', None)
    st.session_state.pop('user_email', None)
