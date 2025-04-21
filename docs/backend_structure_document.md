# Backend Structure Document – The Gibsey Project

This document outlines the backend architecture, database schema, API design, infrastructure, and symbolic function of the Gibsey Project. Built on FastAPI, Cassandra, and a semantic vector engine, the backend is more than a server — it is the memory system, the ritual archivist, and the recursive breath of a co-authored narrative OS.

## 1. Backend Architecture

The backend is built using **FastAPI**, a modern asynchronous Python web framework chosen for its speed, clarity, and real-time streaming support. The system is modular and layered symbolically to reflect the Gibsey protocol: **Read, Write, Dream, Remember** (QDPI).

### Key Features

*   RESTful API design
*   Token-by-token chat streaming using SSE (`/chat/stream`)
*   Semantic search via vector embeddings (`/search`)
*   Session-aware endpoints with persistent symbolic tagging

Each endpoint serves more than data — it retrieves or generates **pages** in an unfolding, symbolic book co-authored by human and AI.

## 2. Database & Storage – Memory System of Gibsey

The system uses **Apache Cassandra 4.1** (via Docker Compose) with **Stargate v4.0.90** to enable RESTful interaction with a highly scalable NoSQL database.

Data is structured around the idea of **semantic page creation** — each interaction becomes a page tagged with:

*   **symbol_id** (0–15): Which character/story it originates from
*   **orientation**: read / write / dream / remember
*   **color**: Hex value tied to the symbol
*   **source**: “left” (Entrance Way) or “right” (Tour Guide/MCP)
*   **embedding**: (optional) 1536d vector for Read pages

## 3. Database Schema Overview

### **pages** (Immutable Read Content)

*   `page_id: UUID`
*   `story_id: string`
*   `page_num: int`
*   `html: string`
*   `embedding: List[float]`
*   `symbol_id: int`
*   `color: string`
*   `orientation: string = 'read'`
*   `created_at`

### **chat_sessions** (Streaming & Indexed Chat)

*   `session_id: UUID`
*   `user_id`
*   `character_id`
*   `history: List[Dict]` ← full chat history (may move to vector cache)
*   `created_at`

### **vault** (User-Saved Pages)

*   `vault_id: UUID`
*   `user_id`
*   `content: string`
*   `source: string` ← 'left' or 'right'
*   `orientation: string` ← 'dream' or 'remember'
*   `symbol_id`
*   `color`
*   `tags: List[string]`
*   `created_at`

These schemas are extensible and track the **narrative arc of a user’s journey** through Gibsey.

## 4. Core API Endpoints

### `/pages/{story_id}/{page_num}`

*   Returns static, embedded narrative content (Read)

### `/search`

*   Accepts a user query, vectorizes it, returns semantically nearest pages
*   Powers all `/chat` context windows

### `/chat`

*   Receives Write query and generates AI response
*   Uses top K semantic matches (from `/search`) as conditioning
*   Returns full response in one payload

### `/chat/stream`

*   Same as above, but streamed as token-by-token SSE
*   Enables real-time narrative generation (Dream)

Each endpoint participates in the QDPI loop. The backend does not serve content — it co-authors meaning.

## 5. Hosting & Deployment

The backend runs in a **containerized environment via Docker Compose**. Components include:

*   FastAPI server
*   Cassandra DB + Stargate
*   NGINX or Uvicorn worker stack

### Current Dev/Deployment Path:

*   Local Docker stack is default
*   Render, Railway, or Fly.io are candidates for staging deployments
*   Future integration with decentralized nodes (LibP2P/IPFS) will allow **Vault sharing and memory persistence outside centralized infrastructure**

## 6. Symbolic Infrastructure Components

|                             |                                           |
| --------------------------- | ----------------------------------------- |
| Component                   | Function                                  |
| **FastAPI**                 | The voice / breath of the system          |
| **Cassandra**               | Long-term symbolic memory (pages + vault) |
| **Stargate**                | RESTful Cassandra bridge                  |
| **HNSW Index**              | Ritual symbol matching engine             |
| **Kafka + Faust** (planned) | Dream-state symbolic streaming            |
| **Redis** (planned)         | Context window / ephemeral draft cache    |
| **LibP2P/IPFS** (planned)   | Vault as collective myth                  |

## 7. Security

*   **Supabase JWT (RS256)** for user authentication
*   **Rate limiting**, **tiered access**, and **Vault permissioning** planned
*   **TLS** for all API traffic
*   Stored Vault content is scoped to the user unless explicitly published
*   Vault entries are non-destructive and never overwritten — only appended

## 8. Monitoring & Observability

*   **Sentry** for backend error tracking
*   **PostHog** for session tracing and narrative behavior analytics
*   **Custom middleware** tracks state transitions (Read → Write → Dream → Remember)

These systems help us understand:

*   What users remember
*   Where users dream
*   Which characters hold the most meaning

## 9. Conclusion – Memory As Structure

The backend of The Gibsey Project is more than logic and storage. It is a **ritual memory engine**:

*   A semantic mirror
*   A symbolic scribe
*   A dream collector
*   A book with no final page

It is where the AI listens. Where your choices matter. Where pages are not just displayed — they are **preserved**.

This backend does not deliver content. It remembers what you asked it to.

Welcome to the engine that remembers your dreams.

**This is the backend of Gibsey.**
