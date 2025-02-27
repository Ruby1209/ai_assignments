import streamlit as st
from openai import OpenAI
import dotenv
import os
from PIL import Image
import base64
from io import BytesIO
import accept_files

    
def main():

    # --- Page Config ---
            st.set_page_config(
                page_title="The FraudLens Chat",
                page_icon="🤖",
                layout="centered",
                initial_sidebar_state="expanded",
            )
                # --- Header ---
            st.html("""<h1 style="text-align: center; color: #6ca395;">🤖 <i>FraudLens Chat</i> 💬</h1>""")
                # --- Side Bar ---
            with st.sidebar:
                st.html("""<h1 style="text-align: center; color: #6ca395;">Upload your docs for KYC</h1>""")
                st.divider()
        # --- Main Content ---
            with st.sidebar:
                doc_type = st.selectbox("Select document type:", [
                    "Selfie", 
                    "Address Proof",
                    "Passport", 
                ], index=0
                ,placeholder="Select document type")
                st.divider()
               
                cols_img = st.columns(2)
                with cols_img[0]:
                    with st.popover("📁 Upload"):
                        uploaded_file = st.file_uploader("Choose a file", type=["jpeg", "pdf", "png", "jpg"],key="file_uploader")
                        if uploaded_file is not None:
                            st.session_state.uploaded_img = uploaded_file
                            accept_files.accept_files(doc_type,uploaded_file)
                with cols_img[1]:                    
                    with st.popover("📸 Camera"):
                        activate_camera = st.checkbox("Activate camera")
                        if activate_camera:
                            st.camera_input(
                                "Take a picture", 
                                key="camera_img",
                            )
                if st.button("Validate 🔍"):
                        evaluation_result=accept_files.compare_images()
                        st.write("evaluation_result::",evaluation_result)
                # Chat input
            if prompt := st.chat_input("Hi! Ask me anything..."):
                st.session_state.messages.append(
                    {
                        "role": "user", 
                        "content": [{
                            "type": "text",
                            "text": prompt,
                        }]
                    }
                )
                # Displaying the new messages
                with st.chat_message("user"):
                    st.markdown(prompt)
if __name__ == "__main__":
    main()