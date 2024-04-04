import streamlit as st
from streamlit_chat import message
from langchain_openai import OpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import (ConversationBufferMemory)

#Handles API key authentication
def validate_api_key(api_key):
    try:
        llm = OpenAI(
            temperature=0,
            openai_api_key=api_key,
            model_name='gpt-3.5-turbo-instruct'
        )
        #A call with meaningless input to test the API key
        test_response = llm.invoke("Hello world")
        return True  #Return True if the API key is valid
    except Exception as e:
        print(f"Error validating API key: {e}")
        return False

#Session variables

#Handles the conversation state
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = None

#Handles the messages created on the resopnse_container 
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
    
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = ''

#Header and Sidebar

st.set_page_config(page_title="Chat Summarizer", page_icon='🤖')
st.markdown("<h1 style='text-align: center; color: #ff69b4;'>What can I do for you?</h1>", unsafe_allow_html=True)

st.sidebar.title("😎")
st.session_state['api_key'] = st.sidebar.text_input("OpenAI API Key", type="password")
summarize_button = st.sidebar.button("Summarize convo", key="summarize")

if summarize_button:
    #Checks if there is a conversation to summarize
    if st.session_state['conversation'] is not None:
        conversation_summary = st.sidebar.write("Nice chatting with you 😊:\n\n" + "\n" + st.session_state['conversation'].memory.buffer)
        summarize_placeholder = st.sidebar.write(conversation_summary)
    else:
        summarize_placeholder = st.sidebar.write("Nice chatting with you 😊")

	
def get_response(user_input, api_key):
    
    if st.session_state['conversation'] is None:
        llm = OpenAI(
                temperature=0,
                openai_api_key=api_key,
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
            
            if st.session_state['api_key'] == '' or not validate_api_key(st.session_state['api_key']):
                st.write('You must enter a valid API key to use this feature')
            
            else:    
                model_response = get_response(user_input, st.session_state['api_key'])
                st.session_state['messages'].append(model_response)
                #st.write(st.session_state['messages'])
                
                with response_container:
                    for i in range(len(st.session_state['messages'])):
                        if (i % 2) == 0:
                            message(st.session_state['messages'][i], is_user=True, key=str(i) + '🙋')
                        else:
                            message(st.session_state['messages'][i], key=str(i) + '🤖')
    