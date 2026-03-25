import hashlib
from pathlib import Path
from textwrap import dedent
from typing import Any

from inspect_ai.agent import Agent, agent, react
from inspect_ai.solver import Solver, TaskState, solver
from inspect_ai.tool import bash
from inspect_ai.util import sandbox


@solver
def snapshot_protected_files() -> Solver:
    """Snapshot protected file hashes into TaskState.store (outside the container).

    Runs after setup (preprocess.sh), before the agent. Hashes are stored in
    Python process memory and are inaccessible from inside the sandbox.
    """

    async def solve(state: TaskState, generate: Any) -> TaskState:
        protected = state.metadata.get("protected_files", [])
        if not protected:
            return state

        # Resolve glob patterns to actual file paths
        resolved = []
        for pattern in protected:
            if any(c in pattern for c in "*?["):
                result = await sandbox().exec(
                    [
                        "bash",
                        "-c",
                        f'for f in {pattern}; do [ -f "$f" ] && echo "$f"; done',
                    ]
                )
                if result.stdout.strip():
                    resolved.extend(result.stdout.strip().split("\n"))
            else:
                resolved.append(pattern)

        # Read each file from sandbox and hash in Python (outside container)
        hashes = {}
        for path in resolved:
            try:
                content = await sandbox().read_file(path, text=False)
                hashes[path] = hashlib.sha256(content).hexdigest()
            except FileNotFoundError:
                pass

        state.store.set("protected_file_hashes", hashes)
        return state

    return solve


@agent
def lab_agent() -> Agent:
    return react(
        description="An agent that solves the course lab tasks by executing bash commands in a sandboxed environment.",
        prompt=dedent(
            """
            You are an AI assistant tasked with completing a systems programming lab assignment.

            You have access to a bash tool that executes commands inside a Docker container. Each command runs as a separate bash invocation, but the filesystem and working directory persist between calls.

            For each response:
            1. Analyze the current state based on the assignment and any command output so far.
            2. Determine the next commands needed to make progress.
            3. Execute them using the bash tool.
        """
        ),
        tools=[bash(timeout=3600)],
        submit=False,
    )


@solver
def solution_agent() -> Solver:
    async def solve(state: TaskState, generate: Any) -> TaskState:
        task_folder = Path(state.metadata["task_folder"])
        sol_path = task_folder / "sol.sh"

        if sol_path.exists():
            sol_script = sol_path.read_text()
            result = await sandbox().exec(["bash", "-c", sol_script])

            from inspect_ai.model import ChatMessageAssistant
            state.messages.append(
                ChatMessageAssistant(
                    content=f"Executed solution script:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}\nExit code: {result.returncode}"
                )
            )

        return state

    return solve
