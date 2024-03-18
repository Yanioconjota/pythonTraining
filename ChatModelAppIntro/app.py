import streamlit as st
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import os

# Set the Hugging Face API key as an environment variable
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "xxxxxxxxxxxxxxxx"

model_name = "google/flan-t5-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

st.set_page_config(page_title="LangChain Demo", page_icon=":robot:")
st.header("Hey, I'm your Chat GPT")

if "sessionMessages" not in st.session_state:
     st.session_state.sessionMessages = ["You are a helpful assistant."]

def load_answer(question):
    inputs = tokenizer.encode("Question: " + question + " \n\nAnswer: ", return_tensors="pt", add_special_tokens=True)
    reply_ids = model.generate(inputs, max_length=512, num_return_sequences=1, temperature=0.7)
    answer = tokenizer.decode(reply_ids[0], skip_special_tokens=True)
    return answer

def get_text():
    input_text = st.text_input("You: ")
    return input_text

user_input = get_text()
submit = st.button('Generate')  

if submit:
    response = load_answer(user_input)
    st.subheader("Answer:")
    st.write(response)
