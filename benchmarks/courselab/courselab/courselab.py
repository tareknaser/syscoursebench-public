from importlib.metadata import version
from pathlib import Path

from inspect_ai import Epochs, Task, task
from inspect_ai.agent import Agent
from inspect_ai.solver import Solver

from courselab.dataset import load_dataset, load_courses_metadata
from courselab.scorer import lab_scorer
from courselab.solver import lab_agent, snapshot_protected_files


@task
def courselab(
    task_dir: Path | str | None = None,
    task_ids: str | list[str] | None = None,
    agent: Agent | Solver | None = None,
    max_turns: int = 30,
    epochs: int = 1,
) -> Task:
    dataset = load_dataset(task_dir=task_dir, task_ids=task_ids)
    metadata = load_courses_metadata(data_dir=Path(task_dir) if task_dir else None)

    return Task(
        dataset=dataset,
        solver=[snapshot_protected_files(), agent or lab_agent()],
        scorer=lab_scorer(),
        max_messages=max_turns,
        epochs=Epochs(epochs, "mean") if epochs > 1 else None,
        metadata={
            "num_courses": len(metadata["courses"]),
            "courses": metadata["courses"],
        },
        name="courselab",
        version=version("courselab-bench"),
    )
