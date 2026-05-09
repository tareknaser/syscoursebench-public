#!/usr/bin/env python3

from inspect_ai import eval

from sysexam.sysexam import sysexam

MODELS = [
    'anthropic/claude-opus-4-6',
    'anthropic/claude-sonnet-4-6',
    'anthropic/claude-haiku-4-5'
]
JUDGE_MODEL = 'anthropic/claude-haiku-4-5'
LIMIT = None
EXAM_IDS = None
QUESTION_TYPES = None
TAGS = None

if __name__ == "__main__":
    task = sysexam(
        exam_ids=EXAM_IDS,
        question_types=QUESTION_TYPES,
        tags=TAGS,
        judge_model=JUDGE_MODEL,
    )

    eval(tasks=task, model=MODELS, limit=LIMIT)
