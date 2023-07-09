import sys

from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType

from models import get_provider_model
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

        llm,_ = get_provider_model()

        if llm is None:
            sys.exit("No valid LLM configured:" + provider)

        self.llm = llm

        print(f"\033[96mWith {self.llm.model_name}\033[0m")

        # initialise agent execute
        self.agent = initialize_agent(
            get_tools(),
            self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=ConversationBufferMemory(
                memory_key="chat_history", return_messages=True),
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
