#!/usr/bin/env python3
"""Run evaluation on using Claude Code agent."""

from courselab import courselab
from inspect_ai import eval
from inspect_swe import claude_code

MODEL = 'anthropic/claude-sonnet-4-5'
MAX_TURNS = 150
EPOCHS = 3
LIMIT = None
TASK_IDS = None
SYSTEM_PROMPT = (
    'You are solving a systems programming lab assignment. Read the task description carefully and follow the instructions precisely.'
)
DISALLOWED_TOOLS = [
    'WebFetch',
    'WebSearch',
]
CLAUDE_CODE_ENV = {
    'BASH_DEFAULT_TIMEOUT_MS': '3600000'
}


if __name__ == '__main__':
    eval(
        tasks=courselab(
            task_ids=TASK_IDS,
            max_turns=MAX_TURNS,
            epochs=EPOCHS,
            agent=claude_code(
                system_prompt=SYSTEM_PROMPT,
                disallowed_tools=DISALLOWED_TOOLS,
                env=CLAUDE_CODE_ENV,
                version='stable',
            ),
        ),
        model=MODEL,
        limit=LIMIT,
    )
