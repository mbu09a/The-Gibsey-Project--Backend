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

## 🚀 6 · Getting Started (Local Dev)

```bash
# Prerequisites: Node ≥ 20 · Python ≥ 3.11 · Docker · Make (Linux/macOS)

# 0. Seed corpus & ANN index (one‑time ~8‑10 min)
$ make seed

# Windows PowerShell (no make):
> python -m scripts.seed --force

# 1. Clone the repo
$ git clone https://github.com/your-org/gibsey.git

# 2. build & run core services
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

Copy `.env.example` → `.env` and fill in all values:

```dotenv
OPENAI_API_KEY=sk-____________________

# Supabase
SUPABASE_PROJECT=your-supabase-project-ref
SUPABASE_JWKS_URL=https://your-supabase-project.supabase.co/auth/v1/keys

# Dev HS256 secret & environment
DEV_JWT_SECRET=dev-only-secret
ENV=dev
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

## 📈 Performance

We've benchmarked the `/search` endpoint for 100 random queries (p95 ≤ 250 ms target):

| Metric    | Value  |
|-----------|--------|
| runs      | 100    |
| mean_ms   | 45.3   |
| p50_ms    | 38.2   |
| p90_ms    | 75.7   |
| **p95_ms**| **110.4** ≤ 250 ms target |
| max_ms    | 180.1  |

You can tweak HNSW search parameters via query:
```
GET /search?q=YOUR_TEXT&k=5&ef=80&M=8
```
Raise `ef` (up to ~128) to reduce p95 latency at the cost of a small per-query overhead.  

---