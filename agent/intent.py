from langchain_groq import ChatGroq
from agent.config import GROQ_API_KEY

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=GROQ_API_KEY
)

def classify_intent(state):
    # 🚨 Skip intent if already in lead flow
    if state.get("lead_mode"):
        return state

    user_msg = state["messages"][-1].content.lower()

    prompt = f"""
You are an intent classifier.

Classify the user intent into ONE of the following:
- greeting
- product_inquiry
- high_intent

User message: "{user_msg}"

Return ONLY the intent.
"""

    intent = llm.invoke(prompt).content.strip().lower()
    state["intent"] = intent

    return state



