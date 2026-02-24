# Gemini Project Context: Data Viewer

This project is a Streamlit-based data visualization and management tool.

## Project Structure
- `streamlit_app.py`: Main entry point for the Streamlit application.
- `pages/`: Individual Streamlit pages for different functionalities (Data Health, DB Inspector, Inventory Manager).
- `src/`: Core logic and data handling.
    - `database/`: DB connection, operations, and schema definitions.
    - `ui/`: UI components and logic for different modules.
    - `utils/`: Utility functions like logging.

## Tech Stack
- **Frontend/App Framework:** Streamlit
- **Data Handling:** Pandas
- **Database:** Turso (LibSQL)
- **Secrets Management:** Infisical

## Development Guidelines
- Follow Streamlit best practices for UI and state management.
- Keep database operations centralized in `src/database/operations.py`.

## 🔐 1. Secrets Management (Infisical)

The project uses **Infisical** as the single source of truth for secrets (Turso URLs, API Keys, Webhooks).

### A. The SDK & Implementation
*   **Correct Package**: Always use `infisicalsdk` (installed via pip). In code, import as `infisical_sdk`.
*   **Attribute Access**: Use `secret.secretValue` (camelCase) for attribute access when using the new SDK.
*   **Manager Pattern**: All logic is encapsulated in `src/infisical_manager.py`. It initializes the client and handles authentication state.
*   **Usage**: Entry points initialize the manager and fetch secrets during application startup.

### B. Authentication Methods
The manager supports two distinct authentication flows via environment variables:
1.  **Service Token (Legacy/Simple)**:
    *   Requires: `INFISICAL_TOKEN`.
    *   Auth Call: `client.auth.login(token=INFISICAL_TOKEN)`.
2.  **Universal Auth (Machine Identity - Preferred)**:
    *   Requires: `INFISICAL_CLIENT_ID`, `INFISICAL_CLIENT_SECRET`.
    *   Auth Call: `client.auth.universal_auth.login(client_id=..., client_secret=...)`.
*   **Required for both**: `INFISICAL_PROJECT_ID`.

## 🤖 5. CLI Operational Mandates (Gemini CLI ONLY)

The following rules apply **EXCLUSIVELY** to the **Gemini CLI** agent (this interface). They do **NOT** apply to automated agents like Antigravity.

1.  **Automatic Pushing**: Because all actions in the Gemini CLI are directed and approved by the user in real-time, the agent must **always** execute a `git push` immediately after completing a code modification or bug fix. 
2.  **No Manual Staging Required**: The agent should assume that once a task is finished, the state is ready for the remote repository.
3.  **Mandatory Test-Driven Workflow**: After every code modification or bug fix, the agent MUST run the full test suite (`python3 -m pytest tests/`). If tests fail, the agent must fix the errors and re-run the tests until they pass before pushing the changes to GitHub.

---
