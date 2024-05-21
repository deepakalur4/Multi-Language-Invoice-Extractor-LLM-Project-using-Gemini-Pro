from dotenv import load_dotenv
import PIL
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Function to load a Gemini pro vision

model=genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(input,image,prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()
        image_parts=[
            {
                "mime_type":uploaded_file.type,
                "data":bytes_data
            }

        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


st.set_page_config(page_title="Multi language invoice extracter")


st.header("Multi language invoice extracter")
inputs=st.text_input("Input Prompt: ",key="input")
uploaded_file=st.file_uploader("Choose an image of the invoice : ",type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image=PIL.Image.open(uploaded_file)
    st.image(image,caption="uploaded Image", use_column_width=True)

submit=st.button("Tell me about the invoice")


input_prompt='''
You are an expert in understanding a invoices, We will upload a image of invoices and you wil have to answer 
any questions based on the uploaded invoice image
'''

#If submit button is cliked
if submit:
    image_data=input_image_details(uploaded_file)
    response=get_gemini_response(input=input_prompt,image=image_data,prompt=inputs)
    st.subheader("The response is")
    st.write(response)
