import streamlit as st
import requests

st.set_page_config(page_title="PDF Chatbot", layout="centered")

st.title("📄 PDF Chatbot")

# -Uploading PDF Section here
st.header("📤 Upload a PDF Document")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
    response = requests.post("http://127.0.0.1:8000/upload/", files=files)

    if response.status_code == 200:
        st.success("✅ PDF uploaded and processed successfully!")
    else:
        st.error(f"❌ Error uploading PDF ({response.status_code})")

# -Chat Section
st.header("💬 Chat with Your Document")

user_query = st.text_input("Ask a question")

if st.button("Submit"):
    if user_query:
        try:
            response = requests.post(
                "http://127.0.0.1:8000/chat/", 
                params={"query": user_query} 
            )

            if response.status_code == 200:
                chatbot_response = response.json().get("response", "No response received.")
                
                st.markdown(f"""
                <div style="background-color:#f1f1f1;padding:10px;border-radius:5px;">
                <strong>Chatbot:</strong> {chatbot_response}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"⚠️ Error retrieving response ({response.status_code})")
        
        except Exception as e:
            st.error(f"⚠️ API request failed: {str(e)}")
