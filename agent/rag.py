from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from agent.config import GROQ_API_KEY


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=GROQ_API_KEY
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def load_vectorstore():
    loader = TextLoader("data/knowledge_base.md")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(docs)

    return FAISS.from_documents(chunks, embeddings)


VECTORSTORE = load_vectorstore()


def rag_answer(state):
    query = state["messages"][-1].content
    docs = VECTORSTORE.similarity_search(query, k=3)

    context = "\n".join(d.page_content for d in docs)

    prompt = f"""
Answer the question clearly using ONLY the context below.

Context:
{context}

Question:
{query}
"""

    answer = llm.invoke(prompt)

    return {
        "messages": state["messages"] + [answer]
    }
