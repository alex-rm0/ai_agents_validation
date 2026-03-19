# PM Agent - AI Agents Validation

## Project Overview

A multi-agent AI workflow proof-of-concept written in Portuguese. The system uses an OpenAI-powered PM agent to interpret product requirements, generate GitHub issues, and optionally generate React frontend components.

## Architecture

### Python Backend (`/`)
- **Entry point:** `main.py` — CLI agent orchestrator
- **`agent/` module:**
  - `agent_planner.py` — Generates a structured plan (issues) from a user prompt using OpenAI
  - `agent_validator.py` — Validates the generated plan
  - `agent_outputs.py` — Saves plan outputs to run folders, generates previews
  - `agent_github.py` — Creates GitHub issues via the GitHub API
  - `agent_frontend_generator.py` — Generates React TSX components using OpenAI
  - `utils.py` — Environment variable loading, label validation

### React Frontend (`frontend_preview/`)
- React 19 + Vite 8 + TypeScript
- Displays generated components as a live preview
- Generated components land in `frontend_preview/src/generated/`
- Dev server runs on `0.0.0.0:5000`

## Environment Variables Required

```ini
OPENAI_API_KEY=your_api_key_here
GITHUB_TOKEN=your_github_token
GITHUB_OWNER=github_username
GITHUB_REPO=github_repo_name
```

## Running the Project

- **Frontend preview:** Handled by the "Start application" workflow (`cd frontend_preview && npm run dev`)
- **Python CLI agent:** Run `python main.py` in the shell

## Dependencies

- Python: `openai`, `python-dotenv`, `requests`, `pydantic` (see `requirements.txt`)
- Node: React 19, Vite 8, TypeScript (see `frontend_preview/package.json`)

## Deployment

Configured as a static site — builds the Vite app and serves `frontend_preview/dist`.
