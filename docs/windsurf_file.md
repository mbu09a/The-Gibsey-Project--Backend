# .windsurfrules

## Project Overview

*   **Type:** windsurf_file
*   **Description:** Gibsey is a Recursive AI OS and Engine for Reading, Writing, Remembering, and Dreaming — combining AI co-authorship, symbolic UI metaphors, and a custom narrative interface into a whole new creative medium.
*   **Primary Goal:** Build a symbolic, dual-panel AI OS where users co-navigate an interactive book and chat-based narrative system through recursive semantic indexing, character querying, and page-level memory retention.

## Project Structure

### Framework-Specific Routing

*   **Next.js 14 (App Router)** must be used. Enforce the `app/` directory pattern with nested folders:

    *   `app/[route]/page.tsx`
    *   `app/api/[endpoint]/route.ts`
    *   Layouts go in `app/[section]/layout.tsx`

Legacy support for:

*   `pages/` only if migrating older files
*   `src/routes/` for alternative routers (React Router, etc.)

### Core Directories

*   `app/`: Main routing and page rendering
*   `app/api/`: Route Handlers for endpoints like `/pages`, `/search`, `/chat`, `/chat/stream`
*   `components/`: UI primitives (e.g., PageBox, SymbolIndex, WriteBox)
*   `docs/`: Narrative structure, symbolic system reference, and QDPI documentation
*   `data/`: 710 embedded pages, HNSW index (`hnsw.idx`), and NumPy fallback
*   `styles/`: Tailwind and design token definitions (color mappings per symbol/character)
*   `public/`: Static assets like SVG Corpus symbols

## Key Files

*   `app/layout.tsx`: Root layout (with symbolic frame wrappers)
*   `app/page.tsx`: Default landing page, possibly narrative intro or story selector
*   `app/dashboard/layout.tsx`: Used for multi-column symbolic UI (Primary Read, Vault, Secondary Chat)
*   `app/auth/login/page.tsx`: Supabase JWT flow
*   `components/SymbolTag.tsx`: Displays rotated visual tags
*   `components/VaultScroll.tsx`: Chronological timeline of saved pages

## UI Symbolic System

*   Each of the 16 characters or chapters has a base SVG symbol

*   These symbols rotate by meaning:

    *   `UP = Read` (Immutable narrative)
    *   `RIGHT = Write` (Unsaved input)
    *   `DOWN = Dream` (AI-generated response)
    *   `LEFT = Remember` (User-curated memory)

*   Symbol and color tags are attached to:

    *   Pages in the Vault
    *   Frame outlines of current panels
    *   Chatboxes and query inputs

*   **Writes are ephemeral.** Saving a Write transforms it into a Remember with updated symbolic tag.

## UI Panel Layout

*   `Far Left`: Primary Corpus Index (16 story symbols)

*   `Left`: 5 stacked panels

    *   Title
    *   Primary Read
    *   Primary Dream
    *   Primary Remember
    *   Primary Write Box

*   `Center`: The Gibsey Vault (chronological + curated timeline)

*   `Right`: 5 stacked panels

    *   Tour Guide Title (chatbot character name)
    *   Secondary Read
    *   Secondary Dream
    *   Secondary Remember
    *   Secondary Write Box

*   `Far Right`: Chatbot Index (16 character symbols)

## App Flow Integration

*   Read navigation (arrows or symbol select) instantly updates page + Vault
*   Write/Dream/Remember slots **replace** prior content unless saved
*   Color scheme and symbol tag persist in Vault after save
*   No infinite scroll — this is a ritual-based book system

## PRD Compliance

**MVP Rule:**

*   MVP is **desktop-only**
*   One active session at a time
*   Read, Write, Dream, Remember must be **distinct UI elements**
*   Chat is recursive, not infinite — prioritize page generation over scroll

## Version Enforcement

*   `next@14` (App Router only)
*   `typescript@latest`
*   `tailwindcss@latest` with JIT mode
*   `shadcn/ui` + `radix-ui`
*   `lucide-react` for icons

## Optional Enhancements

If you want Windsurf to help with motion or transitions later:

ts

CopyEdit

`// Add Framer Motion for transitions // Tailwind variant: animate-fade, animate-slide, etc.`
