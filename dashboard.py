"""
Dashboard for Gemini AI Assistant - Comprehensive project analytics and management.
"""

import os
import json
import streamlit as st
from datetime import datetime, timedelta
from collections import Counter
import firebase_admin
from firebase_admin import credentials, auth, db

# Page config
st.set_page_config(
    page_title="📊 Gemini AI Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .metric-value {
        font-size: 2.5em;
        font-weight: bold;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 0.9em;
        opacity: 0.9;
    }
    .status-active { color: #10b981; }
    .status-inactive { color: #ef4444; }
    .chart-container { 
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

HISTORY_DIR = "user_histories"


def init_firebase():
    """Initialize Firebase connection."""
    try:
        if firebase_admin._apps:
            return True
        
        if os.path.exists("firebase-credentials.json"):
            cred = credentials.Certificate("firebase-credentials.json")
            firebase_admin.initialize_app(cred)
            return True
        return False
    except:
        return False


def get_all_users():
    """Get list of all users from Firebase."""
    try:
        snapshot = db.reference('users').get()
        if snapshot.val():
            return list(snapshot.val().keys())
        return []
    except:
        return []


def get_user_conversations(uid):
    """Get all conversations for a specific user."""
    try:
        snapshot = db.reference(f'users/{uid}/conversations').get()
        if snapshot.val():
            return list(snapshot.val().values())
        return []
    except:
        return []


def get_all_local_histories():
    """Get all local user history files."""
    histories = {}
    if not os.path.exists(HISTORY_DIR):
        return histories
    
    try:
        for filename in os.listdir(HISTORY_DIR):
            if filename.startswith('chat_history_') and filename.endswith('.json'):
                user_id = filename.replace('chat_history_', '').replace('.json', '')
                path = os.path.join(HISTORY_DIR, filename)
                with open(path, 'r', encoding='utf-8') as f:
                    histories[user_id] = json.load(f)
    except:
        pass
    
    return histories


def calculate_stats():
    """Calculate comprehensive project statistics."""
    stats = {
        'total_users': 0,
        'total_conversations': 0,
        'total_messages': 0,
        'languages_used': Counter(),
        'modes_used': Counter(),
        'avg_response_length': 0,
        'active_today': 0,
        'firebase_enabled': False,
    }
    
    # Try Firebase first
    firebase_ok = init_firebase()
    stats['firebase_enabled'] = firebase_ok
    
    response_lengths = []
    today = datetime.now().date()
    active_users_today = set()
    
    if firebase_ok:
        try:
            users = get_all_users()
            stats['total_users'] = len(users)
            
            for uid in users:
                conversations = get_user_conversations(uid)
                stats['total_conversations'] += len(conversations)
                
                for conv in conversations:
                    stats['total_messages'] += 1
                    if 'language' in conv:
                        stats['languages_used'][conv.get('language', 'unknown')] += 1
                    if 'mode' in conv:
                        stats['modes_used'][conv.get('mode', 'unknown')] += 1
                    
                    response = conv.get('response', '')
                    if response:
                        response_lengths.append(len(response))
                    
                    # Check if active today
                    try:
                        timestamp = datetime.fromisoformat(conv.get('timestamp', ''))
                        if timestamp.date() == today:
                            active_users_today.add(uid)
                    except:
                        pass
        except:
            pass
    
    # Add local histories
    try:
        local_histories = get_all_local_histories()
        stats['total_users'] = max(stats['total_users'], len(local_histories))
        
        for user_id, conversations in local_histories.items():
            if not firebase_ok or user_id == 'guest':  # Count local guest conversations
                stats['total_conversations'] += len(conversations)
                
                for conv in conversations:
                    stats['total_messages'] += 1
                    if 'language' in conv:
                        stats['languages_used'][conv.get('language', 'unknown')] += 1
                    if 'mode' in conv:
                        stats['modes_used'][conv.get('mode', 'unknown')] += 1
                    
                    response = conv.get('response', '')
                    if response:
                        response_lengths.append(len(response))
                    
                    try:
                        timestamp = datetime.fromisoformat(conv.get('timestamp', ''))
                        if timestamp.date() == today:
                            active_users_today.add(user_id)
                    except:
                        pass
    except:
        pass
    
    stats['active_today'] = len(active_users_today)
    
    if response_lengths:
        stats['avg_response_length'] = int(sum(response_lengths) / len(response_lengths))
    
    return stats


def get_recent_conversations(limit=10):
    """Get recent conversations across all users."""
    convs = []
    
    try:
        local_histories = get_all_local_histories()
        for user_id, conversations in local_histories.items():
            for conv in conversations:
                conv['user_id'] = user_id
                convs.append(conv)
    except:
        pass
    
    # Sort by timestamp
    try:
        convs.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    except:
        pass
    
    return convs[:limit]


def show_header():
    """Display dashboard header."""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📊 Gemini AI Dashboard")
        st.markdown("*Comprehensive project analytics and management*")
    with col2:
        st.metric("Last Updated", datetime.now().strftime("%H:%M:%S"))


def show_metrics(stats):
    """Display key metrics."""
    st.subheader("📈 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "👥 Total Users",
            stats['total_users'],
            help="Unique users who have used the system"
        )
    
    with col2:
        st.metric(
            "💬 Total Conversations",
            stats['total_conversations'],
            help="Total number of chat sessions"
        )
    
    with col3:
        st.metric(
            "📝 Total Messages",
            stats['total_messages'],
            help="Total user prompts sent"
        )
    
    with col4:
        st.metric(
            "🔥 Active Today",
            stats['active_today'],
            help="Users active in the last 24 hours"
        )


def show_usage_analytics(stats):
    """Display usage analytics."""
    st.subheader("📊 Usage Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Languages Used")
        if stats['languages_used']:
            lang_data = dict(stats['languages_used'])
            lang_names = {
                'en': '🇬🇧 English',
                'es': '🇪🇸 Spanish',
                'fr': '🇫🇷 French',
                'de': '🇩🇪 German',
                'zh': '🇨🇳 Chinese',
                'ja': '🇯🇵 Japanese',
                'pt': '🇵🇹 Portuguese',
                'ru': '🇷🇺 Russian',
            }
            
            display_data = {}
            for lang_code, count in lang_data.items():
                display_data[lang_names.get(lang_code, lang_code)] = count
            
            st.bar_chart(display_data)
        else:
            st.info("No language data available")
    
    with col2:
        st.markdown("#### Conversation Modes")
        if stats['modes_used']:
            mode_data = dict(stats['modes_used'])
            mode_names = {
                'chat': '💬 Chat',
                'qa': '❓ Q&A',
                'analysis': '🔍 Analysis',
            }
            
            display_data = {}
            for mode, count in mode_data.items():
                display_data[mode_names.get(mode, mode)] = count
            
            st.bar_chart(display_data)
        else:
            st.info("No mode data available")


def show_system_status(stats):
    """Display system status."""
    st.subheader("⚙️ System Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        firebase_status = "✅ Connected" if stats['firebase_enabled'] else "⚠️ Disabled"
        st.info(f"**Firebase**: {firebase_status}")
    
    with col2:
        local_histories = get_all_local_histories()
        st.info(f"**Local Histories**: {len(local_histories)} users")
    
    with col3:
        try:
            with open("knowledge_base.json", "r") as f:
                kb = json.load(f)
                st.info(f"**Knowledge Base**: {len(str(kb))} chars")
        except:
            st.info("**Knowledge Base**: Not found")


def show_recent_activity(limit=10):
    """Display recent conversations."""
    st.subheader("🕐 Recent Activity")
    
    conversations = get_recent_conversations(limit)
    
    if conversations:
        for i, conv in enumerate(conversations, 1):
            with st.expander(
                f"#{i} • {conv.get('user_id', 'unknown')} • {conv.get('timestamp', '')[:16]}"
            ):
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    st.caption(f"**Mode**: {conv.get('mode', 'chat')}")
                    st.caption(f"**Language**: {conv.get('language', 'en')}")
                
                with col2:
                    st.markdown("**Prompt**:")
                    st.write(conv.get('prompt', 'N/A')[:200])
                    st.markdown("**Response**:")
                    st.write(conv.get('response', 'N/A')[:300])
    else:
        st.info("No conversations yet")


def show_user_management():
    """Display user management section."""
    st.subheader("👥 User Management")
    
    tab1, tab2 = st.tabs(["Active Users", "User Details"])
    
    with tab1:
        try:
            local_histories = get_all_local_histories()
            if local_histories:
                user_data = []
                for user_id, conversations in local_histories.items():
                    last_active = "Never"
                    msg_count = len(conversations)
                    
                    if conversations:
                        try:
                            timestamps = [conv.get('timestamp', '') for conv in conversations]
                            timestamps = [t for t in timestamps if t]
                            if timestamps:
                                last_active = max(timestamps)[:10]
                        except:
                            pass
                    
                    user_data.append({
                        "User ID": user_id[:20],
                        "Messages": msg_count,
                        "Last Active": last_active,
                    })
                
                st.dataframe(user_data, use_container_width=True, hide_index=True)
            else:
                st.info("No local user data available")
        except Exception as e:
            st.error(f"Error loading user data: {e}")
    
    with tab2:
        st.markdown("#### User Details")
        local_histories = get_all_local_histories()
        if local_histories:
            selected_user = st.selectbox("Select user:", list(local_histories.keys()))
            
            if selected_user:
                conversations = local_histories[selected_user]
                st.metric("Total Conversations", len(conversations))
                
                # Calculate stats for this user
                total_chars_sent = sum(len(c.get('prompt', '')) for c in conversations)
                total_chars_received = sum(len(c.get('response', '')) for c in conversations)
                avg_response = total_chars_received // len(conversations) if conversations else 0
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Characters Sent", total_chars_sent)
                with col2:
                    st.metric("Total Characters Received", total_chars_received)
                with col3:
                    st.metric("Avg Response Length", avg_response)
                
                # Language breakdown
                lang_counter = Counter(c.get('language', 'en') for c in conversations)
                lang_names = {
                    'en': '🇬🇧 English',
                    'es': '🇪🇸 Spanish',
                    'fr': '🇫🇷 French',
                    'de': '🇩🇪 German',
                    'zh': '🇨🇳 Chinese',
                    'ja': '🇯🇵 Japanese',
                    'pt': '🇵🇹 Portuguese',
                    'ru': '🇷🇺 Russian',
                }
                
                st.markdown("**Languages Used**:")
                lang_display = {lang_names.get(k, k): v for k, v in lang_counter.items()}
                st.bar_chart(lang_display)
        else:
            st.info("No user data available")


def show_export_section():
    """Display data export options."""
    st.subheader("📥 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Export All Analytics"):
            stats = calculate_stats()
            export_data = {
                "generated_at": datetime.now().isoformat(),
                "statistics": {
                    "total_users": stats['total_users'],
                    "total_conversations": stats['total_conversations'],
                    "total_messages": stats['total_messages'],
                    "active_today": stats['active_today'],
                    "avg_response_length": stats['avg_response_length'],
                },
                "languages": dict(stats['languages_used']),
                "modes": dict(stats['modes_used']),
            }
            
            st.download_button(
                label="Download Analytics JSON",
                data=json.dumps(export_data, indent=2),
                file_name=f"analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
            )
    
    with col2:
        if st.button("💾 Export All Conversations"):
            conversations = get_recent_conversations(limit=10000)
            st.download_button(
                label="Download Conversations JSON",
                data=json.dumps(conversations, indent=2, ensure_ascii=False),
                file_name=f"conversations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
            )


def main():
    """Main dashboard function."""
    show_header()
    
    # Calculate statistics
    stats = calculate_stats()
    
    # Display sections
    show_metrics(stats)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        show_usage_analytics(stats)
    with col2:
        show_system_status(stats)
    
    st.divider()
    
    show_recent_activity()
    
    st.divider()
    
    show_user_management()
    
    st.divider()
    
    show_export_section()
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
        <p>Gemini AI Assistant Dashboard • Last updated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
