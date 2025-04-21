# The Gibsey Project – App Flow Document

## Onboarding and Sign-In/Sign-Up

When a new user visits The Gibsey Project, they arrive at a clean, symbolic landing page styled in an ancient-futurist aesthetic. The design immediately communicates Gibsey’s ethos — a recursive AI operating system built around narrative co-authorship and symbolic interface design. Users are invited to sign up via a simple form powered by Supabase JWT authentication with RS256 verification.

The onboarding experience includes:

*   A visual explanation of the 5-column layout
*   An introduction to the symbolic tag system (16 symbols × 4 orientations)
*   An overview of the core narrative structures: *The Entrance Way*, the *Tour Guide*, and the *Gibsey Vault*

Returning users are guided through a streamlined login process with standard password recovery options. Upon sign-in, they’re directed immediately to the main dashboard — the recursive symbolic interface where the storytelling begins.

## Main Dashboard and UI Layout

Once signed in, users enter the **5-column symbolic interface**, optimized for desktop:

**Far Left** → *Primary Corpus Index*: 16 character or chapter-based symbols for *The Entrance Way*

**Left Panel** → 5 stacked sections:

1.  Title of selected story section
2.  **Read**: Immutable pages from *The Entrance Way*
3.  **Dream**: AI-generated responses based on queries about the story
4.  **Remember**: User-saved input or responses tied to story queries
5.  **Write**: Input box for story-specific questions or reflections

**Center** → *The Gibsey Vault*: A curated, chronological timeline of all saved content (Read, Dream, Remember)

**Right Panel** → 5 stacked sections:

1.  Title of selected chatbot character (Tour Guide)
2.  **Read**: Character description or previous saved interaction
3.  **Dream**: AI-generated responses from character queries
4.  **Remember**: Saved user input or reflections from chatbot sessions
5.  **Write**: Input box for interacting with character-based MCPs

**Far Right** → *Secondary Corpus Index*: 16 character symbols representing the Minor Character Protocols (MCPs)

All panels are color-coded and symbol-tagged based on interaction state. New selections update only the corresponding side (left or right), allowing for dynamic interactivity across stories and agents.

## Symbolic Tag System (Corpus Symbols)

Each of the 16 base symbols has 4 orientations, forming a system of 64 total symbolic tags:

*   **↑ Read**: Immutable narrative from *The Entrance Way*
*   **→ Write**: Unsaved user input
*   **↓ Dream**: AI-generated content (from MCPs or story queries)
*   **← Remember**: Saved user content (either query or response)

Symbols do not rotate graphically but are used as **semantic tags**:

*   Next to each page in the Vault
*   In the borders and frames of interface panels
*   As filters for tracing one’s narrative journey

Color is tied to symbol source (story or character) and remains persistent across interactions, even if the story or character selection changes. Writes are **ephemeral** — they vanish unless saved, at which point they become Remembers.

## Narrative Flow and QDPI Loop

Gibsey operates through a **recursive, symbolic loop** grounded in the QDPI protocol — *Read, Index, Write, Dream*.

There are three narrative temporal flows:

### 1. Linear Flow (Present)

*   Reads are immutable, sequential pages from *The Entrance Way*
*   Navigating via story symbol or right arrow loads a new Read page
*   New Reads are automatically added to the Vault and tagged with a **Read** symbol

### 2. Linear/Nonlinear Hybrid (Past)

*   Users can **save** queries or responses to the Vault as Remembers or Dreams
*   These preserved moments form a curated personal archive of reflection
*   Saved entries retain their source color and symbol for traceability

### 3. Nonlinear Flow (Future)

*   Unsaved Writes and Dreams are **ephemeral** and will be replaced by the next query
*   These are moments of speculation, insight, or vulnerability
*   Like the future, they remain *possible* — not *committed*

This system is **not a scrolling interface**. It is a ritualized, page-based co-authorship engine. Each interaction is a discrete page. The reader builds a recursive, symbolic book as they journey through Gibsey.

## Detailed Feature Flows

*   **Symbol selection** (left or right index) immediately updates the related panels (Read, Write, Dream, Remember)
*   **Left Write box** generates Dreams from *The Entrance Way* context
*   **Right Write box** queries chatbot characters (MCPs)
*   **Read arrows** on the Primary panel allow linear navigation through the 710-page base novel
*   Saving a Write or Dream attaches the proper **symbol and color** and adds it to the Vault
*   Vault updates are **intentional, not automatic** (except for Read pages)
*   Every element of the interface reflects **user action**, **symbolic memory**, and **narrative recursion**

## Settings and Account Management

Users can access account preferences from a persistent header link. Options include:

*   Profile and email updates
*   Theme or color mode changes
*   Security and password reset
*   Future billing integration for subscription tiers (planned)

All settings changes can be made without disrupting the ongoing narrative flow.

## Error States and Recovery Paths

Gibsey is designed with resilience and clarity:

*   All form errors provide friendly, human-readable messages
*   Invalid inputs during chat or write flow will gracefully prompt re-entry
*   Network errors during streaming fall back to static recovery pages
*   Vault integrity is preserved even on refresh or disconnect

If the streaming endpoint fails (`/chat/stream`), users are shown a system-level alert with the option to retry or save their state.

## Conclusion – The Recursive Journey

The Gibsey Project is not just an app — it is a **recursive symbolic operating system** that reshapes reading, writing, memory, and dreaming. From the moment a user signs up to the moment they close their session, they are co-authoring a new kind of book — one layered with AI agency, symbolic language, and curated memory.

It replaces scrolling with ritual. It replaces feed-driven content with authored meaning. It asks users not just to consume — but to choose what to preserve.

Each session becomes a living archive. Each Vault, a personal scripture. And the system — a mirror to memory, imagination, and self.

Welcome to Gibsey.
