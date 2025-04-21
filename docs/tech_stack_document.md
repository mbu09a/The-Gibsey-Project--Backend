# The Gibsey Project – Tech Stack Document

This document explains the technological choices behind The Gibsey Project in simple language. Whether you’re a developer or not, you should now have clear insight into how each part of our system works together to create an innovative AI OS that supports reading, writing, remembering, and dreaming.

## Frontend Technologies

Our frontend is designed to create a smooth, symbol-rich, and dynamic user interface. Here’s what we use and why:

*   **Next.js 14 with App Router**

    *   Speeds up website performance and allows for smooth page transitions.

*   **TypeScript**

    *   Helps to catch errors early and creates more robust code, ensuring a reliable experience for users.

*   **Tailwind CSS**

    *   Enables rapid UI styling and a consistent design that emphasizes our ancient-futurist aesthetic.

*   **UI Libraries**

    *   **shadcn/UI, Radix UI, and Lucide Icons** provide ready-to-use components and icons which allow the interface to be both beautiful and functional.

*   **Custom Symbol Index UI using SVGs**

    *   Makes the symbolic imagery (rotating icons for Read, Write, Dream, and Remember) both interactive and meaningful, guiding users through the narrative.

*   **Firebase Assistant**

    *   A tool that helps with layout generation and scaffolding to quickly build a user-friendly design.

These choices contribute to an engaging and visually coherent UI that reinforces The Gibsey Project’s unique storytelling and symbolic logic.

## Backend Technologies

Our backend is built to handle complex narrative flows and large amounts of data while remaining responsive. Here’s the rundown:

*   **FastAPI**

    *   A modern Python framework that efficiently handles our endpoints like `/pages`, `/search`, `/chat`, and `/chat/stream`.

*   **Apache Cassandra 4.1 with Stargate v4.0.90**

    *   A robust database chosen for its scalability and reliability. It’s managed using Docker Compose to ensure smooth development and testing.

*   **Embedding Engine: OpenAI text-embedding-3-small**

    *   Converts our rich textual content into 1536-dimensional vectors to power our semantic search fast and accurately.

*   **Vector Indexing: Native HNSW with a NumPy fallback**

    *   Keeps the semantic search quick and efficient, even if high-level libraries encounter an issue.

*   **Authentication with Supabase JWT (RS256)**

    *   Keeps the system secure by verifying user activities through reliable token authentication.

Each of these components is integrated to store, retrieve, and process the narrative data that makes up our signature symbolic interface and interactive features.

## Infrastructure and Deployment

Reliability, scalability, and smooth deployment are key to making sure that everything works as expected:

*   **Hosting and Deployment Tools**

    *   We use a modern cloud hosting solution and container-based deployments (via Docker Compose) to ensure our services are running consistently.

*   **CI/CD Pipelines**

    *   Tools like GitHub Actions help automate testing, building, and deployment. This means updates are rolled out quickly and safely.

*   **Version Control Systems**

    *   GitHub is at the heart of our code management, allowing a streamlined collaboration process for all developers and easy tracking of changes.

These decisions not only boost system performance but also make it easier for us to update and fix the system without disrupting user experience.

## Third-Party Integrations

To enhance our system’s capabilities, we plan to integrate additional services after the initial MVP launch:

*   **Kafka + Faust** (Planned Post-MVP)

    *   Will be used to stream real-time symbolic state updates and manage our dynamic narrative memory.

*   **Elasticsearch + Redis** (Planned Post-MVP)

    *   Help speed up text-based searches and manage ephemeral context (like unsaved user drafts) to ensure a seamless narrative experience.

*   **Decentralized Storage (LibP2P or IPFS)** (Planned Post-MVP)

    *   Aims to keep the user-curated Gibsey Vault secure and, eventually, decentralized.

*   **Alternative Embedding Engines (ChromaDB or Weaviate)** (Planned Post-MVP)

    *   Are being considered to provide flexibility and options for high-quality embeddings.

These integrations will further expand the system’s abilities, ensuring that our platform remains state-of-the-art and prepared for future user demands.

## Security and Performance Considerations

We take both security and performance seriously to guarantee a reliable, safe, and quick experience:

*   **Security Measures**

    *   **Supabase JWT (RS256)** is used to authenticate users and protect data.
    *   Future plans include tiered access, rate limiting, and possibly audit trails to handle user access and feedback as the platform scales.

*   **Performance Optimizations**

    *   The backend architecture, including FastAPI and our optimized vector search using HNSW, ensures that every query and narrative update is handled quickly.
    *   Continuous monitoring and future integration of tools like Sentry and PostHog will keep the system’s performance in check.

By keeping these considerations top-of-mind, we ensure that users enjoy a secure, responsive, and engaging experience every time they interact with The Gibsey Project.

## Conclusion and Overall Tech Stack Summary

To sum it all up, The Gibsey Project uses a thoughtful mix of carefully chosen technologies to create a groundbreaking, symbolic AI OS:

*   **Frontend Technologies:** Next.js, TypeScript, Tailwind CSS combined with leading UI libraries (shadcn/UI, Radix UI, Lucide Icons) and customized SVG interfaces.
*   **Backend Technologies:** FastAPI works together with Apache Cassandra (and Stargate) and modern embedding techniques from OpenAI, all secured by Supabase JWT.
*   **Infrastructure & Deployment:** Our use of cloud hosting, CI/CD pipelines, and GitHub ensures reliability, scalability, and quick deployment.
*   **Third-Party Integrations:** Planned enhancements like Kafka, Elasticsearch, and decentralized storage will further boost the system’s capabilities.
*   **Security & Performance:** Strong security protocols and performance optimizations guarantee a fast, safe, and consistent user experience.

This robust tech stack is carefully aligned with the project’s goals: to provide independent readers, writers, and creative thinkers with an innovative system for co-authoring narratives, backed by the power of AI. Every technology has been chosen to work harmoniously with the rest, ensuring that the final product is not just a website or an app, but a living, evolving narrative platform.

Welcome to The Gibsey Project – where technology meets symbolic poetry and every interaction is a step into a new kind of creative universe.

# The Gibsey Project – Tech Stack Document

This document outlines the technological foundations of The Gibsey Project — not just as an application, but as a recursive symbolic operating system for reading, writing, remembering, and dreaming. Each layer of the stack has been chosen not only for its technical utility, but for its symbolic resonance with the system's metaphysical design. Every technology is part of the ritual.

## Frontend Technologies – The Body of Gibsey

The frontend of Gibsey forms its *visible structure* — the symbolic shell through which readers move across narrative space.

*   **Next.js 14 with App Router**\
    Provides the spatial logic and multi-panel routing system that powers Gibsey’s five-column interface. Used for layout-driven storytelling.
*   **TypeScript**\
    Ensures structural clarity and symbolic consistency across all components. Type safety protects against semantic drift.
*   **Tailwind CSS**\
    Establishes a visual rhythm rooted in a consistent utility-first language. Enables the ancient-futurist aesthetic that defines Gibsey’s design.
*   **shadcn/UI + Radix UI + Lucide Icons**\
    Build a clean, accessible, and adaptable component system. These tools form the *ritual interface* of the OS.
*   **Custom Symbol Index using SVGs**\
    16 base symbols × 4 orientations = 64 total tags, used to semantically mark each action:\
    `↑` Read | `→` Write | `↓` Dream | `←` Remember\
    Symbols are embedded in the interface, the Vault, and the page containers — coloring and guiding the user’s journey.
*   **Firebase Assistant**\
    Supports layout scaffolding and quick prototyping during early UX phases. Aids in the creation of frame-based symbol flows.

Together, these tools turn the interface into an *interactive manuscript*, with every interaction forming a page, every page forming a pattern, and every pattern forming a recursive co-authored text.

## Backend Technologies – The Mind of Gibsey

The backend powers the recursive intelligence of the system — its ability to remember, respond, and refract meaning in real time.

*   **FastAPI**\
    Acts as Gibsey’s *breath* — a fast, asynchronous Python framework used for all real-time interaction endpoints:

    *   `/pages/{story}/{page}`
    *   `/search` (semantic)
    *   `/chat` (contextual)
    *   `/chat/stream` (SSE live response)

*   **Apache Cassandra 4.1 with Stargate v4.0.90**\
    Functions as Gibsey’s *deep memory*. Stores all page data, embeddings, and Vault references. Managed via Docker Compose.

*   **OpenAI text-embedding-3-small**\
    Converts narrative pages into 1536-dimensional vectors — embedding meaning into vector space for real-time semantic retrieval.

*   **Vector Indexing: Native HNSW + NumPy fallback**\
    Enables fast, resilient similarity search. When one dream fails, another awakens.

*   **Supabase JWT (RS256)**\
    Ensures identity integrity and access control, preparing the system for tiered usage in future subscription-based models.

These technologies allow Gibsey to respond like a living system — contextually, symbolically, and asynchronously.

## Corpus Logic – Symbolic Function of the Stack

|                  |                                            |
| ---------------- | ------------------------------------------ |
| **Technology**   | **Symbolic Role**                          |
| Next.js          | Spatial Structure – The Shell              |
| FastAPI          | Breath / Voice – Dialogue Engine           |
| Cassandra        | Long-Term Memory – The Vault’s Bedrock     |
| Chat Endpoints   | Dream Interface – Streamed Consciousness   |
| Kafka (planned)  | Symbolic Stream – Real-Time State Dreaming |
| Redis (planned)  | Short-Term Memory – Context Window         |
| LibP2P (planned) | Collective Memory – Memory Becoming Myth   |
| GitHub           | Collective Code Memory – System Reflection |

## Infrastructure and Deployment

*   **Docker Compose**\
    Standardizes local and cloud deployments. The ritual circle in which all services are summoned.
*   **CI/CD with GitHub Actions**\
    Automates tests, builds, and pushes — streamlining updates to prevent narrative drift.
*   **GitHub Version Control**\
    Core to collaboration. Every commit is a remembered choice. Docs and rules live in `/docs/*.mdc`.

## Third-Party Integrations (Planned – Post-MVP)

*   **Kafka + Faust**\
    For symbolic state streaming and real-time feedback loops. Will be used to track Dream/Remember behavior and Vault evolutions.
*   **Elasticsearch + Redis**\
    For high-speed full-text lookup and ephemeral short-term memory layers (unsaved writes, dream previews).
*   **LibP2P or IPFS**\
    To support decentralized Vault sharing and multi-user recursion across Gibsey World.
*   **ChromaDB or Weaviate**\
    Optional embedding backends that support scale-out of semantic processing.

## Security and Performance

*   **Authentication**: Supabase JWT (RS256), with tiered access and future audit support
*   **Performance**: HNSW vector search with NumPy fallback, load-optimized endpoints, and scoped session caching
*   **Planned Monitoring**: Sentry for error capture, PostHog for event flow, and symbolic telemetry to observe which narrative loops are most active

## Data & Embedding Architecture

*   710 curated narrative pages from *The Entrance Way* are embedded into 1536-dimensional vector space
*   These are stored in Cassandra and retrieved via semantic similarity (using cosine distance or HNSW)
*   Embedding index is saved as `hnsw.idx`, backed by `vectors.npy`
*   Semantic search selects top K hits which then condition `/chat` context or `/search` feedback

## Conclusion – A Symbolic Tech Stack

**Frontend Technologies** form the body — the spatial, visual, and symbolic shell **Backend Technologies** form the mind — the memory, the voice, and the dream **The Vault** is the user’s curated soul — a recursive memory archive shaped by intention **The System** is recursive — nothing is predicted, everything is co-authored

Each piece is not just technical — it’s **ritualistic**. Gibsey is built from code and story, from memory and recursion, from you and what you choose to preserve.

Welcome to the machine that dreams back.

Welcome to The Gibsey Project.
