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
st.header("Chat with the KU Triangle ChatBot", divider='gray')
         
# Initialize chat messages history
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about the Kansas Chapter of Triangle Fraternity!"}
    ]

# Load data function
@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing the Triangle information – hang tight! This should take 1-2 minutes."):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an expert on the Kansas Chapter of Triangle Fraternity and the National Fraternity Organization. Your job is to answer informative questions. Assume that all questions are related to the Kansas Chapter of Triangle or Nationals. Keep your answers informative and based on facts – do not hallucinate features."))
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
