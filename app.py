import os
from PIL import Image
from pathlib import Path
from utils import utils
import streamlit as st
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv; load_dotenv()
from lyzr import QABot

# Setup your config
st.set_page_config(
    page_title="Literature Review",
    layout="centered",  # or "wide" 
    initial_sidebar_state="auto",
    page_icon="./logo/lyzr-logo-cut.png"
)

# Load and display the logo
image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Literature Review by Lyzr")
st.markdown("### Welcome to the Literature Review!")
st.markdown("Literature Review by Lyzr is a tool that helps researchers and students quickly summarize and analyze research papers.")

# Custom function to style the app
def style_app():
    # You can put your CSS styles here
    st.markdown("""
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# Literature Review Application
    
# replace this with your openai api key or create an environment variable for storing the key.
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY') 

data = "data"
os.makedirs(data, exist_ok=True)



def literature_review():
    # "This function will implement the Lyzr's QA agent to review the Research Paper"
    path = utils.get_files_in_directory(data)
    path = path[0]
    
    reviewer = QABot.pdf_qa(
        input_files=[Path(path)]
    )
    
    return reviewer


def file_checker():
    file = []
    for filename in os.listdir(data):
        file_path = os.path.join(data, filename)
        file.append(file_path)

    return file


if __name__ == "__main__":
    style_app()
    research_paper = st.file_uploader("Choose Resarch paper", type=["pdf"])
   
    if research_paper is not None:
        utils.save_uploaded_file(directory=data, uploaded_file=research_paper)
        file = file_checker()
        if len(file)>0:
            if st.button("Review"):
                research_review = literature_review()
                responses = utils.reviewer(agent=research_review)
                if responses is not None:
                    utils.get_response(response=responses)
       
    else:
        st.warning('Please upload a research paper in pdf')
    

    with st.expander("ℹ️ - About this App"):
        st.markdown("""
        This app uses Lyzr QABot agent to review the research paper and provide the summary of that paper. The QABot agent is built on the powerful Retrieval-Augmented Generation (RAG) model, enhancing your ability to extract valuable insights. For any inquiries or issues, please contact Lyzr.
        
        """)
        st.link_button("Lyzr", url='https://www.lyzr.ai/', use_container_width = True)
        st.link_button("Book a Demo", url='https://www.lyzr.ai/book-demo/', use_container_width = True)
        st.link_button("Discord", url='https://discord.gg/nm7zSyEFA2', use_container_width = True)
        st.link_button("Slack", url='https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw', use_container_width = True)