## loading all the environment variables
from dotenv import load_dotenv
load_dotenv() 

import streamlit as st
import os
from PIL import Image
import PIL.Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load Gemini Pro model and get repsonses
def get_gemini_response(question):
    model=genai.GenerativeModel("gemini-pro")
    chat = model.start_chat(history=[])
    response=chat.send_message(question)
    # Uncomment the below line if you want to stream the conversation 
    # response=chat.send_message(question,stream=True)
    return response

##Function to load Gemini Pro vision Model 
def get_gemini_vision_response(uploaded_image,txt_input):
    
    model=genai.GenerativeModel("gemini-pro-vision")
    chat = model.start_chat(history=[])
    img = PIL.Image.open(uploaded_image)
    response = model.generate_content([txt_input,img])
    # Uncomment the below line if you want to stream the conversation 
    # response = model.generate_content([txt_input,img],stream=True)
    return response


##initialize our streamlit app

st.set_page_config(page_title="Q&A Demo")

st.header("Visual QnA: Explore the World Through Your Images")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

txt_input=st.text_input("Input: ",key="input")
submit=st.button("Ask the question")

# if submit and txt_input:
if submit :
    response  = ""
    if uploaded_image:
        st.image(uploaded_image)
        response = get_gemini_vision_response(uploaded_image,txt_input)
        if txt_input == "":
            txt_input = "Read the given Image"
    else:
        response=get_gemini_response(txt_input)

    # st.subheader("The Response is: ")
    st.subheader(txt_input)
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].insert(0,("Bot", chunk.text))
    
    # Add user query and response to session state chat history
    st.session_state['chat_history'].insert(0,("You", txt_input))
st.subheader("Chat History:")
    
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")