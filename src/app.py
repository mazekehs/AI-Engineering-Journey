import streamlit as st
from groq import Groq
from google import genai
from core.config import config


# -----------------------------------
# LLM FUNCTION
# -----------------------------------
def run_llm(provider, model_name, messages, max_tokens=500):

    if provider == "Groq":
        client = Groq(api_key=config.GROQ_API_KEY)

        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_completion_tokens=max_tokens
        )

        return response.choices[0].message.content

    elif provider == "Google":
        client = genai.Client(api_key=config.GEMINI_API_KEY)

        # Convert our common message format to Gemini format
        gemini_messages = []

        for message in messages:
            role = message["role"]

            # Gemini uses "model" instead of "assistant"
            if role == "assistant":
                role = "model"

            gemini_messages.append(
                {
                    "role": role,
                    "parts": [
                        {
                            "text": message["content"]
                        }
                    ]
                }
            )

        response = client.models.generate_content(
            model=model_name,
            contents=gemini_messages
        )

        return response.text

    else:
        raise ValueError(f"Unsupported provider: {provider}")


# -----------------------------------
# SIDEBAR SETTINGS
# -----------------------------------
with st.sidebar:
    st.title("⚙️ Settings")

    provider = st.selectbox(
        "Provider",
        ["Groq", "Google"]
    )

    if provider == "Groq":
        model_name = st.selectbox(
            "Model",
            ["llama-3.3-70b-versatile"]
        )

    else:
        model_name = st.selectbox(
            "Model",
            ["gemini-2.5-flash"]
        )

    # Store selected provider and model
    st.session_state.provider = provider
    st.session_state.model_name = model_name


# -----------------------------------
# INITIALIZE CHAT HISTORY
# -----------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! How can I assist you today?"
        }
    ]


# -----------------------------------
# DISPLAY CHAT HISTORY
# -----------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -----------------------------------
# USER INPUT
# -----------------------------------
if prompt := st.chat_input("Type your message here..."):

    # Add user message to history
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)


    # -----------------------------------
    # GENERATE AI RESPONSE
    # -----------------------------------
    with st.chat_message("assistant"):

        answer = run_llm(
            provider=st.session_state.provider,
            model_name=st.session_state.model_name,
            messages=st.session_state.messages
        )

        st.markdown(answer)


    # Add assistant response to history
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )