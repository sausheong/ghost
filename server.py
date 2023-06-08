import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv, find_dotenv
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.utilities import PythonREPL
from langchain.tools import ShellTool
from langchain.tools import DuckDuckGoSearchRun
from langchain.chat_models import AzureChatOpenAI

# get configurations
load_dotenv(find_dotenv())
api_key  = os.getenv('OPENAI_API_KEY')
specs_file = os.getenv('SPECS')
model = os.getenv('LLM_MODEL')
api_version = os.getenv('OPENAI_API_VERSION')
base_url = os.getenv('OPENAI_API_BASE')

# get path for static files
static_dir = os.path.join(os.path.dirname(__file__), 'static')  
if not os.path.exists(static_dir): 
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

# initialise the agent
def initAgent():
    # read the specifications from file
    specs = ""
    with open(specs_file, 'r') as file:
        specs = file.read()

    python_repl = PythonREPL()
    repl_tool = Tool(
        name="python_repl",
        description="A Python shell. Use this to execute python commands. \
            Input should be a valid python command. If you want to see the \
            output of a value, you should print it ut with `print(...)`.",
        func=python_repl.run
    )
    shell_tool = ShellTool()
    search = DuckDuckGoSearchRun()
    tools = [repl_tool, shell_tool, search]

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    llm = AzureChatOpenAI(
        temperature=0.0,
        max_tokens=8192-len(specs),
        openai_api_base=base_url,
        openai_api_version=api_version,
        deployment_name=model,
        openai_api_key=api_key,
        openai_api_type = "azure",
    )    

    agent = initialize_agent(
        tools, 
        llm, 
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, 
        verbose=True, 
        memory=memory,
        handle_parsing_errors="Check your output and make sure it conforms!")

    agent.run(specs)
    return agent

# start server
server = Flask(__name__, static_folder=static_dir, template_folder=static_dir)
agent = initAgent()

# server landing page
@server.route('/')
def landing():
    return render_template('index.html')

# run the promptscript
@server.route('/run', methods=['POST'])
def run():
    data = request.json
    response = agent.run(data['input'])    
    return jsonify({'input': data['input'],
                    'response': response})

if __name__ == '__main__':
    # start server
    server.run("127.0.0.1", 1337, debug=False)
    

