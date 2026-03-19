# PM Agent - AI Agents Validation

## Project Overview

A multi-agent AI workflow proof-of-concept written in Portuguese. The system uses OpenRouter (Llama 3.1 8b) to interpret product requirements, generate GitHub issues, generate React frontend components, and run functional tests.

## Architecture

### Python Backend (`/`)
- **Entry point:** `main.py` — CLI agent orchestrator
- **`agent/` module:**
  - `agent_planner.py` — PM Agent: generates a structured plan (issues) from a user prompt via OpenRouter
  - `agent_validator.py` — Validates the generated plan
  - `agent_outputs.py` — Saves plan outputs to run folders, copies components to frontend preview
  - `agent_github.py` — Creates GitHub issues via the GitHub API
  - `agent_frontend_generator.py` — Frontend Agent: generates React TSX components via OpenRouter

### React Frontend Preview (`frontend_preview/`)
- React 19 + Vite 8 + TypeScript
- Displays generated components as a live preview
- Generated components land in `frontend_preview/src/generated/`
- Dev server runs on `0.0.0.0:5000`

### Test Engine (`test_engine/`)
- .NET 8 + Playwright + Reqnroll (Gherkin/BDD) + NUnit
- Generic reusable functional test runner
- Receives `.feature` files from the AI agent pipeline
- Target app: `https://dev.nexus.shipperform.devlop.systems/`
- Browser binaries at: `.cache/ms-playwright/chromium-1208/`

## Environment Variables Required

```ini
OPENROUTER_API_KEY=your_openrouter_key    # Used by agent_planner and agent_frontend_generator
GITHUB_TOKEN=your_github_token
GITHUB_OWNER=github_username
GITHUB_REPO=github_repo_name
```

## Running the Project

- **Frontend preview:** Handled by the "Start application" workflow (`cd frontend_preview && npm run dev`)
- **Python CLI agent:** `python main.py`
- **Functional tests:** `bash test_engine/run_tests.sh`

## Running Tests for the First Time

1. Build the test project: `cd test_engine && dotnet build`
2. Install Playwright browsers: `pwsh test_engine/bin/Debug/net8.0/playwright.ps1 install chromium`
3. Run tests: `bash test_engine/run_tests.sh`

The `run_tests.sh` script automatically sets the required `LD_LIBRARY_PATH` for Chromium to find `libgbm` in the Nix store.

## Dependencies

- Python: `openai` (for OpenRouter), `python-dotenv`, `requests`, `pydantic` (see `requirements.txt`)
- Node: React 19, Vite 8, TypeScript (see `frontend_preview/package.json`)
- .NET 8: Playwright 1.58, Reqnroll 3.3, NUnit 4.5 (see `test_engine/FunctionalTests.csproj`)
- System: PowerShell (`pwsh`), Mesa (`libgbm`), GLib, NSS, GTK3 (for Chromium)

## Deployment

Configured as a static site — builds the Vite app and serves `frontend_preview/dist`.
