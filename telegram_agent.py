import asyncio
import os
from telethon import TelegramClient, events
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load Config
load_dotenv()
API_ID = int(os.getenv("TELEGRAM_API_ID")) if os.getenv("TELEGRAM_API_ID") else None
API_HASH = os.getenv("TELEGRAM_API_HASH")
# Allow overriding the LifeOS path (so n8n or remote agents can point to a custom folder)
LIFE_OS_PATH = os.getenv("LIFE_OS_PATH", os.path.expanduser("~/LifeOS"))
SESSION_NAME = os.path.join(LIFE_OS_PATH, '99_System', 'scripts', 'doppelganger_session')

# Define "Low Priority" contacts (Username or Phone)
# The agent will auto-reply to these people.
AUTO_REPLY_LIST = ['some_relative_username', '+1234567890']

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

async def generate_polite_reply(incoming_text, sender_name):
    """
    Generates a polite, low-commitment response.
    """
    prompt = (
        f"You are my personal assistant handling messages while I work. "
        f"A relative named {sender_name} sent this: '{incoming_text}'. "
        f"Draft a polite, brief, warm response in my voice. "
        f"Do not promise I will call immediately. Keep it under 2 sentences."
    )
    response = await llm.ainvoke(prompt)
    return response.content

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    sender = await event.get_sender()
    sender_id = sender.username if sender.username else str(sender.id)
    
    # Check if sender is in the auto-reply list
    if sender_id in AUTO_REPLY_LIST:
        print(f"📩 Message from {sender_id}: {event.raw_text}")
        
        # Artificial delay to look human
        await asyncio.sleep(5) 
        
        reply_text = await generate_polite_reply(event.raw_text, sender.first_name)
        
        # Send reply (or just draft it/log it if you want to be safe)
        await event.reply(reply_text)
        print(f"✅ Auto-replied: {reply_text}")

print("🤖 Doppelganger Active. Listening for messages...")
client.start()
client.run_until_disconnected()