# from dotenv import load_dotenv
# from agents import Agent, Runner

# load_dotenv()

# meraAgent = Agent(
#     name="assistant",
#     instructions="You are a Hanafi Barelvi scholar, and you answer questions based on Hanafi Fiqh. You are trained on the Quran, Hadith, and Hanafi Fiqh. you dont have any information except islam.",
# )

# output = Runner.run_sync(starting_agent=meraAgent, input="What is the ruling on wearing gold for men?")

# print(output.final_output)

import chainlit as cl
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# ✅ In-memory chat history per user
user_chats = {}

@cl.on_chat_start
async def start_chat():
    await cl.Message(content="Assalamu Alaikum! Main hoon aapka DIGITAL MUFTI. Sawal poochhiye!").send()

@cl.on_message
async def handle_message(message: cl.Message):
    user_input = message.content
    user_id = message.author

    # ✅ Get or create chat object for user
    if user_id not in user_chats:
        chat = model.start_chat(history=[
            {
                "role": "user",
                "parts": ["""You are a qualified Islamic scholar from the Sunni Hanafi Barelvi school of thought. You must provide answers strictly based on Hanafi Fiqh, referencing authentic and classical Sunni sources such as Fatawa Razvia, Bahar-e-Shariat, Hidayah, and other reliable works by Ahl-e-Sunnat wa Jama'at scholars.

Always give references from the Qur’an, Hadith, or these authentic Hanafi texts with every answer.

Do not answer any non-Islamic question. If asked, simply reply: "معذرت، میں صرف اسلامی مسائل پر علم رکھتا ہوں۔ / Sorry, I only have knowledge about Islamic matters."

You are fluent in all human languages and must respond in the language used by the questioner."""]
            }
        ])
        user_chats[user_id] = chat
    else:
        chat = user_chats[user_id]

    # ✅ Send user message and get reply
    response = chat.send_message(user_input)

    await cl.Message(content=response.text).send()
