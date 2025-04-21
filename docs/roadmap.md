# Roadmap

This document is a living, kanban‑style roadmap that tracks completed, testing, backlog, and future features with target dates for The Gibsey Project.

## Overview

The Gibsey Project is an AI OS that blends human authorship and advanced AI to foster a new medium of recursive storytelling, symbolic interaction, and narrative co-authorship. This roadmap reflects our agile approach to building an immersive, desktop-first experience through iterative milestones and planned integrations.

Below is the current status of key milestones and features, organized into four columns:

### Completed

*   **Backend Endpoints Complete**

    *   *Description:* All key backend endpoints (e.g., `/pages`, `/search`, `/chat`, `/chat/stream`) have been implemented.
    *   *Target Date:* April 26, 2025

### Testing

*   **Symbol‑Aware UI Beta**

    *   *Description:* Initial testing for the 5‑column symbolic interface and dynamic color themes is underway.
    *   *Target Date:* May 03, 2025

*   **Vault Storage & Timeline**

    *   *Description:* Validation of the automatic Vault timeline, where user interactions (Reads, Dreams, Remembers) are recorded and color-tagged.
    *   *Target Date:* May 10, 2025

### Backlog

*   **Security & Load‑Test Pass**

    *   *Description:* Ongoing improvements to security measures including RS256 JWT, rate‑limiting, and comprehensive load testing. This phase will ensure robust performance and data integrity.
    *   *Target Date:* May 15, 2025

### Future Features

*   **MVP Soft Launch**

    *   *Description:* Final release of the desktop‑only MVP, integrating all core functions of the Quad‑Directional Protocol Interface (QDPI) cycle—Read, Index, Write, and Generate.
    *   *Target Date:* May 17, 2025

*   **Post‑MVP Integrations**

    *   Planned features include:

        *   Kafka + Faust for real‑time symbolic state streaming
        *   Ollama for local LLM support
        *   Elasticsearch + Redis for real‑time symbolic updates
        *   LibP2P/IPFS for decentralized Vault storage
        *   Alternative embedding solutions such as ChromaDB or Weaviate

## Additional Milestones & Timeline

|                            |         |             |
| -------------------------- | ------- | ----------- |
|                            |         |             |
|                            |         |             |
| Milestone                  | Owner   | Target Date |
| Backend endpoints complete | Brennan | Apr 26 '25  |
| Symbol‑aware UI beta       | Maggie  | May 03 '25  |
| Vault storage & timeline   | Brennan | May 10 '25  |
| Security & load‑test pass  | —       | May 15 '25  |
| MVP soft launch            | Both    | May 17 '25  |

## How to Use This Roadmap

*   **Dynamic Updates:** This document is updated regularly to reflect current progress on completed tasks, items in testing, backlog priorities, and future feature planning.
*   **Feedback Loop:** As with the QDPI cycle, every new milestone and retrospective drives iterative improvements to both the product and the roadmap itself.
*   **Kanban Style:** The roadmap is maintained in a kanban style to facilitate transparency and enable the team and stakeholders to track progress at a glance.

## Conclusion

This roadmap serves not only as a project management tool but also as a symbolic narrative of The Gibsey Project’s journey. As we move from a completed backend framework to an immersive, symbol-driven UI and full MVP launch, every milestone contributes to the transformation from token‑metered scarcity to gifted AI abundance.

*Stay tuned for further updates as we continue to build, test, and refine the Gibsey experience.*Gibsey Roadmap – v0.2   *(Refactor Sprint → Private‑Alpha)*

**Timebox:** April 2025 → June 2025   |   **North‑Star:** Ship a stable, doc‑aligned desktop MVP (5‑column UI, semantic search, streaming chat, encrypted Vault) to a closed tester cohort.

## Overview

The roadmap is maintained kanban‑style and updated continuously by Cursor hooks (§ Validation Matrix).\
It marries **technical milestones** (vector index latency, TLS, audit logs) with **symbolic goals** (color‑true UI, Vault ritual flow).\
Every checkbox is both a project task **and** a page in Gibsey’s unfolding narrative.

## Kanban Board

✅ Completed (v0.1‑baseline)

*   [x] **FastAPI skeleton** `backend/main.py`) + Swagger.
*   [x] **Cassandra 4.1 + Stargate** dockerised.
*   [x] **710 Entrance Way pages** embedded (1536‑d) and seeded.
*   [x] **Next.js 14 prototype grid** (5‑column).
*   [x] **Supabase JWT auth (RS256)** round‑trip.
*   [x] **Backend endpoints complete** `/pages`, `/search`, `/chat`, `/chat/stream`). *(Apr 26 ’25)*

🧪 Testing

*   [ ] **SymbolIndex colour mapping** ↔ `/docs/colors.json` *(May 03 ’25 target)*
*   [ ] **SSE latency** `/chat/stream` ≤ 100 ms token gap
*   [ ] **Vector search** HNSW top‑K ≤ 250 ms
*   [ ] **Vault timeline** auto‑tag validation *(May 10 ’25)*

🚧 In Progress (Refactor Sprint)

*   [ ] Phase 0 cleanup script + `v0.1‑refactor‑baseline` tag
*   [ ] Move docs → `/docs` & wire `.cursor/context.json`
*   [ ] `make preflight` Node/Python verifier
*   [ ] `nginx_ssl` sidecar + mkcert TLS for local HTTPS
*   [ ] CSP + HSTS headers via `next.config.js`

🔜 Backlog (MVP Hard Blockers)

*   [ ] `scripts/load_corpus.py` seeding + index build
*   [ ] Cursor metrics auto‑hook → `cursor_metrics.md`
*   [ ] Cypress E2E flow (login → read → write → dream → remember → vault revisit)
*   [ ] Security + load‑test pass (rate limiting, JWT replay tests) *(May 15 ’25)*
*   [ ] GitHub Actions CI/CD → Render/Fly deploy

🌱 Future Features / Post‑MVP

*   [ ] Kafka + Faust symbolic state streaming
*   [ ] Redis cache (short‑term Dream/Write memory)
*   [ ] Elasticsearch + Kibana full‑text Vault search
*   [ ] LibP2P/IPFS decentralised Vault export
*   [ ] Alt embedding store (ChromaDB / Weaviate)
*   [ ] Ollama local LLM support

## Milestone Timeline

|                |                  |            |                                                        |
| -------------- | ---------------- | ---------- | ------------------------------------------------------ |
|                |                  |            |                                                        |
| Milestone      | Owner            | ETA        | Exit Criteria                                          |
| **v0.2‑alpha** | Brennan & Maggie | 2025‑05‑15 | All Backlog items checked; private invite list live    |
| **v0.3‑beta**  | Brennan          | 2025‑06‑15 | Redis cache + audit logs in prod; Cypress 100 % pass   |
| **v1.0**       | Both             | 2025‑Q3    | Public desktop launch; funding deck final; docs frozen |

## Changelog

*   **2025‑04‑23** Roadmap merged with CodeGuide version; added kanban sections.
*   **2025‑04‑20** Doc overhaul (frontend, backend, security).
*   **2025‑03‑08** Vector index proof‑of‑concept complete.
*   **2025‑02‑14** Supabase auth prototype merged.

## Validation Matrix

|             |                                                                     |
| ----------- | ------------------------------------------------------------------- |
|             |                                                                     |
| Phase       | Critical Exit Criteria                                              |
| Cleanup     | `git status` shows only expected dirs; CI green                     |
| Env & Docs  | `make preflight` passes; `.cursor/context.json` references all docs |
| FE Refactor | `npm run dev` shows colour‑true 5‑column UI + auth                  |
| BE Refactor | `/search` ≤ 250 ms; `/chat/stream` token gap ≤ 100 ms               |
| Integration | Cypress E2E script passes locally                                   |
| Deployment  | Render/Fly returns **200/OK** on `/health`; TLS cert valid          |

**Doctrine:** *Write → Dream → Remember → Refactor.*

Roadmap lives at `/docs/ROADMAP.md`.\
Checkboxes are updated via PR titles (`[x] …`) to keep Cursor metrics and Windsurf kanban in sync.
