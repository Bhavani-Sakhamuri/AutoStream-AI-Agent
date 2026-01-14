import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from agent.graph import build_graph

st.set_page_config(page_title="AutoStream AI Agent", page_icon="🤖")

st.title("🤖 AutoStream AI Agent")

# Build graph ONCE
if "app" not in st.session_state:
    st.session_state.app = build_graph()

# Initialize agent state
if "state" not in st.session_state:
    st.session_state.state = {
        "messages": [],
        "intent": None,
        "lead_mode": False,
        "lead_step": None,
        "name": None,
        "email": None,
        "platform": None,
    }

# Display chat history
for msg in st.session_state.state["messages"]:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    elif isinstance(msg, AIMessage):
        st.chat_message("assistant").write(msg.content)

# Input box
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    st.chat_message("user").write(user_input)

    # Update state
    st.session_state.state["messages"].append(
        HumanMessage(content=user_input)
    )

    # Run agent
    st.session_state.state = st.session_state.app.invoke(
        st.session_state.state
    )

    # Show latest assistant message
    last_msg = st.session_state.state["messages"][-1]
    if isinstance(last_msg, AIMessage):
        st.chat_message("assistant").write(last_msg.content)
