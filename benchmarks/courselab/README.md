# Course Lab Benchmark

Evaluate AI agents on systems programming lab assignments.

> Leaderboard hosted on HuggingFace Spaces: [sys-intelligence/leaderboard](https://huggingface.co/spaces/sys-intelligence/leaderboard)

```bash
pip install -e .

# Modify and run the evaluation script directly:
python run_eval.py

# If using internal TRAPI model, modify and run the custom script:
python run_eval_trapi.py

# View results
inspect view
```

## Task Structure

Each lab task requires the following files:

```
data/course_id/task_id/
├── config.json      # Task metadata and artifacts to capture
├── task.md          # Problem statement shown to the agent
├── compose.yaml     # Docker sandbox configuration
├── evaluate.sh      # Grading script (exit 0 = pass, non-zero = fail)
├── sol.sh           # Reference solution script to validate task solvability
├── preprocess.sh    # Optional: setup script run before agent starts
└── starter/         # Optional: starter files copied to workspace
    └── *.py
```

- `config.json`: Contains `instance_id`, `course_id`, `timeout_minutes`, optional `artifacts` list (files to capture after evaluation), and optional `protected_files` list (files the agent must not modify — verified via hashing outside the container)
- `task.md`: Problem description given to the agent
- `compose.yaml`: Docker sandbox specification
- `evaluate.sh`: Runs tests and returns exit code 0 for pass, non-zero for fail
- `sol.sh`: Reference solution script that validates the task is solvable (executable bash script)
- `preprocess.sh`: Optional setup script that runs before the agent starts
- `starter/`: Optional directory containing starter files that are copied to the workspace with the same relative paths

See [`tutorial/distributed_systems/task_1_echo_server/`](tutorial/distributed_systems/task_1_echo_server/) for a complete example.

## Adding New Labs

The `course_id` must follow the convention `institution_course_year` using lowercase and underscores (e.g., `mit_6_5840_2024`, `uw_madison_cs537_2018`). The folder name inside `data/` must match the `course_id`. Task folders must be named `task_N_name` (e.g., `task_1_mapreduce`, `task_3a_raft`) and the `instance_id` in `config.json` must be `{course_id}__{task_folder_name}` (e.g., `mit_6_5840_2024__task_1_mapreduce`).

1. Create task directory: `data/course_id/task_id/`
2. Update `data/courses.json` with course metadata (including a `category` from: `Intro to Systems`, `Operating Systems`, `Distributed Systems`, `Database Systems`)
3. Add `config.json`, `task.md`, `compose.yaml`, and `evaluate.sh`
4. Optionally add `starter/` directory with skeleton code
5. Optionally add `preprocess.sh` for environment setup
6. Add `protected_files` to `config.json` listing any files the agent must not modify (test harnesses, grading scripts, etc.). Glob patterns are supported (e.g., `src/tests/*.c`). Integrity is enforced by hashing these files in the Python harness — outside the container — before and after the agent runs
7. Add `sol.sh` as a reference solution script to validate task solvability (see note below)
8. Run tests to validate: `python -m pytest tests/test_data_schema.py -v`

> **Note on Solution Scripts**: Every task must have a `sol.sh` reference solution to verify solvability. If you prefer not to have your solution publicly available, submit the entire lab to the [private repository](https://github.com/sys-intelligence/syscoursebench-private) instead.
>
> **Note on Sandboxing**: Inspect AI offers multiple sandbox environments (Docker, Kubernetes, local, etc.). For simplicity, and because the majority of tasks won't require more than that, we currently expose a streamlined way to include tasks that use Docker sandboxing via `compose.yaml`. For more information regarding sandboxing and available environments in Inspect AI, see the [Sandboxing documentation](https://inspect.aisi.org.uk/sandboxing.html#environment-binding). If the lab you are adding requires a different sandboxing environment (e.g., Kubernetes), refer to the Inspect AI documentation.
>
> **Note on Complex Setup**: If the task requires complicated setup (e.g., many starter files or a complex long-running preprocessing script), package the prerequisites into a Docker image. The Dockerfile used to build the image should be hosted in our GitHub repository so it can be maintained and pushed to the benchmark's DockerHub organization.

### Reproducibility Requirements

All external dependencies must be pinned to immutable references so that tasks produce identical environments over time. These are enforced by CI (see `.github/workflows/lint-courselab.yml`).

| Dependency | Requirement | Example |
| --- | --- | --- |
| Docker images (`compose.yaml`) | Pin to SHA256 digest | `image: golang:1.21-bookworm@sha256:c6a5b9...` |
| Git repositories (`preprocess.sh`, `sol.sh`) | Checkout a specific commit after cloning | `git checkout 95318f7910...` |
| pip packages (`preprocess.sh`) | Pin to exact versions | `pip install flask==3.0.2` |
| URL downloads (`curl`/`wget`) | Include a commit hash or version, never `master`/`main` | `curl -sL https://.../<commit>/file` |
| apt packages | Do not pin versions — older packages are regularly removed from registries and will break builds | `apt-get install -y git` |

## Task Audit Agent

Use the LLM-powered audit agent to validate that `task.md` descriptions are clear, complete, and aligned with `evaluate.sh`:

```bash
cd benchmarks/courselab
# Remove stale report to avoid permission issues on re-runs
rm -f task_quality_report.md
cat task_audit_prompt.md | claude --print --model sonnet
```

This spawns a subagent per task. Results are written to `task_quality_report.md`.

## Solution Validation

We validate that tasks are solvable by running pre-defined solution scripts:

```bash
python run_solution_validation.py
```

Validation logs are kept in `courselab/validation_log/`.

This is not run in CI because some tasks are resource-intensive and long-running. Instead:

- Run it as part of PR review when adding or modifying tasks.
- We run it regularly and keep the log of the last successful run in `courselab/validation_log/`

## Best Practices

Tasks should be designed carefully and responsibly to ensure they are fair. Here are some best practices:

- Test with at least one agent: If you test with multiple agents and LLMs and no agent solves the task, it's likely the task needs revision. Review the trajectories to understand whether failures have something in common.

## Statistical Reporting

The benchmark reports standard error of the mean (SEM) alongside accuracy, to enable 95% confidence intervals (score ± 1.96 × SEM) for all reported results. Standard errors are clustered by `course_id` to account for within-course correlation (tasks in the same course share codebase, toolchain, and difficulty patterns).

### Multi-Epoch Runs

Agent-based tasks are non-deterministic (the agent's tool calls, exploration paths, and error recovery differ across runs). To measure reliability, run multiple epochs:

```bash
inspect eval courselab --model anthropic/claude-sonnet-4-6 -T epochs=3
```

With `epochs > 1`, the `mean` reducer is applied per task before aggregation — each task's score is its average pass rate across epochs (e.g., passing 2/3 times scores 0.67).

By default, `epochs=1` preserves single-run behavior. For publishable results, we recommend `epochs=3`.

## Using Custom Agents

To use a different agent, pass it to the `courselab()` function:

```python
from inspect_ai import eval
from inspect_ai.solver import basic_agent
from inspect_ai.tool import bash
from courselab import courselab

eval(
    courselab(agent=basic_agent(tools=[bash(timeout=3600)])),
    model="openai/gpt-4"
)
```

The default agent uses a 60-minute timeout per tool call. You can adjust this when using a custom agent.

See the [Inspect AI Agents documentation](https://inspect.ai-safety-institute.org.uk/agents.html) for more information.
