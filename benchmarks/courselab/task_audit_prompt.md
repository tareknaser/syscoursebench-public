# CourseLab Task Quality Validation

You are a benchmark quality reviewer for **CourseLab**, a benchmark that evaluates AI agents on systems programming lab assignments. Each task places an agent in a Docker container with a problem description (`task.md`) and grades it by running `evaluate.sh` after the agent finishes.

Read `benchmarks/courselab/README.md` for full context on the benchmark structure.

## Important Context

These tasks come from **real university courses**. The task descriptions (`task.md`) are often adapted directly from course handouts, which are intentionally underspecified in places — students (and agents) are expected to read code, explore the environment, and infer details. **This is by design and should NOT be flagged.**

What we care about is the **environment specification**: the agent must have enough information to work effectively in the Docker container. Things like knowing the working directory, which files are protected, and how evaluation works.

The agent does NOT have access to `config.json`, `evaluate.sh`, or `preprocess.sh` — it only sees `task.md` and the container filesystem.

All tasks have validated `sol.sh` reference solutions, so they are known to be solvable.

## Your Job

Validate every task under `benchmarks/courselab/data/` by checking the alignment between `task.md` and the evaluation environment. For each task, spawn a subagent that reads all task files and performs the checks below. Do NOT modify any files. This is a read-only audit.

**Only flag issues where the agent is missing critical environment information that it cannot reasonably discover on its own.** Be conservative — when in doubt, don't flag it.

## Checks to Perform

For each task, read `task.md`, `evaluate.sh`, `preprocess.sh` (if present), `config.json`, and any starter files. Then check:

### 1. Protected Files Disclosure

- Check `config.json` for `protected_files`.
- If protected files exist, verify that `task.md` warns the agent not to modify them (look for an "Environment Notes" section or similar).
- Flag ONLY if protected files exist in `config.json` but `task.md` gives NO indication whatsoever.

### 2. Working Directory Clarity

- Check that the working directory is stated or easily inferable from `task.md` (e.g., paths in examples, an "Environment Notes" section, or the compose.yaml `working_dir`).
- Flag ONLY if the agent would have no way to know where it is.

### 3. Build and Evaluation Alignment

- If `evaluate.sh` uses specific build flags (e.g., `-D_GNU_SOURCE`, `-O2`, `-std=gnu11`) that differ from what `task.md` describes, flag only if the discrepancy would cause a compilation failure or wrong behavior.
- Flag ONLY if the agent would fail evaluation due to undocumented environment requirements (not due to underspecified algorithmic requirements).

## What NOT to Flag

Do NOT flag any of the following — these are false positives:

- **Vague algorithmic requirements**: If `task.md` describes a problem loosely and the agent must figure out the approach, that's intentional course design.
- **External references**: Papers, textbook chapters, or URLs mentioned in `task.md` are fine — agents can work from the description alone.
- **Undocumented test details**: The agent doesn't need to know exactly which tests run or how many there are. It just needs to implement the described functionality.
- **Prerequisite assumptions**: If a task builds on prior labs, the preprocess script handles setup. The agent doesn't need to know the dependency chain.
- **API discovery**: If the agent must read code to learn function signatures, that's normal.
- **Performance constraints**: Timeouts and performance requirements don't need to be documented.
- **Pre-installed reference solutions**: If `preprocess.sh` installs code from prior labs, the agent can discover this by reading the filesystem.
- **Artifact completeness**: Whether `config.json` captures every file the agent creates is an internal concern, not an agent-facing issue.
- **Anti-cheating gaps**: `.git` directories, solution file access, etc. are infrastructure concerns, not task quality issues.
- **Test flakiness or retry logic**: These are internal evaluation concerns.
- **Files the agent can discover by exploring**: If `preprocess.sh` creates files the agent can find by running `ls` or `find`, that's fine.
- **Preprocess modifying protected files**: `preprocess.sh` runs before the snapshot — modifications during setup are expected.

## Severity

Only use **CRITICAL** — for issues where the agent would fail or be unfairly penalized due to missing environment information (protected files not disclosed, wrong build flags, missing working directory with no way to infer it).

Do not use WARNING or INFO levels. This is a focused check for hard blockers only.

## Output

Process tasks by spawning subagents (you may batch multiple tasks per agent). After all tasks are validated, write the report file to `benchmarks/courselab/task_quality_report.md`. Use the following structure:

```markdown
# CourseLab Task Quality Report

Generated: <date>

## Summary

| Course | Task | Critical |
|--------|------|----------|
| ...    | ...  | ...      |

**Total**: X critical findings across N tasks.

## Findings by Task

### course_id / task_name

- [Protected Files] `config.json` lists X as protected but `task.md` gives no warning.

---
(repeat for each task with findings)
```

For tasks with no findings, list them in the summary table with 0 and skip the detailed section. Most tasks should have 0 findings.
