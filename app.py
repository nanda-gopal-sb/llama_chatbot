import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
# initialize the client
client = OpenAI(
  base_url="https://api-inference.huggingface.co/v1",
  api_key= os.getenv("TOKEN")
)

#Pull info about the model to display
model = "meta-llama/Meta-Llama-3-8B-Instruct"

def reset_conversation():
    st.session_state.conversation = []
    st.session_state.messages = []
    return None




if "prev_option" not in st.session_state:
    st.session_state.prev_option = model

if st.session_state.prev_option != model:
    st.session_state.messages = []
    st.session_state.prev_option = model
    reset_conversation()

st.subheader("Debyez Chatbot")
#intialize the session state of streamlit
if model not in st.session_state:
    st.session_state[model] = model 
if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#get user input
if prompt := st.chat_input("Hi I'm a chatbot"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": m["role"], "content": (m["content"])}
                    for m in st.session_state.messages
                ],
                temperature=0.5,
                stream=True,
                max_tokens=3000,
            )
            response = st.write_stream(stream)
        except Exception as e:
            response = "An error occurred: {}".format(str(e))
            st.write(response)
            st.write("This was the error message:")
            st.write(e)
    st.session_state.messages.append({"role": "assistant", "content": response})