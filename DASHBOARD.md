# 📊 Gemini AI Dashboard

A comprehensive analytics and management dashboard for the Gemini AI Assistant project.

## Features

### 📈 Key Metrics
- **Total Users**: Track unique users across the system
- **Total Conversations**: Monitor chat sessions and interactions
- **Total Messages**: Count of all user prompts sent
- **Active Today**: Users active in the last 24 hours

### 📊 Usage Analytics
- **Languages Used**: Visualize language distribution across conversations
- **Conversation Modes**: Breakdown of chat, Q&A, and analysis modes
- **Charts**: Interactive bar charts for data visualization

### ⚙️ System Status
- **Firebase Connection**: Status of cloud database
- **Local Histories**: Number of per-user history files
- **Knowledge Base**: Size and availability of knowledge base

### 🕐 Recent Activity
- **Activity Feed**: Latest conversations across all users
- **Conversation Details**: View prompts and responses
- **Timestamps**: Track when conversations occurred

### 👥 User Management
- **Active Users List**: All users with message counts
- **User Analytics**: Per-user statistics and language preferences
- **Usage Patterns**: Character count and average response lengths

### 📥 Export Data
- **Analytics Export**: Download project statistics as JSON
- **Conversation Export**: Export all conversations for backup/analysis

## Running the Dashboard

### Option 1: Direct Streamlit
```bash
streamlit run dashboard.py
```

### Option 2: From main Streamlit app
Add a "Dashboard" tab in the navigation menu to switch between the assistant and dashboard.

### Option 3: As separate page
The dashboard runs as a standalone Streamlit app on a different port:
```bash
streamlit run dashboard.py --server.port 8502
```

## Data Sources

The dashboard automatically collects data from:

1. **Local Per-User Histories**
   - Location: `user_histories/chat_history_{user_id}.json`
   - Format: JSON array of conversations
   - Updates: Real-time from local files

2. **Firebase Database** (if configured)
   - Path: `users/{uid}/conversations/`
   - Real-time sync with cloud
   - User authentication data
   - Profile information

3. **Knowledge Base**
   - File: `knowledge_base.json`
   - Provides context for conversations

## Dashboard Sections

### Top Row: Key Metrics
Quick overview of system activity and usage.

### Analytics Charts
Visual representation of:
- Language usage patterns
- Conversation mode distribution
- User activity trends

### Recent Activity
Live feed of recent conversations across all users with expandable details.

### User Management
- Lists all active users
- Shows detailed per-user analytics
- Tracks language preferences and usage patterns

### Export Options
Download data for external analysis or backup.

## Customization

### Add Custom Metrics
Edit the `calculate_stats()` function to add new metrics:
```python
stats['custom_metric'] = some_calculation()
```

### Modify Charts
Update `show_usage_analytics()` to add new visualizations:
```python
st.line_chart(data)
st.scatter_chart(data)
```

### Change Color Scheme
Update the CSS in `show_header()` to customize dashboard appearance.

## Performance Notes

- Dashboard reads all local history files on load
- For large deployments, consider paginating recent activity
- Firebase queries are optimized with `.get()` snapshots
- Charts are rendered client-side by Streamlit

## Troubleshooting

### "No conversations yet"
- Ensure the app has been used (conversations created)
- Check that `user_histories/` directory exists
- Verify Firebase credentials are properly configured

### Firebase connection fails
- Check `firebase-credentials.json` exists
- Verify database URL is correct
- Ensure Firebase rules allow read/write access

### Charts not showing
- Ensure data exists in conversations
- Check language/mode values are not null
- Verify JSON structure is valid

## Related Files

- [streamlit_ui.py](streamlit_ui.py) - Main chat application
- [firebase_auth.py](firebase_auth.py) - Firebase authentication
- [gemini_api.py](gemini_api.py) - Gemini API integration
- [requirements.txt](requirements.txt) - Python dependencies

## Next Steps

Consider adding:
- Real-time WebSocket updates
- Advanced filtering and search
- Export to CSV/Excel
- User activity heatmaps
- Response quality metrics
- API usage analytics
- Custom date range selection
