from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
import os
# Load environment variables
load_dotenv()


# Create embedding model
embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)

# Connect to existing Qdrant collection
vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="bio_notes",
    embedding=embedding_model
)

# User query
user_query = input("Ask something: ")

# Similarity search
search_result = vector_db.similarity_search(
    query=user_query,
    k=3
)

# Create context from retrieved documents
context = "\n\n".join([
    f"""Page Content: {result.page_content}
Page Number: {result.metadata.get('page_label', 'Unknown')}
File Location: {result.metadata.get('source', 'Unknown')}"""
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


client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {
                "role": "system",
                "content":SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_query
            }
        ]
    )

print(response.choices[0].message.content)