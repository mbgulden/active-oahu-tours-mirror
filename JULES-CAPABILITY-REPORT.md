# Jules CLI Capability Report

## 1. CLI Surface

The Jules CLI is the primary interface for developers and orchestrators to interact with the Jules agent system from the command line.

### Core Commands
- **`jules new <description>`**: Initiates a new task. Jules will analyze the description and begin execution within the local or specified environment.
- **`jules remote <subcommand>`**: Manages interactions with remote repositories and tasks.
    - `list`: Lists active remote tasks or branches.
    - `pull`: Pulls changes from a remote task branch.
    - `apply`: Applies changes from a remote source to the current workspace.
- **`jules teleport`**: Launches the interactive Terminal User Interface (TUI). This provides a rich, persistent environment for real-time collaboration with Jules.

### Flags & Options
- **`--repo <path|url>`**: Specifies the target repository for a command, overriding the default local discovery.
- **`--parallel`**: Enables parallel execution for compatible tasks (e.g., batch processing files).
- **`--session <id>`**: Resumes a specific session using its unique ID.

---

## 2. TUI Commands (Slash Commands)

When inside the `teleport` TUI, Jules supports several slash commands to control the agent's state and workflow.

- **`/help`**: Displays a list of available commands and tool documentation.
- **`/submit`**: Finalizes the current task, runs pre-commit checks, and prepares the submission (PR/Commit).
- **`/handoff <agent_name>`**: Transitions the current context to another agent.
    - Example: `/handoff AGY` for UI/Visual tasks.
- **`/clear`**: Clears the conversation history in the TUI view.
- **`/undo`**: Reverts the last file modification made by Jules.
- **`/plan`**: Displays or updates the current execution plan.

---

## 3. Hidden & Advanced Features

- **Continuation Mode**: Triggered by including "CONTINUATION MODE" in a request along with a valid session ID. This allows Jules to bypass initial discovery and resume work autonomously.
- **Self-Correction Loop**: Jules automatically attempts to fix its own errors (e.g., bash command failures or linting errors) without user intervention.
- **Artifact Protection**: Jules is designed to detect build artifacts (e.g., `dist/`, `build/`) and will refuse to edit them directly, instead searching for the source code.
- **`AGENTS.md` Protocol**: Jules follows instructions in `AGENTS.md` files hierarchically. Root-level files provide global instructions, while nested files provide local overrides.

---

## 4. Integration Patterns

### Linear Integration
Jules is deeply integrated with Linear for project management.
- **Task Identification**: Automatically parses Task IDs (e.g., `GRO-142`).
- **Status Syncing**: Updates task status in real-time (`Todo` -> `In Progress` -> `In Review` -> `Done`).
- **Comment Monitoring**: Jules "listens" to comments on Linear issues to receive feedback and iterate on tasks.

### GitHub Integration
- **PR Management**: Automatically opens and updates Pull Requests.
- **Branch Strategy**: Creates feature-specific branches (e.g., `feat/`, `fix/`, `docs/`) based on the task description.
- **Mirroring**: Supports working in mirrored repositories with automatic synchronization.

---

## 5. Multi-Agent Ecosystem

Jules operates as part of a specialized agent droid fleet:
- **Fred (The Orchestrator)**: Handles task dispatching, high-level planning, and cross-task coordination.
- **Jules (The Engineer)**: The core software engineering droid (this agent).
- **AGY / Antigravity (The Designer)**: Specialist in UI, UX, and visual verification.

---

## 6. Environment Variables & System Paths

- **`JULES_SESSION_ID`**: Persists the session context across multiple tool calls and CLI invocations.
- **`GIT_TERMINAL_PROMPT=0`**: Ensures git operations are non-interactive to prevent hanging in headless environments.
- **`PATH` additions**: Jules' environment includes specialized paths for modern tooling, such as `/usr/local/bun/bin`, `/home/jules/.pyenv/shims`, and `/opt/android-sdk`.
- **System Configs**: Jules uses a specialized `.gitconfig` with `google-labs-jules[bot]` identity for all automated commits.

---

## 7. Limits & Constraints

- **Context Window**: ~200,000 tokens (powered by Claude 3.5 Sonnet). Large codebases are handled via targeted search and file reading rather than full ingestion.
- **Sandbox Environment**: Jules operates in a contained bash environment with access to standard dev tools (npm, pip, bun, etc.) but restricted root access unless via `sudo`.

---

## 8. Best Practices for Orchestrators

1. **Batching**: Assign work in small batches (e.g., 5 tasks). This maximizes parallel processing without overwhelming the agent's context.
2. **Explicit Handoffs**: Use `/handoff` when a task moves from engineering to visual design to ensure the right specialist is engaged.
3. **Comment-Driven Development**: Treat Linear comments as the primary feedback loop. Provide specific, pinpointed feedback rather than vague requests.
4. **The 24-Hour Rule**: For high-stakes architectural decisions, allow Jules to "reflect" by providing a plan and waiting for confirmation after a period of time.
