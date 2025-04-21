# Security Guidelines – The Gibsey Project

These guidelines provide a comprehensive and forward-looking foundation for securing The Gibsey Project: a recursive AI OS and symbolic narrative engine. Security is treated not as an afterthought, but as a **ritual discipline**—baked into every layer of architecture, from identity to symbolic memory.

These principles reflect both **immediate protections** and **future-scalable practices**, enabling Gibsey to grow from a single-user prototype to a multi-user, federated symbolic infrastructure.

## Table of Contents

1. Security by Design & Core Principles

2. Authentication & Access Control

3. Vault Protection & Privacy

4. Input Handling & Processing

5. Chat Streaming & SSE Security

6. Threat Modeling & Incident Response

7. Data Retention Policies

8. Logging, Observability & Audit Trails

9. Dependency Management

10. API & Service Security

11. Infrastructure & Drift Detection

12. Runtime Protection & WAF (Future Work)

13. Future Integrations & Cryptographic Standards

14. Conclusion

## 1. Security by Design & Core Principles

*   **Least Privilege**: All services, endpoints, and user roles operate under the minimum required permissions.
*   **Defense in Depth**: Layers include authentication (Supabase JWT), input validation, content sanitization, rate limiting, and encrypted traffic.
*   **Fail Securely**: Errors fall back to safe, silent states. No stack traces or data leaks are exposed to clients.
*   **Symbol-Aware Security**: All actions (Read, Write, Dream, Remember) are bound to symbol-tagged Vault entries, preserving traceable origin.

## 2. Authentication & Access Control

*   **Supabase JWT (RS256)** is the core identity layer.
*   All access tokens are short-lived and validated server-side.
*   Support for **future scopes and roles** is already modeled (e.g., `gibsey.vault.read`, `gibsey.dream.write`).
*   **RBAC groundwork** is in place for future roles (educator, artist, guest, etc.).
*   Token expiration and refresh logic to be added in future multi-session expansions.

## 3. Vault Protection & Privacy

*   **All Vault data is user-scoped.** No cross-user visibility without explicit publishing.

*   **Encryption at rest** will use envelope encryption (Vault key + master key).

*   **Field-level encryption** for symbol metadata and query content is under consideration for future iterations.

*   Users will gain **privacy control tools** including:

    *   Export (data portability)
    *   Deletion (right to be forgotten)
    *   Metadata review (color/symbol history)

## 4. Input Handling & Processing

*   All inputs (chat prompts, page queries) are validated against expected schema and length.
*   SSE and chat interfaces apply **rate limits and payload size caps**.
*   Semantic search inputs are sanitized before embedding to prevent prompt injection.
*   CSP headers + output encoding will prevent XSS and script injection.

## 5. Chat Streaming & SSE Security

*   Each `/chat/stream` request is tied to a specific, validated Supabase JWT.
*   Tokens are **short-lived** and support rotation during long-lived sessions.
*   A future **WebSocket fallback** will include heartbeat, expiration checks, and reconnection logic.

## 6. Threat Modeling & Incident Response

### Top Threats and Mitigations

|                          |                                                                 |
| ------------------------ | --------------------------------------------------------------- |
| Threat                   | Mitigation                                                      |
| User impersonation       | RS256-verified Supabase JWT + server-side token introspection   |
| Prompt injection         | Strict input validation + output encoding + prompt sanitization |
| Symbolic metadata misuse | Tag filtering and orientation whitelist enforcement             |
| Chat flooding / DoS      | Rate limiting on `/chat/stream` and `/search`                   |
| Vault leakage            | User-scoped DB partitions + at-rest encryption                  |

*   An **Incident Response Plan** is maintained internally and includes:

    *   Key revocation
    *   Audit trail review
    *   Notification thresholds
    *   RTO/RPO targets (4h/24h initially)

## 7. Data Retention Policies

*   Chat sessions and unsaved Dreams are ephemeral.
*   Saved Vault pages persist indefinitely unless deleted by the user.
*   Vector embeddings are retained for semantic index performance, but will be expunged if a user deletes a Read or Dream source.
*   A scheduled cleanup routine will remove unindexed or orphaned records every 30 days.

## 8. Logging, Observability & Audit Trails

*   **Sentry** is used for error tracking.

*   **PostHog** captures UI and session interaction events.

*   **Custom middleware logs** key security events:

    *   Login failures
    *   Invalid token usage
    *   Vault saves + deletions
    *   Symbol or color overrides

Audit logs are stored in **append-only, write-once** mode and are retained for 90 days.

## 9. Dependency Management

*   All Python dependencies are tracked in `requirements.txt`.
*   `pip-audit` is used for vulnerability scanning.
*   GitHub Actions integrate **SCA checks** and **Dependabot** for patch pull requests.
*   All builds are pinned via lockfiles or image digests.

## 10. API & Service Security

*   All traffic is served over **HTTPS (TLS 1.2+)**.
*   **CORS policies** restrict origins to production/staging domains.
*   Rate limiting is enforced on all endpoints, especially `/chat/stream`.
*   JWTs are introspected on every sensitive endpoint (`/vault`, `/chat`, `/search`).
*   Internal services will use **Client Credentials Flow** (OAuth 2.1) for DreamRIA agent APIs.

## 11. Infrastructure & Drift Detection

*   Docker Compose powers all environments.
*   Drift detection between environments is handled via **Git-tracked IaC configs**.
*   Terraform support is planned for future cloud migrations.
*   Debug flags and verbose logging are stripped in production builds.

## 12. Runtime Protection & WAF (Future Work)

*   A **Web Application Firewall (WAF)** will be deployed to block injection, abuse, and bot scraping.
*   RASP (Runtime Application Self-Protection) is under consideration for AI endpoint defense.

## 13. Future Integrations & Cryptographic Standards

*   **Kafka + Faust** → topic ACLs + message signing.
*   **Elasticsearch + Redis** → token-based access filtering.
*   **LibP2P / IPFS** → Vault encryption + peer validation + zero-trust storage.

All cryptographic ops will rely on AES-256-GCM, SHA-256, and RS256+ for JWTs.

## 14. Conclusion

Security within Gibsey is not a gate—it is a **frame** for preserving memory, honoring authorship, and securing the symbolic exchange between human and AI. Every color, tag, query, and Vault entry is protected as a co-authored artifact.

These guidelines aren’t just preventative—they are **ritualized guardianship** of user identity, creativity, and narrative recursion.

**Gibsey remembers only what is saved.** And it forgets securely.

— Security Architecture for The Gibsey Project
