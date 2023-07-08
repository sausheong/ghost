import sys

from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import AzureChatOpenAI, ChatVertexAI, ChatOpenAI
from langchain.llms import OpenAI, AzureOpenAI, VertexAI

from tools import get_tools
from config import specs_file, retries, provider
from config import provider_config as cfg


class Agent:
    agent = None
    llm = None

    # initialise the agent
    def __init__(self):
        print("\033[96mInitialising Ghost with the following specifications:\033[0m")

        self.empty()
        llm = None

        # read the specifications from file
        specs = ""
        with open(specs_file, 'r') as file:
            specs = file.read()
        print(specs, "\nlength:", len(specs), "words")
        print(f"\033[96mUsing {cfg.provider} \033[0m")

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

        if llm is None:
            sys.exit("No valid LLM configured:" + provider)

        self.llm = llm

        print(f"\033[96mWith {self.llm.model_name}\033[0m")

        FORMAT_INSTRUCTIONS = """Do not put any quotes in output response and To use a tool, please use the following format:

        \```
        Thought: Do I need to use a tool? Yes
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        \```

        When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the following format(the prefix of "Thought: " and "{ai_prefix}: " are must be included):

        \```
        Thought: Do I need to use a tool? No
        {ai_prefix}: [your response here]
        \```
        do not create any triplet quotes single or double in the output,only create ASCII characters in output and no comments required
        """

        # initialise agent execute
        self.agent = initialize_agent(
            get_tools(),
            self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=ConversationBufferMemory(
                memory_key="chat_history", return_messages=True),
            agent_kwargs={"format_instructions": FORMAT_INSTRUCTIONS},
            handle_parsing_errors="Check the output and correct it to make it conform.",
            verbose=True)

        self.agent.run(specs)

    def run(self, data):
        return self.agent.run(data)

    def empty(self):
        self.agent = None
        self.llm = None

    def reset(self):
        print("\033[96mReset agent has been triggered\033[0m")
        self.__init__()
