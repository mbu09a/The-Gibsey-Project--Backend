# Implementation Plan – Gibsey Project (Refactor‑First Approach)

**Goal:** Refactor the existing codebase so it aligns 1‑for‑1 with the final doc set (PRD, Frontend/Backend guidelines, Security rules) **without wiping functional work**.

## Phase 0  Repository Cleanup

|        |                                                                                            |                                       |
| ------ | ------------------------------------------------------------------------------------------ | ------------------------------------- |
|        |                                                                                            |                                       |
|        |                                                                                            |                                       |
|        |                                                                                            |                                       |
|        |                                                                                            |                                       |
|  Step  |  Action                                                                                    |  Validation                           |
| 0.1    | Run `scripts/cleanup.sh` → removes stale `/pages/`, unused Docker volumes, stray `.env.*`  | `git status` shows only expected dirs |
| 0.2    | Move **all** docs into `/docs/` (`security_guidelines.md`, `frontend_guidelines.md`, etc.) | Open `/docs/index.md` confirms links  |
| 0.3    | Add `/docs/symbolic_ui_rules.mdc`, `/docs/colors.json` (hex table)                         | Referenced by Cursor rules            |
| 0.4    | Commit — tag **v0.1‑refactor‑baseline**                                                    |                                       |

## Phase 1  Environment & Tooling

1.  **Pre‑flight Script** `make preflight`

    *   Checks Node ≥ 20 and Python ≥ 3.11.
    *   Fails fast with friendly hint if versions mismatch.

2.  **Cursor Context**

    *   Create `/cursor_metrics.md` (auto‑updated via hook).
    *   Create `.cursor/context.json` → points to `/docs/` for rules.

3.  **Supabase Secrets**

    *   Store connection string in `.env` → `SUPABASE_URL`, `SUPABASE_JWT_SECRET`.
    *   `context.json` references `process.env.SUPABASE_URL` (no plain text).

## Phase 2  Frontend Refactor

1.  **Confirm Next.js 14 App Router** (`app/` folder only). Remove leftover `pages/` dir.

2.  **Install / Upgrade** → Tailwind ^3, shadcn/ui, Radix UI, Lucide.

3.  `app/layout.tsx`

    *   Implements 5‑column grid via Tailwind CSS.
    *   Imports global CSS with strict CSP meta tags.

4.  **Components**

    *   `/src/components/SymbolIndex.tsx` pulls symbol + color from `/docs/colors.json`.
    *   `/src/components/SymbolicChat.tsx` handles left/right read/dream/remember/write.

5.  **Auth Pages** (`/app/auth/`)

    *   Sign‑in, Sign‑up with Supabase client SDK (PKCE ready).

6.  **Dev Validation** → `npm run dev` renders grid, auth flow, and hot‑reload.

## Phase 3  Backend Refactor

1.  **Python venv** (`make venv`) installs FastAPI + `python-dotenv`.
2.  **Project Layout**

`backend/ main.py routes/ pages.py search.py chat.py services/ vector_index.py auth.py scripts/ load_corpus.py`

1.  **Endpoints**

    *   `GET /pages/{story}/{page}` (Read)
    *   `GET /search?q=` + top‑K vector matches
    *   `POST /chat` (single response)
    *   `GET /chat/stream` (SSE)

2.  **Embedding & HNSW**

    *   `scripts/load_corpus.py` seeds Cassandra and builds `hnsw.idx` in `/data/`.
    *   Embeddings cached in table `pages`.

3.  **JWT Middleware** (`services/auth.py`) validates RS256 tokens, scopes coming soon.

4.  **Docker Compose** (`docker-compose.yml`)

    *   Services: `api`, `cassandra`, `stargate`, `nginx_ssl`.

5.  **Backend Tests** → pytest for routes, vector latency < 250 ms.

## Phase 4  Integration

1.  **Frontend API wrapper** `/src/services/api.ts` (axios) with token injection.
2.  **SSE Polyfill** → `event-source-polyfill` for legacy browsers.
3.  **End‑to‑End Test** → Cypress flow: login → select symbol → read page → write query → see Dream tokens.
4.  **Cursor Metrics Hook** updates `cursor_metrics.md` on every code‑gen commit.

## Phase 5  Deployment

1.  **CI/CD (GitHub Actions)**

    *   Job 1: lint + tests (FE & BE)
    *   Job 2: build Docker images, push to registry, trigger Render/Fly deploy.

2.  **TLS & CSP** handled by `nginx_ssl` sidecar (auto‑cert via Let’s Encrypt staging).

3.  **Smoke Tests** run post‑deploy hitting `/health`, `/chat/stream`.

## Phase 6  Post‑MVP Roadmap (Placeholder Tickets)

*   **Kafka + Faust** topic ACLs & signed messages.
*   **Redis** short‑term memory cache & rate limiter.
*   **Elasticsearch** full‑text cross‑Vault search.
*   **LibP2P/IPFS** decentralized Vault export (encrypted blocks).
*   **ChromaDB** or **Weaviate** alt‑embedding store.

Tickets live in `/docs/roadmap.md` and are referenced by Cursor when generating future code.

## Validation Matrix

|       |                                                                           |
| ----- | ------------------------------------------------------------------------- |
|       |                                                                           |
|       |                                                                           |
|       |                                                                           |
|       |                                                                           |
| Phase | Critical Exit Criteria                                                    |
| 0     | Repo at **v0.1‑refactor‑baseline**; no stray dev artifacts                |
| 1     | `make preflight` passes on fresh machine                                  |
| 2     | `npm run dev` shows 5‑column layout & Supabase auth                       |
| 3     | `pytest` passes; `/pages/{story}/{page}` returns HTML; `/search` ≤ 250 ms |
| 4     | Cypress e2e script passes; SSE updates visible                            |
| 5     | GitHub Actions green, Render/Fly returns 200 on `/health`                 |

**Mantra:** *Refactor beats rebuild.* With docs as context, Cursor/Windsurf will generate code that stays in ritual alignment with Gibsey’s symbolic architecture — fast, tidy, and ready for the next dream.
