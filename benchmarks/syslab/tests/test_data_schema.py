import json
from pathlib import Path
import pytest

DATA_DIR = Path(__file__).parent.parent / "data"
VALID_CATEGORIES = {
    "Intro to Systems",
    "Operating Systems",
    "Distributed Systems",
    "Database Systems",
}


def get_task_folders(data_dir: Path) -> list[Path]:
    task_folders = []
    for config_path in data_dir.rglob("config.json"):
        if config_path.name == "courses.json":
            continue
        task_folders.append(config_path.parent)
    return task_folders


class TestTaskStructure:
    def test_data_dir_exists(self):
        assert DATA_DIR.exists(), f"Data directory not found: {DATA_DIR}"

    def test_tasks_found(self):
        task_folders = get_task_folders(DATA_DIR)
        assert len(task_folders) > 0, "No tasks found in data directory"

    def test_required_files_exist(self):
        task_folders = get_task_folders(DATA_DIR)
        required_files = ['config.json', 'task.md', 'compose.yaml', 'evaluate.sh', 'sol.sh']

        for task_folder in task_folders:
            for filename in required_files:
                file_path = task_folder / filename
                assert file_path.exists(), f"{task_folder.name} missing {filename}"

    def test_config_valid_json(self):
        task_folders = get_task_folders(DATA_DIR)

        for task_folder in task_folders:
            config_path = task_folder / "config.json"
            with config_path.open("r") as f:
                config = json.load(f)
            assert isinstance(
                config, dict
            ), f"{task_folder.name}: config.json must be object"

    def test_config_required_fields(self):
        task_folders = get_task_folders(DATA_DIR)
        required_fields = ["instance_id", "course_id", "timeout_minutes"]

        for task_folder in task_folders:
            config_path = task_folder / "config.json"
            with config_path.open("r") as f:
                config = json.load(f)

            for field in required_fields:
                assert field in config, f"{task_folder.name}: missing {field}"

            assert isinstance(
                config["instance_id"], str
            ), f"{task_folder.name}: instance_id must be string"
            assert isinstance(
                config["course_id"], str
            ), f"{task_folder.name}: course_id must be string"
            assert isinstance(
                config["timeout_minutes"], (int, float)
            ), f"{task_folder.name}: timeout_minutes must be number"
            assert (
                config["timeout_minutes"] > 0
            ), f"{task_folder.name}: timeout_minutes must be positive"

    def test_config_optional_fields(self):
        task_folders = get_task_folders(DATA_DIR)

        for task_folder in task_folders:
            config_path = task_folder / "config.json"
            with config_path.open("r") as f:
                config = json.load(f)

            if "artifacts" in config:
                assert isinstance(
                    config["artifacts"], list
                ), f"{task_folder.name}: artifacts must be list"
                for artifact in config["artifacts"]:
                    assert isinstance(
                        artifact, str
                    ), f"{task_folder.name}: each artifact must be string"

            if "protected_files" in config:
                assert isinstance(
                    config["protected_files"], list
                ), f"{task_folder.name}: protected_files must be list"
                for pf in config["protected_files"]:
                    assert isinstance(
                        pf, str
                    ), f"{task_folder.name}: each protected_file must be string"

    def test_instance_ids_unique(self):
        task_folders = get_task_folders(DATA_DIR)
        instance_ids = []

        for task_folder in task_folders:
            config_path = task_folder / "config.json"
            with config_path.open("r") as f:
                config = json.load(f)
            instance_ids.append(config["instance_id"])

        assert len(instance_ids) == len(
            set(instance_ids)
        ), "Duplicate instance_ids found"

    def test_instance_id_format(self):
        task_folders = get_task_folders(DATA_DIR)

        for task_folder in task_folders:
            config_path = task_folder / "config.json"
            with config_path.open("r") as f:
                config = json.load(f)

            instance_id = config["instance_id"]
            course_id = config["course_id"]
            folder_name = task_folder.name
            expected_id = f"{course_id}__{folder_name}"
            assert instance_id == expected_id, (
                f"{folder_name}: instance_id must be "
                f"'{{course_id}}__{{folder_name}}', "
                f"expected '{expected_id}' but got '{instance_id}'"
            )

    def test_courses_json_exists(self):
        courses_path = DATA_DIR / "courses.json"
        assert courses_path.exists(), "courses.json not found in data directory"

    def test_courses_json_valid(self):
        courses_path = DATA_DIR / "courses.json"
        with courses_path.open("r") as f:
            courses = json.load(f)

        assert "courses" in courses, "courses.json must have 'courses' key"
        assert isinstance(courses["courses"], list), "'courses' must be a list"

        for course in courses["courses"]:
            assert isinstance(course, dict), "each course must be an object"
            assert "course_id" in course, "each course must have course_id"
            assert "category" in course, (
                f"course '{course.get('course_id', '?')}' must have category"
            )
            assert course["category"] in VALID_CATEGORIES, (
                f"course '{course['course_id']}': category '{course['category']}' "
                f"must be one of {VALID_CATEGORIES}"
            )
            assert "num_tasks" in course, "each course must have num_tasks"

    def test_course_id_in_courses_json(self):
        courses_path = DATA_DIR / "courses.json"
        with courses_path.open("r") as f:
            courses_data = json.load(f)

        valid_course_ids = {
            course["course_id"] for course in courses_data["courses"]
        }
        task_folders = get_task_folders(DATA_DIR)

        for task_folder in task_folders:
            config_path = task_folder / "config.json"
            with config_path.open("r") as f:
                config = json.load(f)

            course_id = config["course_id"]
            assert course_id in valid_course_ids, (
                f"{task_folder.name}: course_id '{course_id}' not found in courses.json"
            )

    def test_starter_files_exist(self):
        task_folders = get_task_folders(DATA_DIR)

        for task_folder in task_folders:
            starter_dir = task_folder / "starter"
            if starter_dir.exists():
                assert (
                    starter_dir.is_dir()
                ), f"{task_folder.name}: starter must be a directory"
                files = list(starter_dir.rglob("*"))
                assert len(files) > 0, f"{task_folder.name}: starter directory is empty"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
