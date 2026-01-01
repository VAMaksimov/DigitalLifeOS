# The goal

I want to create database of my whole life (and simultaneously central hub of my online activity), where I regularly update the data, and which can be accessible by any LLM. I want to have to-do-list and notes there. Also I want to create my digital doppelganger, that will answer unimportant messages (elder relatives for example), make access telegram chats, manage databases, files, to-do-list, do research, find best options on the internet, etc.. Currently, I have the gemini-cli agent on my linux OS home machine and on my VPS and in the future browser with AI agent able to interact with websites' GUI.

1. The Infrastructure: A bash script to set up the file structure, synchronization, and version control.
   `setup_life_database.sh` sets up a directory structure optimized for LLM reading (The PARA Method), initializes Git for history, and sets up a Python environment.
2. The Brain (RAG System): A Python engine to index your notes so any LLM can query them.
   `brain.py` allows your "Digital Doppelganger" to actually know what is in your database. It watches your Markdown files, turns them into vectors, and stores them. It also provides a function to query that data.
3. The Doppelganger (Telegram Agent): A script to handle messaging automation.
   `telegram_agent.py` uses Telethon to log in as you (not a bot). It monitors messages and uses the LLM to draft replies for specific people.

# Instructions on how to install and run app

```bash
# optional
# python3 -m venv venv
source venv/bin/activate

chmod +x setup_life_database.sh
./setup_life_database.sh

python3 99_System/scripts/api.py
```

Query example:

```bash
curl -s -X POST http://127.0.0.1:8000/query \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"What is in my inbox?"}'
```

# LifeOS: Architecture & Workflow Strategy

1. The Core Philosophy
   System is running on a VPS. System is built on Plain Text Files (Markdown). Vectorized Knowledge Base (Markdown + Vector Store) which is native to how LLMs "think."
   This is the only format that ensures:

- Longevity: Readable in 2050.
- AI Compatibility: Easily parsed by gemini-cli, Python scripts, and your Comet browser.
- Syncability: Git, Syncthing, or Dropbox work flawlessly.

2. Managing the Doppelganger
   The "Watcher" Workflow
   Python script (`brain.py`) runs automatically when files change.
   Manual Update: Run python3 `brain.py` whenever you add a massive amount of data.
   Automated Research (Browser agent): ask Browser-use to research "Best hiking boots 2025".

   - Browser agent saves a summary to LifeOS/00_Inbox/Hiking_Boots.md.
   - (Optional) Create a Linux watchdog script that detects new .md files and triggers update_database().

   The Telegram Agent

   - Security: Telegram bans accounts that behave like spambots.
   - Safety Rule: Only enable auto-reply for specific users (White-listing), never for "All contacts.
   - Needs 24/7 uptime to reply to messages instantly.

3. To-Do List & Notes Integration
   The Input Method
   Don't write directly to the database manually every time. Use a "Capture" mechanism.

- On Linux (Terminal):Create a bash alias in your .bashrc:

```bash
alias todo='nano ~/LifeOS/00_Inbox/todo.md'
alias log='echo "$(date): $1" >> ~/LifeOS/00_Inbox/Daily_Log.md'
```

Usage: log "Had a call with John about project X"

The AI Review
Use your gemini-cli to review your day. Command:

```bash
gemini "Read ~/LifeOS/00_Inbox/Daily_Log.md and summarize my key achievements today and what I forgot to do."
```

4. Next Steps for Expansion
   Calendar: Use the Google Calendar API in Python to let the Agent read your schedule.
   TaskWarrior: If plain text to-dos are too simple, install TaskWarrior on Linux and export the list to JSON for the AI to read.

# API Endpoints Examples

Here are some curl commands to test the API endpoints:

## Creating and Viewing Documents

To create a document and obtain its ID, use the `POST /documents` endpoint:

```bash
curl -X POST "http://127.0.0.1:8000/documents" \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer $API_TOKEN" \
 -d '{
"content": "This is a test document about software engineering",
"metadata": {"source": "test_script", "author": "gemini"}
}'
```

- Note the `id` from the response for update/delete operations.

To view document content, you can use the `POST /documents/search` endpoint. You can search using keywords and specify the number of results (`k`).

```bash
curl -X POST "http://127.0.0.1:8000/documents/search" \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer $API_TOKEN" \
 -d '{
"query_text": "software engineering",
"k": 2
}'
```

The results will contain the `id`, `content` and `metadata` of the matching documents.

## Updating a Document

To update a document, use the `PUT /documents/{doc_id}` endpoint, replacing `<DOC_ID>` with the ID obtained from the create operation:

```bash
curl -X PUT "http://127.0.0.1:8000/documents/<DOC_ID>" \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer $API_TOKEN" \
 -d '{
"content": "This is an updated document about software development best practices.",
"metadata": {"source": "test_script", "author": "gemini"},
"version": "2"
}'
```

## Deleting a Document

To delete a document, use the `DELETE /documents/{doc_id}` endpoint, replacing `<DOC_ID>` with the ID of the document:

```bash
curl -X DELETE "http://127.0.0.1:8000/documents/<DOC_ID>" \
 -H "Authorization: Bearer $API_TOKEN"
```

## Triggering a Full Database Re-index

To re-index the entire database, use the `POST /update` endpoint:

```bash
curl -X POST "http://127.0.0.1:8000/update" \
 -H "Authorization: Bearer $API_TOKEN"
```
