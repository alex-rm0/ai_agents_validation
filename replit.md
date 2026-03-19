# AI Agents Validation

## Project Overview

Proof-of-concept of a multi-agent AI pipeline (written in Portuguese) that covers a full software development cycle: from interpreting a product requirement to a tested, documented output. Uses OpenRouter (Llama 3.1 8b) via the OpenAI-compatible API.

## Architecture

### Python Agents (`agent/`)
- **Entry point:** `main.py` — CLI orchestrator that runs the full pipeline
- `agent_planner.py` — PM Agent: decomposes a user prompt into GitHub issues with acceptance criteria
- `agent_validator.py` — Validates the plan before proceeding
- `agent_outputs.py` — Writes plan outputs to timestamped run folders
- `agent_github.py` — Creates GitHub issues via the GitHub API
- `agent_frontend_generator.py` — Frontend Agent: generates React TSX components per issue

### React Frontend Preview (`frontend_preview/`)
- React 19 + Vite 8 + TypeScript
- Previews AI-generated components in a live browser
- Generated components land in `frontend_preview/src/generated/`
- Dev server runs on `0.0.0.0:5000`

### Test Engine (`test_engine/`)
- .NET 8 + Playwright + Reqnroll (Gherkin/BDD) + NUnit
- Generic BDD test runner — receives `.feature` files and executes them
- AI-generated `.feature` files go to `test_engine/Features/generated/`
- Target app: `https://dev.nexus.shipperform.devlop.systems/`
- Browser binaries at: `.cache/ms-playwright/chromium-1208/`
- Login selectors: `input[type='text']`, `input[type='password']`, `text=Iniciar Sessão`

### Docs (`docs/`)
- `notas.md` — design decisions and implementation notes

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
