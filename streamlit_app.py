import streamlit as st
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms import OpenAI
import openai

# Set page configuration
st.set_page_config(
    page_title="KU Triangle ChatBot",
    page_icon="🔺",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None
)

# API key and title
openai.api_key = st.secrets.openai_key

# Custom CSS for the header
st.markdown("""
    <style>
        [data-testid="stHeader"] {
            background-color: #0e3745;
            height: 5rem;
            background-image: url("https://images.squarespace-cdn.com/content/v1/5edab77f1d34342bd8d942b6/6abeefe1-f357-4992-aa59-dcfe74c726b1/Logotype-Horiz.png?format=1500w");
            background-repeat: no-repeat;
            background-position: left 2rem center;
            background-size: auto 4rem;
        }
    </style>
    """, unsafe_allow_html=True,
)

# Custom CSS for the buttons
st.markdown("""
    <style>
        .row-widget.stLinkButton a {
            background-color: #0e3745;
            width: 100%;
        }
        .row-widget.stLinkButton a:hover {
            background-color: #990033;
        }
    </style>
    """, unsafe_allow_html=True,
)

# Custom CSS for the sidebar
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True,
)

# Custom CSS for the chat input
st.markdown("""
    <style>
        [data-testid="stChatInput"] {
            background-color: #0e3745;
            color: #FFFFFF;
        }
    </style>
    """, unsafe_allow_html=True,
)

# Social Media Links in the Sidebar
with st.sidebar:
    st.markdown("<u>Social Media Links</u>", unsafe_allow_html=True)
    st.link_button(":speech_balloon: Facebook", "https://www.facebook.com/KUTriangle")
    st.link_button(":camera: Instagram", "https://www.instagram.com/kutriangle/")
    st.link_button(":bird: Twitter", "https://twitter.com/KUTriangle")
    st.link_button(":globe_with_meridians: Website", "https://kutriangle.org")
    st.link_button(":envelope: Contact Us", "https://www.kutriangle.org/contact")
    st.link_button(":moneybag: Donate", "https://www.paypal.com/donate/?hosted_button_id=AGBB3YBDR73NW")
    st.markdown("&copy; Kansas Chapter of Triangle Fraternity")

# Header
st.header("KU Triangle ChatBot &#916;")

# Disclaimer and instructions
st.markdown("**Disclaimer:** *This chatbot responds based on its current knowledge, which might not cover all aspects of your inquiry. If a response seems incomplete or unrelated, consider rephrasing your question for clarity. For complex topics beyond the chatbot's scope, please refer to the Recruitment Chair.*")
         
# Initialize chat messages history
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about the Kansas Chapter of Triangle Fraternity!"}
    ]

# Load data function
@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing the data - hang tight! This should take 1-2 minutes."):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an expert on the Kansas Chapter of Triangle Fraternity and the National Triangle Fraternity Organization. Your job is to answer informative questions. Assume that all questions are related to the Kansas Chapter of Triangle or Nationals. Keep your answers informative and based on facts – do not hallucinate features."))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index

index = load_data()

# Initialize chat engine
if "chat_engine" not in st.session_state.keys():
    st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

# User input and chat history
if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Generate new response from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)  # Add response to message history


