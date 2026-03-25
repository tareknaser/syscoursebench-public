import hashlib
from pathlib import Path

from inspect_ai.scorer import Score, Scorer, Target, accuracy, scorer, stderr
from inspect_ai.solver import TaskState
from inspect_ai.util import sandbox


@scorer(metrics=[accuracy(), stderr(cluster="course_id")])
def lab_scorer() -> Scorer:
    async def score(state: TaskState, target: Target) -> Score:
        # Verify protected files are unchanged (hashes stored outside container)
        original_hashes = state.store.get("protected_file_hashes", {})
        if original_hashes:
            violations = []
            for path, expected_hash in original_hashes.items():
                try:
                    content = await sandbox().read_file(path, text=False)
                    actual_hash = hashlib.sha256(content).hexdigest()
                    if actual_hash != expected_hash:
                        violations.append(f"MODIFIED: {path}")
                except FileNotFoundError:
                    violations.append(f"DELETED: {path}")

            if violations:
                return Score(
                    value="I",
                    answer="FAIL",
                    explanation="Protected files were tampered with:\n"
                    + "\n".join(violations),
                )

        task_folder = Path(state.metadata["task_folder"])
        evaluate_script = (task_folder / "evaluate.sh").read_text()

        await sandbox().write_file("evaluate.sh", evaluate_script)
        await sandbox().exec(["chmod", "+x", "evaluate.sh"])

        try:
            result = await sandbox().exec(['bash', 'evaluate.sh'], timeout=3600)
        except TimeoutError:
            return Score(
                value='I',
                answer='FAIL',
                explanation='evaluate.sh timed out after 3600 seconds',
            )

        artifacts = {}
        artifact_patterns = state.metadata.get("artifacts", [])
        if artifact_patterns:
            for pattern in artifact_patterns:
                glob_result = await sandbox().exec(
                    ["bash", "-c", f"ls {pattern} 2>/dev/null || true"]
                )
                if glob_result.success and glob_result.stdout.strip():
                    for file_path in glob_result.stdout.strip().split("\n"):
                        try:
                            content = await sandbox().read_file(file_path)
                            artifacts[file_path] = content
                        except Exception as e:
                            artifacts[file_path] = f"Error reading file: {str(e)}"

        if result.success:
            return Score(
                value="C",
                answer="PASS",
                explanation=result.stdout,
                metadata={"artifacts": artifacts} if artifacts else None,
            )
        else:
            return Score(
                value="I",
                answer="FAIL",
                explanation=result.stderr or result.stdout,
                metadata={"artifacts": artifacts} if artifacts else None,
            )

    return score
