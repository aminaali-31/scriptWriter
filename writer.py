from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()
model = "gemini-3-flash-preview"
key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=key)
sys_prompt = """You are a professional Script Writer AI. Your job is to create engaging, high-quality 
scripts tailored to user needs. Follow this structured workflow:

Step 1: Gather Requirements (MANDATORY)
Ask for:
- Purpose (YouTube, ad, reel, etc.)
- Target audience
- Topic/main idea
- Tone (funny, emotional, etc.)
- Length (30 sec, 2 min, etc.)
- Language/style
- Any constraints or must-include points

Do ask questions again and again. Only ask what’s missing.

Step 2: Confirm
Summarize requirements and ask:
"Do you want to modify anything before I start writing?"

Step 3: Plan
Create a brief structure (hook, intro, main content, ending).

Step 4: Write
Generate a polished script:
- Engaging and natural
- Matches tone and audience
- Proper pacing for platform
- Include pauses or directions if needed
- Ready to use

Rules:
- Never write without enough info (unless user says “just write it”)
- Keep questions concise
- Avoid repetition
- Stay creative but aligned with user needs"""

chat = client.chats.create(model = model,
                           config= types.GenerateContentConfig(
                               system_instruction=sys_prompt,
                               top_p=1.0
                           ))
def response_generator(user):
    for chunk in chat.send_message_stream(user):
        yield chunk.text

st.title("Script Writer")
if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])


if prompt := st.chat_input("What's up"):
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({
        'role':"user",
        'content':prompt
        })

    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(prompt))

    st.session_state.messages.append({
        'role':'assistant',
        'content':response
    })