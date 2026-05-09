#!/usr/bin/env python3
import os

from azure.identity import AzureCliCredential, get_bearer_token_provider
from inspect_ai import eval
import inspect_ai.model._providers.openai as _openai_provider
import inspect_ai.model._providers.util as _providers_util
import inspect_ai.model._providers.util.azure_hosting as _azure_hosting

from sysexam.sysexam import sysexam

TRAPI_APIPATH = os.environ.get('TRAPI_APIPATH', 'redmond/interactive')
TRAPI_API_VERSION = os.environ.get('TRAPI_API_VERSION', '2025-04-01-preview')
TRAPI_ENDPOINT = os.environ.get('TRAPI_ENDPOINT', f'https://trapi.research.microsoft.com/{TRAPI_APIPATH}')
TRAPI_SCOPE = os.environ.get('TRAPI_SCOPE', 'api://trapi/.default')

TRAPI_MODELS = [
    'gpt-5.2_2025-12-11',
    'gpt-5-mini_2025-08-07',
]

MODELS = [
    'anthropic/claude-sonnet-4-6',
    'anthropic/claude-haiku-4-5',
]

TRAPI_JUDGE_MODEL = 'gpt-5.2_2025-12-11'

LIMIT = None
EXAM_IDS = None
QUESTION_TYPES = None
TAGS = None


os.environ['AZUREAI_OPENAI_BASE_URL'] = TRAPI_ENDPOINT
os.environ['AZUREAI_OPENAI_API_VERSION'] = TRAPI_API_VERSION
os.environ['AZUREAI_AUDIENCE'] = TRAPI_SCOPE
os.environ.pop('AZUREAI_OPENAI_API_KEY', None)
os.environ.pop('AZURE_OPENAI_API_KEY', None)

# Patch inspect-ai's Azure token resolver to use AzureCliCredential.
# DefaultAzureCredential picks ManagedIdentityCredential first on this host,
# which returns a token that TRAPI rejects (403). AzureCliCredential works.
def _trapi_token_provider(provider_name):
    return get_bearer_token_provider(AzureCliCredential(), TRAPI_SCOPE)

_azure_hosting.resolve_azure_token_provider = _trapi_token_provider
_providers_util.resolve_azure_token_provider = _trapi_token_provider
_openai_provider.resolve_azure_token_provider = _trapi_token_provider

if __name__ == '__main__':
    judge_model = f'openai/azure/{TRAPI_JUDGE_MODEL}'
    trapi_models = [f'openai/azure/{m}' for m in TRAPI_MODELS]
    all_models = trapi_models + MODELS

    task = sysexam(
        exam_ids=EXAM_IDS,
        question_types=QUESTION_TYPES,
        tags=TAGS,
        judge_model=judge_model,
    )
    eval(tasks=task, model=all_models, limit=LIMIT, fail_on_error=False)
