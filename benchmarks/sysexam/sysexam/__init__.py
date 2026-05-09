from importlib.metadata import version

from .sysexam import sysexam
from .dataset import load_dataset, load_exam_metadata
from .metrics import (
    points_accuracy,
    total_points_earned,
    total_points_possible,
)
from .scorer import exam_scorer

__all__ = [
    "sysexam",
    "load_dataset",
    "load_exam_metadata",
    "exam_scorer",
    "points_accuracy",
    "total_points_earned",
    "total_points_possible",
]

__version__ = version("sysexam-bench")
