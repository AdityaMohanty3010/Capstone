# AI Customer Support — Capstone

An explainable RAG (Retrieval-Augmented Generation) system for customer support built with FastAPI (backend) and Streamlit (frontend). It answers customer questions by retrieving relevant snippets from a PDF-based knowledge base and generating concise responses using a large language model.

## Stack
- Language: Python 3.11
- Framework / runtime: FastAPI (backend), Streamlit (frontend)
- Notable libraries: sentence-transformers, pinecone, google-genai, pypdf

## What this repo contains
Top-level layout:

```
backend/                 FastAPI backend, ingestion, retrieval, generation, and tests
  DockerFile
  requirements.txt
  app/
    main.py               FastAPI app entrypoint
    rag.py                RAG pipeline wiring (retriever + LLM)
    retrieval/            retrieval components (Retriever, loaders)
    generation/           LLM integration (LLMService)
    ingestion/            ingestion utilities for building the vector DB
frontend/                Streamlit UI
  Dockerfile
  requirements.txt
  streamlit_app.py       Streamlit frontend that calls POST /api/chat
knowledge_base/          PDF knowledge base used for retrieval
  01_*.pdf ... 08_*.pdf
docker-compose.yml       Compose file to run backend + frontend for development
Readme.md                (this file)
.env.example             example env file (backend env vars)

```

How it fits together: the frontend collects a user's question and calls the backend's /api/chat endpoint. The backend's RAG pipeline (app/rag.py) uses Retriever to fetch the most relevant chunks from the vector store, then passes a prompt containing those chunks to the LLMService which produces the final answer.

## Quick start — run with Docker Compose (recommended)

1. Copy environment variables for backend: create `backend/.env` from `.env.example` and set required keys (see Environment variables below).
2. From repository root, build and start services:

```bash
docker-compose up --build
```

- Backend will be available at: http://localhost:8000
- Frontend (Streamlit UI) will be available at: http://localhost:8501

## Run locally without Docker

Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Frontend
```bash
cd frontend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py --server.address=0.0.0.0 --server.port=8501
```

## API

POST /api/chat
- Request JSON: { "question": "...", "top_k": 3 }
- Response JSON: { "answer": "..." }

Example using curl (when backend is running locally):

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"How do I reset my password?","top_k":3}'
```

## Environment variables
The project uses external services (vector DB, LLM). Typical env vars to configure (set these in `backend/.env`):

- PINECONE_API_KEY — Pinecone API key
- PINECONE_ENV — Pinecone environment/region
- PINECONE_INDEX — (optional) index name
- GOOGLE_API_KEY or other LLM provider keys — for google-genai or configured LLM
- Other keys used by ingestion/retrieval depending on vectorstore choice

Check `backend/.env.example` for a starting template.

## Knowledge base
The `knowledge_base/` folder contains PDF documents (01_.. to 08_..) that are used by the ingestion pipeline to produce embeddings and populate the vector store. To update the KB, add PDFs to the folder and run the ingestion scripts (look in `backend/app/ingestion/` for loaders and utilities).

## Tests
Several test scripts exist under `backend/` (e.g., `test_embedding.py`, `test_rag.py`, `test_pinecone.py`). Run them with pytest from the `backend/` directory after installing dev/test dependencies:

```bash
cd backend
pip install -r requirements.txt
# If you have pytest installed
pytest -q
```

## Development notes
- The RAG pipeline is implemented in `backend/app/rag.py` and composes `Retriever` (retrieval/relevance) and `LLMService` (generation). Inspect those modules to tune prompting, chunking, or retrieval strategies.
- The Streamlit app expects the backend API at `/api/chat` (containerized compose sets BACKEND_URL for the frontend to `http://backend:8000`).

## Common troubleshooting
- "Unable to connect to the backend" in the frontend indicates the backend server is not reachable from the frontend container or the backend process is not running; check `docker-compose logs` or `uvicorn` output.
- If embeddings/retrieval fail, ensure Pinecone (or the configured vectorstore) credentials are correct.

## Contributing
Contributions, bug reports, and PRs are welcome. Create an issue describing the change, branch from `main`, and open a PR with a clear description and tests where applicable.

## License
No license specified. Add a LICENSE file to make the terms explicit.

## Contact
Repository owner: @AdityaMohanty3010

