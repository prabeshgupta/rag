# Local PDF RAG Assistant

A lightweight local Retrieval-Augmented Generation (RAG) application for chatting with uploaded PDF documents. The project combines a FastAPI backend, a Streamlit frontend, Qdrant for vector storage, and Ollama for embeddings and generation.

It is designed to run fully on your machine, allowing you to upload PDFs, index them locally, and ask questions about their contents without sending data to a remote service.

## Overview

This project lets you:

- upload PDF files from a browser interface
- split documents into chunks for better retrieval
- generate vector embeddings locally with Ollama
- store and query those embeddings in Qdrant
- retrieve relevant passages using hybrid search
- ask questions and receive grounded answers with source excerpts

## Features

- PDF upload from the Streamlit UI
- Local document ingestion and chunking
- Ollama-powered embeddings
- Vector search with Qdrant
- Hybrid retrieval using both semantic and keyword signals
- Session-based chat history
- Source-grounded answers for transparency
- Document listing and deletion in the UI

## Architecture

The app is split into a backend service and a frontend interface:

- `backend/` contains the API, ingestion pipeline, retriever, memory logic, and database access
- `frontend/` contains the Streamlit chat application
- `uploads/` stores uploaded PDFs before indexing

### Request flow

1. A user uploads a PDF through the frontend.
2. The FastAPI backend saves the file and runs the ingestion pipeline.
3. The document is chunked and embedded locally with Ollama.
4. Embeddings are stored in Qdrant.
5. A question is sent to the backend.
6. The retriever finds the most relevant chunks.
7. The LLM uses those chunks and the session history to answer the question.
8. The frontend displays the response and associated source passages.

## Tech Stack

- Python
- FastAPI
- Streamlit
- Qdrant
- Ollama
- Docling
- Rank-BM25

## Project Structure

```text
RAG/
├── backend/
│   ├── api/
│   │   ├── chat.py
│   │   ├── document.py
│   │   └── upload.py
│   ├── db/
│   │   └── qdrant.py
│   ├── ingestion/
│   │   ├── chunker.py
│   │   ├── embedder.py
│   │   └── pipeline.py
│   ├── llm/
│   │   └── chat.py
│   ├── memory/
│   │   └── history.py
│   ├── rag/
│   │   └── pipeline.py
│   ├── retrieval/
│   │   ├── hybrid_search.py
│   │   ├── keyword_search.py
│   │   ├── rerank.py
│   │   ├── retriever.py
│   │   └── vector_search.py
│   ├── main.py
│   ├── uploads/
│   └── venv/
├── frontend/
│   └── app.py
├── .gitignore
├── README.md
├── uploads/
└── .git/
```

## Prerequisites

Before running the project, make sure you have:

- Python 3.10+
- Ollama installed and running locally
- Qdrant running locally or via Docker
- Internet access to install dependencies and pull the required Ollama models

## Required Ollama Models

This project uses the following models:

- Embedding model: `nomic-embed-text`
- Chat model: `qwen2.5:0.5b`

Pull them with:

```bash
ollama pull nomic-embed-text
ollama pull qwen2.5:0.5b
```

## Start Qdrant

The backend expects Qdrant to be available at `localhost:6333`.

Using Docker:

```bash
docker run -d --name qdrant -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

## Install Dependencies

Create and activate a virtual environment if needed, then install the Python packages:

```bash
pip install fastapi uvicorn streamlit requests qdrant-client docling rank-bm25 ollama
```

## Quick Start

### 1) Start the backend

From the `backend` directory:

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:

- `http://127.0.0.1:8000`

### 2) Start the frontend

From the project root:

```bash
streamlit run frontend/app.py
```

The UI will open in your browser and connect to the backend at `http://127.0.0.1:8000`.

### 3) Upload a PDF and ask a question

- Open the Streamlit app
- Upload a PDF from the sidebar
- Wait for indexing to complete
- Ask a question in the chat box

## API Endpoints

### Root

```http
GET /
```

Returns a simple status response.

### Upload a PDF

```http
POST /upload/
```

Uploads a PDF, saves it locally, and indexes it for retrieval.

### Chat with indexed documents

```http
POST /chat/
```

Example request body:

```json
{
  "question": "What does this document say about the main findings?",
  "session_id": "user-session-id"
}
```

Example response:

```json
{
  "answer": "The document highlights ...",
  "sources": [
    { "text": "..." }
  ]
}
```

### List documents

```http
GET /documents/
```

Returns metadata about uploaded documents and their chunk counts.

### Delete a document

```http
DELETE /documents/{document_id}
```

Removes the document and its indexed chunks from Qdrant.

## Retrieval Pipeline

The project uses a hybrid retrieval strategy:

- `vector_search.py` embeds the user query and performs semantic similarity search in Qdrant
- `keyword_search.py` uses BM25 to rank chunks by keyword relevance
- `hybrid_search.py` merges the results and removes duplicates
- `rerank.py` reorders the combined results to prioritize the best matches

This approach improves answer quality compared with a single retrieval method.

## Chat Workflow

The main flow is handled in `backend/rag/pipeline.py`:

- fetch the most relevant chunks for the query
- convert them into a context string
- load the current session history
- send the question, context, and history to the Ollama chat model
- store the user and assistant messages in memory
- return the final answer and source excerpts to the frontend

## Session Memory

Chat history is stored in memory at:

- `backend/memory/history.py`

This means session history persists while the backend is running, but it resets when the server restarts.

## Notes and Limitations

- This is a local demo/prototype, not a production-ready system
- Chat memory is not persisted to disk
- The app depends on local Ollama and Qdrant services
- Uploaded PDFs are stored in the local `uploads/` folder
- Model downloads require internet access

## Troubleshooting

### Qdrant connection errors

Make sure Qdrant is running and accessible at `localhost:6333`.

### Ollama model not found

Pull the required models again:

```bash
ollama pull nomic-embed-text
ollama pull qwen2.5:0.5b
```

### Frontend cannot reach backend

Check that the backend is running on port `8000` and that the frontend is configured to call the correct URL.

### Upload fails

Verify that the uploaded file is a valid PDF and that the backend has write access to the local upload folder.

## Possible Improvements

- add persistent chat history storage
- support multi-user sessions
- add authentication and access control
- improve chunking and reranking quality
- add configuration files for models and endpoints
- move ingestion to a background worker or queue

## License

This project is provided as a local research/demo application. Add your preferred license text before distributing it publicly.

## Contributing

Contributions are welcome for improvements in:

- retrieval quality
- ingestion robustness
- UX and design
- memory persistence
- deployment and configuration
