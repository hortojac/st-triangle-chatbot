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
            background-position: left 2rem center;  /* Adjusted position */
            background-size: auto 4rem;  /* Auto width, 4rem height */
        }
    </style>
    """, unsafe_allow_html=True,
)

# Custom CSS to center the title
st.markdown("""
    <style>
        .stHeadingContainer {
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True,
)
st.header("Chat with the KU Triangle ChatBot &Delta;", divider='gray')

# Custom CSS for the buttons
st.markdown("""
    <style>
        .row-widget.stLinkButton a {
            background-color: #0e3745;
        }
        .row-widget.stLinkButton a:hover {
            background-color: #990033;
        }
    </style>
    """, unsafe_allow_html=True,
)

# Social Media Links
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.link_button(":globe_with_meridians: Website", "https://kutriangle.org", use_container_width=True)
with col2:
    st.link_button(":speech_balloon: Facebook", "https://www.facebook.com/KUTriangle", use_container_width=True)
with col3:
    st.link_button(":camera: Instagram", "https://www.instagram.com/kutriangle/", use_container_width=True)
with col4:
    st.link_button(":bird: Twitter", "https://twitter.com/KUTriangle", use_container_width=True)
with col5:
    st.link_button(":moneybag: Donate", "https://www.paypal.com/donate/?hosted_button_id=AGBB3YBDR73NW", use_container_width=True)

# Disclaimer and instructions
st.markdown("**Disclaimer:** *This chatbot provides responses based on its accessible resources and knowledge base, which may not encompass all details relevant to your inquiry. If you receive an incomplete response or no information related to your question, it may be a result of the chatbot's current knowledge limitations. In such instances, try rewording or elaborating on your question for more precise assistance. For complex inquiries or topics beyond the chatbot's capacity, please consult the chapter's current Recruitment Chair for further guidance.*")
         
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

# Custom Footer
st.markdown("""
    <style>
        .footer {
            color: #FFFFFF;
            font-size: 1.25rem;
            padding: 0.5rem;
            position: fixed;
            left: 0;
            bottom: 0;
            width: auto;
        }
    </style>
    """, unsafe_allow_html=True,
)

# Add footer to the bottom of the page
footer = """
    <div class="footer">
        &copy; Kansas Chapter of Triangle Fraternity
    </div>
    """
st.markdown(footer, unsafe_allow_html=True)


