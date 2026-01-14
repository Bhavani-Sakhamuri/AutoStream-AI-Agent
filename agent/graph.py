from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.intent import classify_intent
from agent.rag import rag_answer
from agent.lead_tool import mock_lead_capture
import re


# ---------- ROUTER ----------
def router(state):
    last_user_msg = state["messages"][-1].content.lower()

    # Sticky lead mode
    if state.get("lead_mode"):
        state["next"] = "lead"
        return state

    # Purchase trigger
    BUY_WORDS = ["buy", "purchase", "subscribe", "sign up", "get started"]
    if any(word in last_user_msg for word in BUY_WORDS):
        state["lead_mode"] = True
        state["lead_step"] = None
        state["next"] = "lead"
        return state

    # Default → intent classification
    state["next"] = "intent"
    return state



# ---------- GREETING ----------
def greeting_node(state):
    state["messages"].append(
        AIMessage(content="Hi 👋 How can I help you today?")
    )
    return state


# ---------- LEAD FLOW ----------
def lead_qualification(state):
    user_input = state["messages"][-1].content.strip()

    if state.get("lead_step") is None:
        state["lead_step"] = "ask_name"
        state["messages"].append(AIMessage(content="May I have your name?"))
        return state

    if state["lead_step"] == "ask_name":
        state["name"] = user_input
        state["lead_step"] = "ask_email"
        state["messages"].append(AIMessage(content="Please share your email address."))
        return state

    if state["lead_step"] == "ask_email":
        if not re.match(r"[^@]+@[^@]+\.[^@]+", user_input):
            state["messages"].append(AIMessage(content="Please enter a valid email address."))
            return state

        state["email"] = user_input
        state["lead_step"] = "ask_platform"
        state["messages"].append(
            AIMessage(content="Which creator platform do you use? (YouTube, Instagram, etc.)")
        )
        return state

    if state["lead_step"] == "ask_platform":
        state["platform"] = user_input
        mock_lead_capture(state["name"], state["email"], state["platform"])
        state["messages"].append(
            AIMessage(content="Thanks! Our team will contact you shortly 🚀")
        )

        # reset
        state["lead_mode"] = False
        state["lead_step"] = None
        return state


# ---------- INTENT ROUTING ----------
def route_from_intent(state):
    intent = state.get("intent")

    if intent == "greeting":
        return "greeting"

    if intent in ["product_inquiry", "high_intent"]:
        return "rag"

    return END


# ---------- BUILD GRAPH ----------
def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("router", router)
    graph.add_node("intent", classify_intent)
    graph.add_node("greeting", greeting_node)
    graph.add_node("rag", rag_answer)
    graph.add_node("lead", lead_qualification)

    # 🔑 ENTRY POINT
    graph.set_entry_point("router")

    graph.add_conditional_edges("router", lambda s: s["next"], {
        "intent": "intent",
        "lead": "lead"
    })

    graph.add_conditional_edges("intent", route_from_intent)

    graph.add_edge("greeting", END)
    graph.add_edge("rag", END)
    graph.add_edge("lead", END)

    return graph.compile()
