import streamlit as st

from langchain_openai import OpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import (ConversationBufferMemory, 
																									ConversationSummaryMemory, 
																									ConversationBufferWindowMemory
																									)

#Header and Sidebar

st.set_page_config(page_title="Chat Summarizer", page_icon='🤖')
st.markdown("<h1 style='text-align: center; color: #ff69b4;'>What can I do for you?</h1>", unsafe_allow_html=True)

st.sidebar.title("😎")
api_key = st.sidebar.text_input("OpenAI API Key", type="password")
summarize_button = st.sidebar.button("Summarize convo", key="summarize")

if summarize_button:
	summarize_placeholder = st.sidebar.write("Nice chatting with you 😊 :\n\n" + "Hello dude!")
	
import os
os.environ["OPENAI_API_KEY"] = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" #Please replace the key with your OpenAI API key

def getResponse(userInput):
    llm = OpenAI(
            temperature=0,
            model_name='gpt-3.5-turbo-instruct'
    )

    conversation = ConversationChain(
            llm=llm,
            verbose=True,
            memory=ConversationBufferMemory()
    )

    conversation("Good morning AI!")
    conversation("My name is Homero!")
    conversation.predict(input="I live in Springfield, USA")
    print(conversation.memory.buffer)
    response = conversation.predict(input="What is my name?")
    
    return response

response_container = st.container()
# Here we create a container for the form
container = st.container()

with container:
    with st.form(key="my_form", clear_on_submit=True):
        user_input = st.text_area("Your message goes here", key='input', height=100)
        submit_button = st.form_submit_button(label="Send")
        if submit_button:
            answer = getResponse(user_input)
            with response_container:
                st.write(answer)
    