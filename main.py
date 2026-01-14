from langchain_core.messages import HumanMessage, AIMessage
from agent.graph import build_graph

def main():
    app = build_graph()

    print("🤖 AutoStream AI Agent")
    print("Type 'exit' to quit\n")

    # Persistent state
    state = {
        "messages": [],
        "intent": None,
        "name": None,
        "email": None,
        "platform": None,
        "lead_mode": False,
        "lead_step": None
    }

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("Agent: Goodbye! 👋")
            break

        # Append user message
        state["messages"].append(HumanMessage(content=user_input))

        # Invoke LangGraph
        state = app.invoke(state)

        # Print only the last AIMessage
        for msg in reversed(state["messages"]):
            if isinstance(msg, AIMessage):
                print("Agent:", msg.content)
                break

if __name__ == "__main__":
    main()
