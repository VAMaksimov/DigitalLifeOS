#!/bin/bash

# ==========================================
# LifeOS Initialization Script
# ==========================================
# This script creates the directory structure for your Life Database,
# initializes Git for version control, and sets up the Python environment
# for your AI agents.

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
git remote add origin git@github.com:VAMaksimov/DigitalLifeOS.git


# 4. Python Environment Setup
python3 -m venv venv
source venv/bin/activate

# Install critical AI libraries
# langchain: Framework for LLM apps
# chromadb: Vector database for storage
# google-generativeai: For Gemini
# telethon: For Telegram automation
# watchdog: For monitoring file changes
pip install -r requirements.txt

# Create a sample .env file
echo "GOOGLE_API_KEY=" > .env
echo "TELEGRAM_API_ID=" >> .env
echo "TELEGRAM_API_HASH=" >> .env
echo "LIFE_OS_PATH=$HOME/LifeOS" >> .env
echo "API_TOKEN=" >> .env

