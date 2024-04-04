import streamlit as st
from streamlit_chat import message
from langchain_openai import OpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import (ConversationBufferMemory, 
																									ConversationSummaryMemory, 
																									ConversationBufferWindowMemory
																									)

#Session variables

#Handles the conversation state
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = None

#Handles the messages created on the resopnse_container 
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

#Header and Sidebar

st.set_page_config(page_title="Chat Summarizer", page_icon='🤖')
st.markdown("<h1 style='text-align: center; color: #ff69b4;'>What can I do for you?</h1>", unsafe_allow_html=True)

st.sidebar.title("😎")
api_key = st.sidebar.text_input("OpenAI API Key", type="password")
summarize_button = st.sidebar.button("Summarize convo", key="summarize")

if summarize_button:
	summarize_placeholder = st.sidebar.write("Nice chatting with you 😊 :\n\n" + "Hello dude!")
	
import os
os.environ["OPENAI_API_KEY"] = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx" #Please replace the key with your OpenAI API key

def get_response(user_input):
    
    if st.session_state['conversation'] is None:
        llm = OpenAI(
                temperature=0,
                model_name='gpt-3.5-turbo-instruct'
        )
        
        #Using session variable to store the conversation
        st.session_state['conversation'] = ConversationChain(
                llm=llm,
                verbose=True,
                memory=ConversationBufferMemory()
        )
    
    response = st.session_state['conversation'].predict(input=user_input)
    print(st.session_state['conversation'].memory.buffer)
    
    return response

response_container = st.container()
# Here we create a container for the form
container = st.container()

with container:
    with st.form(key="my_form", clear_on_submit=True):
        user_input = st.text_area("Your message goes here", key='input', height=100)
        submit_button = st.form_submit_button(label="Send")
        if submit_button:
            
            #Appends every user input and model response to the session state and displays it in the UI
            st.session_state['messages'].append(user_input)
            model_response = get_response(user_input)
            st.session_state['messages'].append(model_response)
            #st.write(st.session_state['messages'])
            
            with response_container:
                for i in range(len(st.session_state['messages'])):
                    if (i % 2) == 0:
                        message(st.session_state['messages'][i], is_user=True, key=str(i) + '🙋')
                    else:
                        message(st.session_state['messages'][i], key=str(i) + '🤖')
    