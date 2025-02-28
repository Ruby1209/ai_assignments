import streamlit as st
import fraudLens_controller

evaluation_result =""  
def main():

    # --- Page Config ---
            st.set_page_config(
                page_title="The FraudLens Assistant",
                page_icon="🤖",
                layout="centered",
                initial_sidebar_state="expanded",
            )
            # --- Header ---
            prompt = """
            <p style="color:#6ca395;"><b>Welcome to the FraudLens Assistant!</b></p>
            <ul>
                <li><b>I'm here to help you with your KYC process.</b></li>
                <li><b>You can upload your documents or take a picture with your camera.</b></li>
                <li><b>I can help you validate your documents and answer any questions you may have.</b></li>
                <li><b>How can I help you today?</b></li>
            </ul>"""
            st.html("""<h2 style="text-align: center; color: #6ca395;">🤖 <i>FraudLens Assistant</i></h2>""")
            with st.chat_message("Assistant"):
                    st.markdown(prompt,unsafe_allow_html=True)
            if 'messages' not in st.session_state:
                st.session_state.messages = []
                # --- Side Bar ---
            with st.sidebar:
                st.html("""<h1 style="text-align: center; color: #6ca395;">Upload your docs for KYC</h1>""")
                st.divider()
        # --- Main Content ---
            with st.sidebar:
                doc_type = st.selectbox("Select document type:", [
                    "Select document",
                    "Selfie", 
                    "Address Proof",
                    "Passport", 
                ], index=0
                ,placeholder="Select document type")
                st.divider()
               
                cols_img = st.columns(2)
                # Upload input
                with cols_img[0]:
                    with st.popover("📁 Upload",disabled= (doc_type == "Selfie" or doc_type=="Select document") ):
                        uploaded_file = st.file_uploader("Choose a file", type=["jpeg", "pdf", "png", "jpg"],key="file_uploader",
                        )
                        if uploaded_file is not None:
                            st.session_state.uploaded_img = uploaded_file
                            fraudLens_controller.accept_files(doc_type,uploaded_file)
                 # Camera input           
                with cols_img[1]:
                        with st.popover("📸 Camera", disabled=(doc_type != "Selfie" or doc_type=="Select document")):
                            activate_camera = st.checkbox("Activate camera")
                            if activate_camera:
                                st.camera_input(
                                    "Take a picture", 
                                    key="camera_img",
                 
                         )
                cols_btn = st.columns(2)
                with cols_btn[0]:
                # Validate button
                    if st.button("Validate 🔍",key="validate",disabled=(doc_type=="Select document")):
                            evaluation_result=fraudLens_controller.compare_images()
                            st.session_state.messages.append(
                            {
                                "role": "assistant", 
                                "content": [{
                                    "type": "text",
                                    "text": evaluation_result,
                                }]
                            }
                     )
                # Reset button
                with cols_btn[1]:      
                    if st.button("🗑️ Reset"):
                        if "messages" in st.session_state and len(st.session_state.messages) > 0:
                                    st.session_state.pop("messages", None)
                                    doc_type = "Select document"
                                    st.session_state.pop("uploaded_img", None)
                                    st.session_state.pop("camera_img", None)
                                    fraudLens_controller.save_file.clear()
                                    st.session_state.messages = []
                            
                        
             # Display chat messages
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    for content in message["content"]:
                        if content["type"] == "text":
                            st.markdown(content["text"])
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