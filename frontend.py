import streamlit as st
from researcherII import INITIAL_PROMPT, graph, config
from langchain_core.messages import AIMessage
import logging

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Page Config
st.set_page_config(
    page_title="ScholarBot - Research Assistant",
    page_icon="📑",
    layout="wide"
)
# Custom CSS for Chat Bubbles

st.markdown("""
<style>
.user-bubble {
    background-color: #d4f8c4;  /* Light green */
    color: black;
    padding: 12px;
    border-radius: 12px;
    margin: 5px 0;
    max-width: 80%;
    align-self: flex-end;
    box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
}
.assistant-bubble {
    background-color: #2e2e2e;  /* Dark gray for dark mode */
    color: white;               /* White text for readability */
    padding: 12px;
    border-radius: 12px;
    margin: 5px 0;
    max-width: 80%;
    align-self: flex-start;
    box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# Sidebar

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.markdown("## 📑 ScholarBot")
    st.markdown("Your AI-powered research companion.")
    st.divider()
    st.markdown("### ⚙️ Settings")
    st.checkbox("Enable detailed responses", value=True)
    st.checkbox("Save chat history", value=True)
    st.divider()
    st.caption("🚀 Powered by LangGraph + Streamlit")

# Header
st.title("📑 ScholarBot")
st.markdown("<p style='font-size:18px; color:gray;'>Explore ideas, gain insights, and generate research papers (for learning purposes).</p>", unsafe_allow_html=True)

# Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    logger.info("Initialized chat history")

# Display Past Chat
chat_container = st.container()
with chat_container:
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(
                f"<div class='user-bubble'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(
                f"<div class='assistant-bubble'>{msg['content']}</div>", unsafe_allow_html=True)


# Chat Input
user_input = st.chat_input("🔍 What research topic would you like to explore?")

if user_input:
    # Save + Show user input
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input})
    st.markdown(
        f"<div class='user-bubble'>{user_input}</div>", unsafe_allow_html=True)

    # Build input for LangGraph
    chat_input = {"messages": [
        {"role": "system", "content": INITIAL_PROMPT}] + st.session_state.chat_history}
    logger.info("Starting agent processing...")

    # Stream LangGraph response
    full_response = ""
    with st.spinner("Thinking..."):
        for s in graph.stream(chat_input, config, stream_mode="values"):
            message = s["messages"][-1]

            # Log tool calls
            if getattr(message, "tool_calls", None):
                for tool_call in message.tool_calls:
                    logger.info(f"Tool call: {tool_call['name']}")

            # Show assistant output
            if isinstance(message, AIMessage) and message.content:
                text_content = message.content if isinstance(
                    message.content, str) else str(message.content)
                full_response += text_content + " "
                st.markdown(
                    f"<div class='assistant-bubble'>{full_response}</div>", unsafe_allow_html=True)

    # Save assistant response
    if full_response:
        st.session_state.chat_history.append(
            {"role": "assistant", "content": full_response})
