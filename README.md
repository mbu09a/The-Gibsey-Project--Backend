# The Gibsey Project
# README.md  (The Gibsey Project)

> \*\*Status \*\*: Feature-complete MVP – Backend ready for deployment with vector search and caching.

---

## ✨ Vision

Gibsey is an interactive, non‑linear storytelling OS that fuses **primary text pages**, **AI‑generated "dream/remember" annotations**, and **character chatbots** into a living novel.  The prototype proves:

1. **16‑color symbolic UX** tied to story sections & MCP bots.
2. **Quad‑directional QDPI loop** – Read ↑, Ask →, Receive ↓, Remember ←.
3. A Cassandra 5 vector store + Redis caching layer serving page‑level embeddings.
4. A FastAPI layer for `/page`, `/search`, `/chat`, `/vault` routes with rate limiting.
5. A Next.js front‑end driven by Maggie's Figma‑to‑Tailwind hand‑off.

## 📁 Repo layout

```
backend/
  │ Dockerfile            # FastAPI container
  ├─ app/                 # Python source
  │   ├─ main.py          # API entrypoint
  │   ├─ embed_load.py    # text→vector loader
  │   └─ requirements.txt
  ├─ seed/                # CQL schema & static data
  │   └─ schema.cql
  └─ docker-compose.yml   # Cassandra + Stargate + API
frontend/                 # (placeholder) Next.js app
infra/                    # IaC / GitHub Actions, coming soon
.data/
  └─ cleaned_normalised.txt   # 710‑page master text
.codex/                   # OpenAI Codex CLI config
```

## 🚀 Quick start (local dev)

```bash
# 1. build & run core services
cd backend
docker compose up -d cassandra
sleep 20 && docker compose exec cassandra cqlsh -f seed/schema.cql
docker compose up -d          # brings up stargate + api

# 2. load the pages (one‑off)
cd app && python embed_load.py --story an_author_preface

# 3. test API
curl "http://localhost:8000/page?story_id=an_author_preface&page_num=1"

# 4. search the text
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "what is Gibsey?", "k": 5}'

# 5. chat with the text
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "what is Gibsey?", "k": 5}'
```

## 🤖 Using Codex CLI

1. `npm install -g @openai/codex`
2. `codex init` → creates `.codex/`
3. `codex chat` and ask e.g. "Generate docker‑compose.yml with Cassandra & Stargate."
4. Review diff → `approve` (auto‑commits).

## 🛡 Environment variables

Copy `.env.example` → `.env` and fill in:

```
OPENAI_API_KEY=sk-____________________
```
## 🚀 Deploying to Fly.io

This repo includes **`fly.toml`** and a GitHub Actions workflow that builds & deploys the container on Fly.io.
Deployment runs when:
* you push/merge to **`main`**, OR
* your commit message contains **`[deploy]`** (for manual/staging deployments).

```bash
# one-time setup
fly launch --copy-config --no-deploy    # creates the app & fly.toml

# set production secrets
fly secrets set \
  OPENAI_API_KEY=... \
  SUPABASE_PROJECT=... \
  JWT_SECRET=...

# manual deploy (CI covers main)
fly deploy
```

> **Tip**: to disable caching during deploy, set `CACHE_TTL=0` or omit `REDIS_HOST`.

## 👷 Contributing

- PRs welcome; open an issue first to discuss major changes.
- Commit style: `type(scope): message` (conventional commits).

## 📡 API Endpoints

- `GET /page` - Retrieve a specific page by `story_id` and `page_num`
- `POST /search` - Semantic search across pages using vector embeddings
  - Body: `{"query": "your search query", "k": 5}` (k = number of results)
  - Returns: Array of pages with similarity scores
- `POST /chat` - Ask questions about the text
  - Body: `{"query": "your question", "k": 5}` (k = context size)
  - Returns: AI-generated answer based on relevant pages

---