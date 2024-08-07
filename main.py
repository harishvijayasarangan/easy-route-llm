import streamlit as st
import openai 
import os
from routellm.controller import Controller

# Set the OpenAI API key using the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize the Controller
client = Controller(
    routers=["mf"],
    strong_model="gpt-4-1106-preview",
    weak_model="ollama_chat/llama3",
)

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #1e1e1e;
            color: #f5f5f5;
            font-family: 'Arial', sans-serif;
        }
        .route-title {
            font-size: 2.8rem;
            font-weight: bold;
            margin-bottom: 1rem;
            color: #ff6600;
            text-align: center;
        }
        .input-prompt {
            font-size: 1.2rem;
            margin-bottom: 0.5rem;
            color: #cccccc;
        }
        .response-box {
            background-color: #2b2b2b;
            border-radius: 5px;
            padding: 1.5rem;
            margin-top: 1.5rem;
            border: 1px solid #444444;
        }
        .upload-section {
            margin-top: 2rem;
            background-color: #2b2b2b;
            border-radius: 5px;
            padding: 1.5rem;
            border: 1px solid #444444;
        }
        .upload-section h3 {
            margin-bottom: 1rem;
            color: #ff6600;
        }
        .file-upload {
            margin-bottom: 1.5rem;
        }
        .stButton>button {
            background-color: #ff6600;
            color: #ffffff;
        }
    </style>
""", unsafe_allow_html=True)

# Streamlit UI
st.markdown('<div class="route-title">Route LLM</div>', unsafe_allow_html=True)
st.write("Enter your prompt and get a response from the chatbot.")

# Get user input from the web interface
user_prompt = st.text_input("Enter your prompt:", "", placeholder="Type your message here...", help="Type your message and press Enter.")

# Handle user input and display response
if user_prompt:
    try:
        # Create a chat completion request
        response = client.chat.completions.create(
            model="router-mf-0.11593",
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )

        # Extract response content
        message_content = response['choices'][0]['message']['content']
        model_name = response['model']

        # Display response
        st.markdown(f'<div class="response-box"><b>Response from {model_name}:</b><br>{message_content}</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")

# File upload sections
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
st.markdown('<h3>Upload files for more context (images, documents, etc.):</h3>', unsafe_allow_html=True)

# Image upload
uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"], key="image_upload")
if uploaded_image:
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True, output_format="auto")
st.markdown('<div class="file-upload"></div>', unsafe_allow_html=True)

# Document upload
uploaded_document = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"], key="doc_upload")
if uploaded_document:
    st.write(f"Uploaded Document: {uploaded_document.name}")
st.markdown('<div class="file-upload"></div>', unsafe_allow_html=True)

# Attachment upload
uploaded_attachment = st.file_uploader("Upload other attachments", type=["zip", "rar", "tar"], key="att_upload")
if uploaded_attachment:
    st.write(f"Uploaded Attachment: {uploaded_attachment.name}")
st.markdown('</div>', unsafe_allow_html=True)
