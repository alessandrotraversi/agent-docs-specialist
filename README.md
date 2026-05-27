# LangChain Agents with Local Ollama

This project demonstrates how to build and run AI agents using [LangChain](https://www.langchain.com/) and [Ollama](https://ollama.com/) for local LLM execution. It provides a modular agent to generate technical documentation.

## Features

- **Documentation Agent**: A modular agent using LangGraph to generate PRD, ADR, FDD, and Design Docs from a project interview.
- **Diagram Generation (Mermaid & PlantUML)**: Ability to generate and save Mermaid.js diagrams (for general flows) and PlantUML (specifically for C4 model) as part of the documentation workflow or via a standalone CLI.
- **Project History & Persistence**: Uses PostgreSQL (via Docker) to store workflow checkpoints (LangGraph) and a project knowledge base to maintain consistency across different document generations.
- **Local Execution**: All models run locally on your machine via Ollama, ensuring data privacy and no API costs.
- **Security Audit**: Includes `pip-audit` to validate project dependencies against known vulnerabilities.
- **Code Quality**: Uses `ruff` for linting and `pytest` for automated testing.

## Prerequisites

1.  **Ollama**: Install Ollama from [ollama.com](https://ollama.com/).
2.  **Local Model**: Pull the `llama3.1` model (used by default in the scripts):
    ```bash
    ollama pull llama3.1
    ```
3.  **Docker**: Needed for PostgreSQL persistence.
4.  **Python**: Python 3.9 or higher is recommended.

## Installation

1.  Clone this repository to your local machine.
2.  Start the infrastructure (PostgreSQL via Docker):
    ```bash
    docker-compose -f docker/docker-compose.yml up -d
    ```
3.  Create a virtual environment:
    ```bash
    python -m venv .venv
    ```
4.  Activate the virtual environment:
    - **macOS/Linux**: `source .venv/bin/activate`
    - **Windows**: `.venv\Scripts\activate`
5.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Ensure Ollama and PostgreSQL (Docker) are running in the background before executing the scripts.

### 1. Documentation Agent (from Interview)
This agent takes a project interview and generates a full suite of documents (PRD, ADR, FDD, Design Doc).
```bash
export PYTHONPATH=$PYTHONPATH:.
python src/main.py
```

### 2. Diagram Generator (Standalone)
You can generate diagrams independently by providing a description and type.
```bash
export PYTHONPATH=$PYTHONPATH:.
python src/tools/generate_diagram_cli.py "Description of your system" C4Context my_diagram
```
Supported types: 
- **Mermaid**: `flowchart`, `sequence`, `class`, `state`, `er`, `gantt`, `pie`.
- **PlantUML**: `C4Context`, `C4Container`, `C4Component`.

### 5. Security Audit
We use `pip-audit` to ensure the security of our dependencies.

#### Check for vulnerabilities in current environment:
```bash
python scripts/audit_packages.py
```

#### Add a new package and check security automatically:
```bash
python scripts/add_package.py <package_name>
```

### 6. Code Quality (Linting)
We use `ruff` to maintain code quality and consistency.

#### Run linter:
```bash
python scripts/run_ruff.py
```

#### Automatically fix issues:
```bash
python scripts/run_ruff.py --fix
```

### 7. Testing
We use `pytest` with `pytest-cov` for coverage and `pytest-sugar` for a better test output. Our test suite is divided into:
- **Unit Tests**: Individual components like LLM loaders and diagram tools.
- **Integration Tests**: Logic verification between modules and data repositories.
- **Functional Tests**: End-to-end verification of the LangGraph agent workflow.
- **Acceptance Tests**: Verification if the generated documents meet format requirements.
- **Regression Tests**: Ensuring previously fixed issues (like data extraction) remain resolved.

#### Run all tests with coverage:
```bash
python scripts/run_tests.py
```

### 8. Repository Protection
A GitHub Ruleset configuration is provided in `branch_protection_ruleset.json` to protect the `main` branch. This ruleset:
- Restricts deletions and non-fast-forward pushes.
- Requires pull requests with at least one approval.
- Restricts merge/bypass permissions to Repository Admins (Owners).

To apply this, go to your GitHub Repository Settings -> Code and automation -> Rules -> Rulesets -> Import ruleset.

### 9. Continuous Integration (CI)
A quality pipeline is configured via GitHub Actions in `.github/workflows/quality.yml`. For every Pull Request targeting the `main` or `master` branches, the following checks are automatically executed:
- **Linting**: Runs `ruff` to ensure code style and quality.
- **Security Audit**: Runs `pip-audit` to check for known vulnerabilities in dependencies.
- **Automated Tests**: Runs the full `pytest` suite with code coverage, using a temporary PostgreSQL service.

### 10. Auto Changelog
A workflow is configured in `.github/workflows/changelog.yml` to automatically update the `CHANGELOG.md` file every time a change is merged into the `main` or `master` branches. It uses the message of the latest commit/merge to document progress.

### 11. Conventional Commits
The project enforces the [Conventional Commits](https://www.conventionalcommits.org/) specification for all commit messages. A validation pipeline is configured in `.github/workflows/commit-lint.yml`.

#### Supported Types:
- `feat`: New features.
- `fix`: Bug fixes.
- `docs`: Documentation changes.
- `style`: Formatting, missing semi-colons, etc (no code changes).
- `refactor`: Refactoring production code.
- `perf`: Performance improvements.
- `test`: Adding tests, refactoring tests.
- `build`: Build system or external dependencies.
- `ci`: CI configuration files and scripts.
- `chore`: Other changes that don't modify src or test files.
- `revert`: Reverts a previous commit.

#### Local Validation:
You can check your last commit message locally:
```bash
python scripts/check_commit.py
```

## Project Structure

- `src/`: Core source code.
    - `main.py`: Main entry point for the Documentation Agent.
    - `agent/`: Agent logic and LangGraph workflows with PostgreSQL persistence.
    - `llm/`: LLM configuration and loaders.
    - `memory/`: PostgreSQL database connection and repository for project history.
    - `prompts/`: Template prompts enhanced with history injection.
    - `tools/`: Independent tools for diagram generation.
    - `config/`: Centralized environment configurations.
- `docker/`: Contains infrastructure configuration (e.g., `docker-compose.yml`).
- `requirements.txt`: Python dependencies.
- `scripts/`: Utility scripts for auditing, linting, and testing.
- `tests/`: Automated tests with pytest.
- `.outputs/`: Generated documents (PRD, ADR, etc.).
