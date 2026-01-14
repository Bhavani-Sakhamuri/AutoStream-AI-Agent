# AutoStream AI Agent 🤖

An AI-powered conversational agent that answers product-related questions using RAG (Retrieval-Augmented Generation) and captures qualified leads through a multi-step conversational flow.

---

## 1. How to Run the Project Locally

### Prerequisites

* Python 3.10+
* Git
* Virtual environment tool (venv / conda)
* Groq API Key

### Steps

```bash
# Clone the repository
git clone https://github.com/Bhavani-Sakhamuri/AutoStream-AI-Agent
cd autostream-agent

# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Run the Agent (CLI)

```bash
python main.py
```

(Optional) If Streamlit UI is enabled:

```bash
streamlit run app.py
```

---

## 2. Architecture Explanation (≈200 words)

### Why LangGraph

LangGraph was chosen because it provides **explicit, deterministic control over agent workflows**, which is critical for real-world applications like lead qualification. Unlike AutoGen or fully autonomous agents, LangGraph allows us to define **clear state transitions, routing logic, and safety boundaries**. This prevents unintended tool execution and makes the agent predictable and debuggable.

### High-Level Architecture

The system is composed of the following nodes:

* **Intent Classifier** – Determines whether the user intent is greeting, product inquiry, or high intent.
* **RAG Node** – Uses FAISS vector search with HuggingFace embeddings to answer questions grounded in a knowledge base.
* **Lead Qualification Node** – A multi-step stateful flow that collects name, email, and platform details.
* **Router Node** – Decides the next node based on intent and conversation state.

### State Management

State is centrally managed using `AgentState`, which stores:

* Conversation messages
* Intent
* Lead details (name, email, platform)
* Lead progress step

This persistent state enables **multi-turn conversations**, “sticky” lead capture mode, and prevents the agent from repeating or skipping steps.

---

## 3. WhatsApp Deployment (Webhook-Based Integration)

To deploy this agent on WhatsApp, I would integrate it using **WhatsApp Business Cloud API** with webhooks.

### High-Level Flow:

1. **Incoming Message**

   * WhatsApp sends user messages to a webhook endpoint (e.g., FastAPI `/webhook`).
2. **Webhook Handler**

   * The handler extracts the text message and user ID.
   * Conversation state is fetched from a database (Redis / DynamoDB).
3. **Agent Invocation**

   * The message is converted into a `HumanMessage` and passed to the LangGraph agent.
4. **Response Handling**

   * The agent’s latest AI response is sent back to the user via WhatsApp API.
5. **State Persistence**

   * Updated state is stored to ensure continuity across messages.

### Benefits

* Supports multi-turn conversations
* Scales horizontally
* Works with the same agent logic (no rewrite needed)
* Production-safe (no direct LLM tool execution)

---

## Summary

* ✅ Deterministic agent using LangGraph
* ✅ RAG-based knowledge grounding
* ✅ Stateful lead qualification
* ✅ Easily deployable to WhatsApp via webhooks

