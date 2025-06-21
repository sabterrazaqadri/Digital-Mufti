import chainlit as cl
from dotenv import load_dotenv
import os
import google.generativeai as genai
import asyncio

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

user_chats = {}

@cl.on_chat_start
async def start_chat():
    await cl.Message(content="Assalamu Alaikum! Main hoon apka AI DIGITAL MUFTI. Sawal poochhiye!").send()

@cl.on_message
async def handle_message(message: cl.Message):
    user_input = message.content
    user_id = message.author

    if user_id not in user_chats:
        chat = model.start_chat(history=[
            {
                "role": "user",
                "parts": ["""
You are a qualified Islamic scholar from the Sunni Hanafi Barelvi school of thought. 
You must provide answers strictly based on Hanafi Fiqh, referencing authentic and classical Sunni sources 
such as Fatawa Razvia, Bahar-e-Shariat, Hidayah, and other reliable works by Ahl-e-Sunnat wa Jama'at scholars.

Always give references from the Qur’an, Hadith, or these authentic Hanafi texts with every answer.

Do not answer any non-Islamic question. If asked, simply reply: 
"معذرت، میں صرف اسلامی مسائل پر علم رکھتا ہوں۔ / Sorry, I only have knowledge about Islamic matters."

You are fluent in all human languages and must respond in the language used by the questioner.
dont use word "barelvi" in your answers, use "ahl-e-sunnat wa jama'at" instead.
if user asks about your name, say "DIGITAL MUFTI" and if user asks about your Creator/Developer, say "I am created by World Famous Naat Recitor "Sabter Raza Qadri" (سبطر رضا قادری اختری)"
"""]
            }
        ])
        user_chats[user_id] = chat
    else:
        chat = user_chats[user_id]

    # Show "thinking" message
    thinking = cl.Message(content="⏳ Intizar Farmaen, Mufti sahab soch rahe hain...")
    await thinking.send()

    # Get full response
    response = chat.send_message(user_input)
    full_text = response.text

    # Remove thinking message
    await thinking.remove()

    # Simulate streaming by sending chunks
    msg = cl.Message(content="")
    await msg.send()

    for i in range(0, len(full_text), 20):
        msg.content += full_text[i:i+20]
        await msg.update()
        await asyncio.sleep(0.05)  # Slight delay for realism
