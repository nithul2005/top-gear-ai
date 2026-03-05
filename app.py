import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# 1. SETUP
load_dotenv()
# Using the stable llama-3.3-70b-versatile for high-quality technical answers
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 2. UI DESIGN: Automotive Dark Dashboard
st.set_page_config(page_title="Top Gear AI", page_icon="🏎️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #ffffff; }
    h1 { color: #e74c3c; text-transform: uppercase; border-bottom: 2px solid #e74c3c; }
    [data-testid="stChatMessage"] { 
        background-color: #1a1a1a; 
        border-left: 5px solid #e74c3c; 
        border-radius: 10px;
    }
    .stChatInputContainer { padding-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏁 TOP GEAR: AI MECHANICAL DIAGNOSTIC")
st.caption("No-Image Professional Technical Support & Troubleshooting")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 3. CORE LOGIC
user_input = st.chat_input("Ask about a vehicle spec or describe a mechanical issue (e.g., 'My bike is knocking')...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        user_lower = user_input.lower().strip()
        
        # --- A. FIXED GREETING ---
        if user_lower in ["hi", "hello", "hey", "hii"]:
            reply = "Engine Start... 🏁 Welcome to Top Gear AI. I am ready to provide technical specs or help you fix any bike/car mechanical issue. What's wrong with your machine today?"
            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        
        else:
            with st.spinner("🔧 ANALYZING SYSTEM DIAGNOSTICS..."):
                response = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system", 
                            "content": """You are a Master Automotive Mechanic. 
                            1. If the user asks for specs, provide a massive detailed report in bold bullet points.
                            2. If the user describes a problem (e.g., knocking, not starting, overheating), provide a step-by-step resolution guide. 
                            3. Use bold headers for Engine, Electrical, and Mechanical checks. 
                            4. Always prioritize safety first."""
                        },
                        {"role": "user", "content": f"User Request: {user_input}"}
                    ]
                )
                bot_reply = response.choices[0].message.content
                st.markdown(bot_reply)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply}) 