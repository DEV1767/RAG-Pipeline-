from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
import os

# Load environment variables
load_dotenv()

# Global variables for lazy initialization
_embedding_model = None
_vector_db = None
_client = None


def _get_embedding_model():
    """Lazily initialize and return the embedding model."""
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001"
        )
    return _embedding_model


def _get_vector_db():
    """Lazily initialize and return the vector database."""
    global _vector_db
    if _vector_db is None:
        embedding_model = _get_embedding_model()
        _vector_db = QdrantVectorStore.from_existing_collection(
            url="http://localhost:6333",
            collection_name="bio_notes",
            embedding=embedding_model
        )
    return _vector_db


def _get_client():
    """Lazily initialize and return the Gemini client."""
    global _client
    if _client is None:
        _client = OpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
    return _client


def process_query(query: str):
    print("Searching Chunks:", query)

    # Get the vector database instance
    vector_db = _get_vector_db()

    # Search relevant chunks
    search_result = vector_db.similarity_search(query=query)

    # Create context from retrieved documents
    context = "\n\n".join([
        f"""
Page Content: {result.page_content}
Page Number: {result.metadata.get('page_label', 'Unknown')}
File Location: {result.metadata.get('source', 'Unknown')}
"""
        for result in search_result
    ])

    # System Prompt
    SYSTEM_PROMPT = f"""
You are a helpful AI assistant.

Answer the user's query only based on the available context retrieved from a PDF file.

Rules:
1. Use only the provided context.
2. Mention the page number so the user can navigate to the correct page.
3. If the answer is not found in the context, say:
   "I could not find relevant information in the provided PDF."
4. Clearly separate AI-generated explanation from retrieved content.

Context:
{context}
"""

    # Get the client instance
    client = _get_client()

    # Generate response
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": query
            }
        ]
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content


