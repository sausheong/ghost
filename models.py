from langchain.chat_models import AzureChatOpenAI, ChatVertexAI, ChatOpenAI
from langchain.llms import OpenAI, AzureOpenAI, VertexAI
from langchain.embeddings import OpenAIEmbeddings, VertexAIEmbeddings
from config import retries
from config import provider_config as cfg


def get_provider_model():
    llm = None
    # OpenAI
    if cfg.provider == "openai":
        if cfg.model_name.startswith("gpt-4") or cfg.model_name.startswith("gpt-3.5"):
            llm = ChatOpenAI(
                temperature=0.7,
                model_name=cfg.model_name,
                openai_api_key=cfg.api_key,
                max_retries=retries,
            )
        else:
            llm = OpenAI(
                temperature=0.7,
                model_name=cfg.model_name,
                openai_api_key=cfg.api_key,
                max_retries=retries,
            )
        embeddings = OpenAIEmbeddings(
            openai_api_key=cfg.api_key,
        )

    # Azure OpenAI
    if cfg.provider == "azure":
        if cfg.model_name.startswith("gpt-4") or cfg.model_name.startswith("gpt-3.5"):
            llm = AzureChatOpenAI(
                temperature=0.7,
                openai_api_base=cfg.base_url,
                openai_api_version=cfg.api_version,
                model_name=cfg.model_name,
                deployment_name=cfg.deployment_name,
                openai_api_key=cfg.api_key,
                max_retries=retries,
                openai_api_type="azure",
            )
        else:
            llm = AzureOpenAI(
                temperature=0.7,
                openai_api_base=cfg.base_url,
                openai_api_version=cfg.api_version,
                model_name=cfg.model_name,
                deployment_name=cfg.deployment_name,
                openai_api_key=cfg.api_key,
                max_retries=retries,
                openai_api_type="azure",
            )
        embeddings = OpenAIEmbeddings(
            openai_api_key=cfg.api_key,
        )

    # Google Vertex AI (PaLM)
    if cfg.provider == "palm":
        if cfg.model_name == "chat-bison" or cfg.model_name == "codechat-bison":
            llm = ChatVertexAI(
                temperature=0.7,
                model_name=cfg.model_name,
                location=cfg.location,
                max_output_tokens=1024,
            )
        else:
            llm = VertexAI(
                temperature=0.7,
                model_name=cfg.model_name,
                location=cfg.location,
                max_output_tokens=1024,
            )
        embeddings = VertexAIEmbeddings()
    return llm, embeddings
