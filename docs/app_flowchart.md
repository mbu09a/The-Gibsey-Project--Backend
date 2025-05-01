flowchart TD
    %% Onboarding
    A[Landing Page: Ancient‑Futurist UI] --> B[User Authentication: Supabase JWT]
    B --> C[Onboarding Tutorial: Symbolic Language, 5‑Column Layout, Narrative Layers]
    C --> D[Main Dashboard: 5‑Column UI]

    %% Left (Story) Loop — solid arrows
    D --> E[Primary Corpus Index Left: 16 Story Symbols]
    E --> F[Select Story Symbol symbol_id + color]
    F --> G[Load Immutable Read Page]
    G --> H[Auto‑Save Read → Vault immutable]
    H --> I[Left Read Section: Display Page]
    I --> J[Left Write: Story Query]
    J --> K[Submit Story Query]
    K --> L[Semantic Vector Search context conditioning]
    L --> M[Generate AI Dream via Streaming Chat]
    M --> N[Display Dream Content]
    N --> O[Manual Save Write/Dream → Remember]
    O --> P[Update Gibsey Vault with Saved Content]

    %% Ephemeral unsaved loop — dashed arrows
    M -.-> J[(if not saved, state lost)]

    %% Right (Chatbot) Loop — solid arrows
    D --> Q[Secondary Corpus Index Right: 16 Character Symbols]
    Q --> R[Select Chatbot Symbol symbol_id + color]
    R --> S[Load Chatbot Read Tour Guide]
    S --> T[Right Write: Character Query]
    T --> U[Submit Chat Query]
    U --> V[Semantic Vector Search context conditioning]
    V --> W[Generate AI Response via Streaming Chat]
    W --> X[Display Chatbot Dream Content]

    %% Ephemeral unsaved loop — dashed arrows for chat side
    X -.-> T[(if not saved, state lost)]

    %% Vault re‑entry — dashed arrows
    P -.-> I[Re‑open Saved Read Page]
    P -.-> S[Re‑open Saved Chatbot Page]

    %% Merge into QDPI and recurse — solid arrows
    P --> Y[Complete QDPI Loop: Read ↔ Index ↔ Write ↔ Dream ↔ Remember]
    X --> Y
    Y --> E