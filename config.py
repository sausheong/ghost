import os
from collections import namedtuple

from dotenv import load_dotenv, find_dotenv


def getOpenaiProviderConfig() -> dict:
    OpenaiConfig = namedtuple(
        'OpenaiConfig',
        [
            'provider',
            'api_key',
            'model_name',
            'api_version',
            'base_url',
        ],
    )
    return OpenaiConfig(
        provider='openai',
        api_key=os.getenv('OPENAI_API_KEY'),
        model_name=os.getenv('OPENAI_MODEL'),
        api_version=os.getenv('OPENAI_API_VERSION'),
        base_url=os.getenv('OPENAI_API_BASE'),
    )


def getAzureProviderConfig() -> dict:
    AzureConfig = namedtuple(
        'AzureConfig',
        [
            'provider',
            'api_key',
            'model_name',
            'deployment_name',
            'api_version',
            'base_url',
        ],
    )
    return AzureConfig(
        provider='azure',
        api_key=os.getenv('AZURE_API_KEY'),
        model_name=os.getenv('AZURE_MODEL'),
        deployment_name=os.getenv('AZURE_DEPLOYMENT_NAME'),
        api_version=os.getenv('AZURE_API_VERSION'),
        base_url=os.getenv('AZURE_API_BASE'),
    )


def getPalmProviderConfig() -> dict:
    PalmConfig = namedtuple(
        'PalmConfig',
        [
            'provider',
            'model_name',
            'location',
        ]
    )
    return PalmConfig(
        provider='palm',
        model_name=os.getenv('PALM_MODEL') or 'chat-bison',
        location=os.getenv('PALM_LOCATION') or 'us-central1',
    )


def getProviderConfig(provider_name: str) -> dict:
    supported_providers = ('palm', 'azure', 'openai')

    if not isinstance(provider_name, str):
        raise TypeError("Input must be a string.")

    if provider_name not in supported_providers:
        raise ValueError(
            f"Invalid input. Supported providers: {supported_providers}.")

    match provider_name:
        case "openai":
            return getOpenaiProviderConfig()
        case "azure":
            return getAzureProviderConfig()
        case "palm":
            return getPalmProviderConfig()


# Get configurations
load_dotenv(find_dotenv())
specs_file = os.getenv('SPECS') or 'specs.md'  # defaults to specs.md
output_file = os.getenv('OUTPUT_FILE') or 'output.md'  # defaults to output.md
retries = int(os.getenv('MAX_RETRIES', 3) or 3)  # defaults to 3
provider = os.getenv('PROVIDER') or 'openai'  # defaults to openai
provider_config = getProviderConfig(provider_name=provider)
