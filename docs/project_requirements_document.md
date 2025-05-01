# The Gibsey Project — Product Requirements Document (MVP v0.2)

*Last updated: 2025‑04‑20*

## 1. Overview — From Scarcity to **Gifted Abundance**

The Gibsey Project is an **AI Operating System for Reading, Writing, Remembering, and Dreaming**. By fusing human authorship with advanced AI, it turns one‑way reading into a living, bi‑directional dialogue. A five‑panel desktop interface—driven by 16 rotating SVG symbols— guides users through fixed pages, free‑form writing, real‑time AI dreams, and an ever‑growing Vault of memory.

**Problem │ Artificial Abundance, Structural Scarcity**\
Token‑metered AI keeps knowledge expensive and linear.

**Solution │ Gifted AI powered by the Quad‑Directional Protocol Interface (QDPI)**\
Gibsey treats every action as a **Gift loop**—the user gives, the system reciprocates—collapsing cost while amplifying meaning.

**Definition of Done (MVP)**   A new visitor can complete a full **QDPI cycle** (Read → Index → Write → Generate) on any page of *The Entrance Way*, entirely in‑browser, no dev tools required.

## 2. Scope

### 2.1 In‑Scope (Desktop‑only MVP)

*   Supabase JWT (RS256) authentication
*   Five‑panel symbolic UI (Primary Read, Write, Dream, Gibsey Vault, Tour‑Guide)
*   710 embedded pages (1 × 1536‑dim vector each) + HNSW search
*   Real‑time SSE chat (`/chat/stream`) and context‑aware `/search`
*   Corpus Symbol Layer: **16 symbols × 4 orientations** (Read ↑, Write →, Dream ↓, Remember ←)
*   Automatic Vault timeline of Reads & curated Dreams
*   **QDPI** request‑logging across all endpoints
*   Frontend (Next.js 14) ↔ Backend (FastAPI + Cassandra) separation

### 2.2 Out‑of‑Scope (for MVP)

*   Mobile/tablet UIs & multi‑user sessions
*   DreamRIA surreal agent layer & tokenized TNAs economy
*   Kafka/Faust, Elasticsearch, LibP2P/IPFS integrations
*   Formal moderation workflows, accessibility/i18n

## 3. User Flow (First‑session narrative)

1.  **Log in** → Supabase verifies RS256 JWT.
2.  **Select Symbol** in the left index → matching immutable **Read** page loads; entry auto‑saves to Vault.
3.  **Index** happens silently: page embedding linked across symbol graph.
4.  **Write** prompt in the middle‑left panel; submit.
5.  **Generate (Dream)**: FastAPI streams AI tokens in real time into the right panel.
6.  User may **Remember** (save) a Dream back to Vault, completing the QDPI loop.

## 4. Quad‑Directional Protocol Interface (QDPI)

|                  |       |                                 |                                      |
| ---------------- | ----- | ------------------------------- | ------------------------------------ |
| Phase            | Glyph | Function                        | System Endpoints                     |
| **Read (X)**     | 📖    | Retrieve canonical material     | `GET /pages`, `GET /vault/{id}`      |
| **Index (Y)**    | 🗂️   | Create links, tags, embeddings  | `POST /index` (+ async graph update) |
| **Write (A)**    | ✍️    | User (or agent) drafts new text | `POST /write`                        |
| **Generate (Z)** | 🤖    | System emits refracted response | `POST /chat`, `POST /dream`          |

`flowchart LR X(Read) --> Y(Index) --> A(Write) --> Z(Generate) --> X`

The four phases map **one‑to‑one** onto the symbol orientations used throughout the UI.

## 5. Core Features

### 5.1 Interface & Symbolic Layer

*   Dual scroll streams (Primary Read / Secondary Dream)
*   Symbol rotations drive dynamic color themes
*   Vault timeline shows color‑coded history; Save‑to‑canon toggle

### 5.2 Backend Services

*   **Semantic Search** — 710 × 1536‑d vectors, HNSW + NumPy fallback (< 250 ms p95)
*   **Streaming Chat** — SSE token push, coherent context, MCP persona selection
*   **Autonomous MPC Agents** — character‑driven flavours for Generate phase
*   **QDPI logging** — every request tagged X/Y/A/Z for analytics & future TNAs

## 6. Tech Stack & Tools

|                  |                                                   |                                                    |
| ---------------- | ------------------------------------------------- | -------------------------------------------------- |
| Layer            | Tech                                              | Notes                                              |
| **Frontend**     | Next.js 14 (App Router), TypeScript, Tailwind CSS | shadcn/ui, Radix UI, Lucide icons                  |
| **Backend**      | FastAPI, Uvicorn, Python 3.11                     | `/pages`, `/search`, `/chat`, `/chat/stream` (SSE) |
| **Datastore**    | Apache Cassandra 4.1 + Stargate                   | Docker Compose; nightly snapshot task              |
| **Embeddings**   | OpenAI *text‑embedding‑3‑small*                   | 1536‑d vectors                                     |
| **Auth**         | Supabase JWT (RS256)                              | HS256 bypass in dev                                |
| **Dev Ops**      | GitHub Actions, Bandit, pip‑audit, locust         | Lint, type‑check, load‑test                        |
| **IDE / Agents** | Cursor, CodeGuideDev, VS Code, Windsurf           | AI‑assisted code reviews                           |

Post‑MVP roadmap: Kafka + Faust, Ollama LLM, Elasticsearch + Redis, LibP2P/IPFS.

## 7. Non‑Functional Requirements

*   **Performance** — Page load < 400 ms; vector search < 250 ms; SSE tokens ≤ 100 ms gap.
*   **Scalability** — Single‑user MVP; architecture supports async workers & horizontal scaling.
*   **Security** — RS256 JWT, rate‑limits, TLS; Vault data encrypted at rest.
*   **Observability** — Sentry error tracking, PostHog analytics; search & chat latency logged.
*   **Usability** — Desktop‑first; color‑blind‑safe palette; minimal clicks to complete QDPI.

### 7.1 Success Metrics

|                                                    |          |
| -------------------------------------------------- | -------- |
| Metric                                             | Target   |
| First‑session completion of Read→Write→Dream cycle | ≥ 90 %   |
| Median page‑load time                              | < 400 ms |
| Vector search latency p95                          | < 250 ms |

## 8. Milestones & Timeline

|                            |         |                |
| -------------------------- | ------- | -------------- |
| Milestone                  | Owner   | ETA            |
| Backend endpoints complete | Brennan | **Apr 26 ’25** |
| Symbol‑aware UI beta       | Maggie  | **May 03 ’25** |
| Vault storage & timeline   | Brennan | **May 10 ’25** |
| Security & load‑test pass  | —       | **May 15 ’25** |
| MVP soft launch            | Both    | **May 17 ’25** |

## 9. Quality Gates (Reviewer Checklist)

*   **Security** — No secrets in git; Bandit & pip‑audit clean; CORS locked.
*   **Performance** — locust: 100 concurrent vector searches < 500 ms p95.
*   **Backup** — Cassandra snapshot cron verified.
*   **UX** — Color contrast AA; Lighthouse desktop score > 90.
*   **Content Safety** — Prompt guardrails against jailbreaks/profanity.

## 10. Constraints & Assumptions

*   Desktop‑only MVP; uniform interface for all users.
*   Symbol animations limited to CSS rotations; no WebGL for launch.
*   Third‑party services (Supabase, OpenAI) remain available within rate limits.
*   FastAPI SSE implementation is adequate for single‑user load.

## 11. Known Issues & Risks

*   **Streaming stability** under spotty networks.
*   **Symbol‑state drift** between UI panels if orientation math mis‑fires.
*   **Future multi‑user scaling** will require partitioned Vaults & Cassandra tuning.
*   **External dependency changes** (OpenAI model deprecation, Supabase auth updates).

## Appendices

### A. Personas & Jobs‑to‑Be‑Done

|                |                             |                                                         |
| -------------- | --------------------------- | ------------------------------------------------------- |
| Persona        | Goal                        | JTBD                                                    |
| Curious Reader | Explore story out of order  | “Let me jump anywhere and understand what I missed.”    |
| Fan Theorist   | Cross‑link lore & symbolism | “Surface all pages about *Jacklyn Variance* instantly.” |
| Educator       | Assign passages to students | “Track what each student has read & discussed.”         |

### B. Source Files

*   **VISION.md** — narrative and philosophical foundations
*   **RULES_OF_THE_GAME.md** — canonical design laws
*   **ROADMAP.md** — future feature map
*   **TEAM.md** — bios & advisory spirits
