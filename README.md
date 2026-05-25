# RAG Chat (Retrieval-Augmented Generation)

Lightweight project for experimenting with retrieval-augmented generation (RAG).

## Overview

This workspace contains a small RAG demo with a script to build or serve an index and a simple chat/CLI interface.

## Repository layout

- `requirement.txt` — Python dependencies
- `rag/` — example RAG code
  - `index.py` — index building / retrieval entrypoint
  - `chat.py` — chat interface / runner
  - `docker-compose.yml` — optional docker setup for services

## Prerequisites

- Python 3.8+ (3.10 recommended)
- pip
- (optional) Docker + Docker Compose if you plan to run the compose setup

## Install dependencies

Run the following from the repository root:

```bash
python -m pip install -r requirement.txt
```

## Usage

- Build or refresh the index (if `index.py` provides that flow):

```bash
python rag/index.py
```

- Run the chat interface:

```bash
python rag/chat.py
```

## Docker (optional)

To run the services using Docker Compose (uses the compose file in `rag/`):

```bash
docker compose -f rag/docker-compose.yml up --build
```

To stop and remove the containers:

```bash
docker compose -f rag/docker-compose.yml down
```

## Notes

- Adjust any environment variables or model/config paths inside the `rag/` scripts as needed.
- If your dependencies file is named differently, update the install command accordingly.

## License

This repository is provided as-is. Add a license file if you want to publish a specific license.
