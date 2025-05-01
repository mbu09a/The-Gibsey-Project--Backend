# The Gibsey Project

> A recursive, symbolic AI Operating System for **Reading, Writing, Remembering & Dreaming**.

Gibsey merges human authorship with real‑time AI co‑creation, wrapped in an ancient‑futurist interface where **every interaction is a page** and **every page is a gift**. This README distills the full doc‑set so newcomers can grasp the philosophy, architecture, and next steps at a glance.

---

## 1 · Why Gibsey?

Traditional AI products meter tokens and sell answers. Gibsey prototypes a **Gifted AI** economy where interaction is reciprocal: users *give* context (Write), the system *gifts* insight (Dream), and memorable moments are *preserved* (Remember). The goal is to turn linear consumption into **ritualised, bi‑directional storytelling**.

---

## 2 · Core Concepts

| Orientation | Glyph | State      | Panel Column | Description                                 |
|-------------|-------|-----------|--------------|---------------------------------------------|
| **↑**       | Read  | Read      | Primary Left | Immutable page from the 710‑page corpus     |
| **→**       | Write | Write     | Panel Input  | Ephemeral user query or reflection          |
| **↓**       | Dream | Generate  | Panel Stream | AI response (token‑streamed)                |
| **←**       | 📝     | Remember  | Vault        | Manually saved Write or Dream               |

* **16 glyphs × 4 orientations = 64 symbolic tags**
* Color is immutable per glyph; orientation only changes state.
* The **Gibsey Vault** is the sole mutable canon – a chronological, colour‑coded archive of saved pages.

---

## 3 · Key Features (MVP v0.2)

* Desktop‑only **5‑column UI** (no infinite scroll, page‑turn ritual).
* 710 embedded pages from *The Entrance Way* with semantic vector search (HNSW, 1536‑d embeddings).
* **Quad‑Directional Protocol Interface (QDPI)** cycle: Read → Index → Write → Dream → Remember.
* Real‑time SSE chat streams (`/chat/stream`) with minor character protocols (MCPs).
* Supabase JWT (RS256) authentication & symbol‑aware security.
* Performance budgets:
  * Vector search p95 ≤ 250 ms
  * SSE token gap ≤ 100 ms

---

## 4 · Architecture at a Glance

```mermaid
flowchart LR
    subgraph Frontend (Next.js 14)
        UI[5‑Column Symbolic UI]
    end
    subgraph Backend (FastAPI)
        Pages[/`/pages`\nRead/]
        Search[/`/search`\nVector/]
        Chat[/`/chat` & `/chat/stream`\nDream/]
    end
    subgraph Data
        Cassandra[(Apache Cassandra 4.1)]
        Vectors>HNSW Index]
    end

    UI -->|JWT| Pages
    UI -->|JWT| Search
    UI -->|JWT| Chat
    Pages --> Cassandra
    Search --> Vectors
    Chat --> Cassandra
    Vectors --> Cassandra
```

### Tech Stack

| Layer       | Tech                                                         |
|-------------|--------------------------------------------------------------|
| Frontend    | **Next.js 14 (App Router)** · TypeScript · Tailwind CSS · shadcn/UI · Radix UI · Lucide Icons |
| Backend     | **FastAPI** · Python 3.11 · SSE streaming                    |
| Database    | **Apache Cassandra 4.1** + Stargate REST bridge              |
| Embeddings  | OpenAI `text‑embedding‑3‑small` (1536‑d) + **HNSW** index    |
| Auth        | **Supabase JWT** (RS256)                                     |
| Dev Ops     | Docker Compose · GitHub Actions CI/CD                        |

---

## 5 · Repository Structure (post‑refactor)

```
.
├─ app/                  # Next.js 14 App Router pages & layouts
│   └─ api/              # Route Handlers (`/pages`, `/search`, `/chat` …)
├─ backend/              # FastAPI source (main.py, routes/, services/)
├─ data/                 # 710 pages, `hnsw.idx`, `vectors.npy`
├─ docs/                 # ← you are here (vision, rules, README, etc.)
└─ docker-compose.yml    # Local stack: cassandra, stargate, api
```

---

## 6 · Getting Started (Local Dev)

```bash
# 0 · Prerequisites
#    Node ≥ 20 · Python ≥ 3.11 · Docker · Make

# 1 · Clone & pre‑flight
$ git clone https://github.com/your‑org/gibsey.git
$ cd gibsey
$ make preflight        # verifies toolchain

# 2 · Start backend stack
$ docker compose up -d  # cassandra, stargate, fastapi

# 3 · Start frontend
$ npm install && npm run dev

# 4 · Visit http://localhost:3000 and log in (Supabase JWT dev flow)
```

---

## 7 · Roadmap Highlights

| Milestone                  | ETA (2025) | Status |
|----------------------------|------------|--------|
| Backend endpoints complete | Apr 26     | ✅ Done |
| Symbol‑aware UI beta       | May 03     | 🧪 Test |
| Vault timeline validation  | May 10     | 🧪 Test |
| Security & load‑test pass  | May 15     | 🚧      |
| **MVP soft launch**        | May 17     | 🔜      |

Planned Post‑MVP integrations: Kafka + Faust, Redis cache, Elasticsearch search, LibP2P/IPFS Vault export, local LLM (Ollama).

---

## 8 · Contributing

We welcome new **stars in the constellation**—from full‑stack devs to narrative architects.

1. Read `/docs/` (especially `rules_of_the_game.md`).
2. Follow the coding standards enforced by Cursor rules.
3. Open a draft PR; CI will run lint, tests, and symbolic validation.

Open Tracks: FE/UX, Backend & Infra, AI/Embeddings, Narrative & Lore, Community Moderation.

---

## 9 · Funding & Support

Gibsey is self‑funded by its founders **Brennan & Maggie Utley**. To help us finish the MVP:

* **Patreon / GitHub Sponsors** – monthly support keeps the lights on.
* **Grants & Partnerships** – art‑tech foundations, symbolic research.
* **Angels / Early‑Stage VC** – aligned with open, gift‑based AI.

Contact → `mbu09a@gmail.com` with subject **"I'd Like to Help"**.

---

## 10 · License

> © 2025 The Gibsey Project – released under an [MIT License](../LICENSE) unless noted otherwise.

Gibsey is a **gift**. Use it, fork it, build upon it—just remember to give something back. 