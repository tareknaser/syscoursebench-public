#!/usr/bin/env python3
"""Run evaluation on using bash only agent."""

from syslab import syslab
from inspect_ai import eval

MODELS = [
    'anthropic/claude-sonnet-4-6',
    'anthropic/claude-haiku-4-5'
]
MAX_TURNS = 200
EPOCHS = 3
LIMIT = None
TASK_IDS = None

if __name__ == '__main__':
    eval(
        tasks=syslab(task_ids=TASK_IDS, max_turns=MAX_TURNS, epochs=EPOCHS),
        model=MODELS,
        limit=LIMIT,
        fail_on_error=False,
    )
