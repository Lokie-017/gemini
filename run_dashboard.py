#!/usr/bin/env python
"""
Quick start script to run the Gemini AI Dashboard
"""

import subprocess
import sys
import os

def run_dashboard():
    """Run the Streamlit dashboard."""
    print("\n" + "="*60)
    print("🚀 Starting Gemini AI Dashboard")
    print("="*60 + "\n")
    
    # Check if streamlit is installed
    try:
        import streamlit
    except ImportError:
        print("❌ Streamlit is not installed!")
        print("Install it with: pip install streamlit")
        sys.exit(1)
    
    # Run the dashboard
    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "dashboard.py"],
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
    except KeyboardInterrupt:
        print("\n\n✅ Dashboard stopped")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error running dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_dashboard()
