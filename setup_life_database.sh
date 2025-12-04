#!/bin/bash

# ==========================================
# LifeOS Initialization Script
# ==========================================
# This script creates the directory structure for your Life Database,
# initializes Git for version control, and sets up the Python environment
# for your AI agents.

BASE_DIR="$HOME/LifeOS"

echo "🚀 Initializing LifeOS at $BASE_DIR..."

# 1. Create Directory Structure (Based on PARA Method + Logs)
mkdir -p "$BASE_DIR"
cd "$BASE_DIR"

# Projects: Active tasks with deadlines
mkdir -p "01_Projects"
# Areas: Ongoing responsibilities (Health, Finances, Coding)
mkdir -p "02_Areas"
# Resources: Reference materials, notes, research
mkdir -p "03_Resources"
# Archive: Completed projects
mkdir -p "04_Archive"
# Inbox: Raw dump for quick notes before sorting
mkdir -p "00_Inbox"
# System: Where the AI logs, database files, and scripts live
mkdir -p "99_System/scripts"
mkdir -p "99_System/vector_db"
mkdir -p "99_System/logs"

echo "✅ Directory structure created."

# 2. Create Initial Markdown Files
echo "# LifeOS Dashboard" > "Dashboard.md"
echo "## Current Focus" >> "Dashboard.md"
echo "- [ ] Setup LifeOS Infrastructure" >> "Dashboard.md"

echo "# Daily Log" > "00_Inbox/Daily_Log.md"

# 3. Initialize Git (For Version Control & Backup)
git init
echo "99_System/vector_db/" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.env" >> .gitignore
git add .
git commit -m "Initial LifeOS Commit"

echo "✅ Git repository initialized."

# 4. Python Environment Setup
echo "🐍 Setting up Python Virtual Environment..."
python3 -m venv venv
source venv/bin/activate

# Install critical AI libraries
# langchain: Framework for LLM apps
# chromadb: Vector database for storage
# google-generativeai: For Gemini
# telethon: For Telegram automation
# watchdog: For monitoring file changes
pip install langchain langchain-community langchain-google-genai chromadb google-generativeai telethon watchdog python-dotenv

# Create a sample .env file
echo "GOOGLE_API_KEY=your_key_here" > .env
echo "TELEGRAM_API_ID=your_id_here" >> .env
echo "TELEGRAM_API_HASH=your_hash_here" >> .env

echo "✅ Python environment ready."
echo "⚠️  Action Required: Edit $BASE_DIR/.env with your actual API keys."
echo "🎉 LifeOS Setup Complete! Location: $BASE_DIR"
