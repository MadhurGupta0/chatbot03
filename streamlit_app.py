# Code refactored from https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps

import openai
import streamlit as st
import requests as res
from pathlib import Path
from streamlit_lottie import st_lottie
sa = ""
st.title("Chatbot")
def lottie_url(url):
    r= res.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie_ff= lottie_url("https://lottie.host/b0e7a727-7511-4b6e-9ab1-75695558e263/uezJK5yfZ0.json")
with st.sidebar:
    try:
     st_lottie(lottie_ff, height=300, key="random")
    except:
        pass
    st.title(' AI CHATBOT/ COPY CHATBOT ')
    if 'OPENAI_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        sa = st.secrets['OPENAI_API_KEY']
    else:
        openai.api_key = st.text_input('Enter OpenAI API token to use as AI Chatbot :', type='password')
        if not (openai.api_key.startswith('sk-') and len(openai.api_key) == 51):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
if openai.api_key:
    client = openai.OpenAI(api_key=sa, )
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    prompt = st.chat_input("AI CHAT BOT")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            try :

             for response in client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": m["role"], "content": m["content"]}
                              for m in st.session_state.messages]):
                full_response += response.choices[0].content
                message_placeholder.markdown(full_response + "▌")
                st.success("It is working fine now.")
            except:
              st.warning("There is some issue with chatbot.It is working as Copybot.")
              full_response=st.session_state.messages[-1]["content"]
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
else:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    prompt = st.chat_input("Copy bot")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            full_response += st.session_state.messages[-1]["content"]
            message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
if len(st.session_state.messages)>11:
    st.session_state.messages.pop(0)
