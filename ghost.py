import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv, find_dotenv
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
from tools import get_tools
from langchain.chat_models import AzureChatOpenAI, ChatVertexAI, ChatOpenAI
from langchain.llms import OpenAI, AzureOpenAI
from waitress import serve
import webbrowser

# get configurations
load_dotenv(find_dotenv())
specs_file = os.getenv('SPECS')
model = os.getenv('MODEL')

# get path for static files
static_dir = os.path.join(os.path.dirname(__file__), 'static')  
if not os.path.exists(static_dir): 
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

# initialise the agent
def initAgent():
    print("\033[96mInitialising Ghost with the following specifications:\033[0m")
    # read the specifications from file
    specs = ""
    with open(specs_file, 'r') as file:
        specs = file.read()
    print(specs, "\nlength:", len(specs), "words")

    print(f"\033[96mUsing {model}\033[0m")

    # OpenAI
    if model == "openai":
        api_key  = os.getenv('OPENAI_API_KEY')
        model_name = os.getenv('OPENAI_MODEL')
        api_version = os.getenv('OPENAI_API_VERSION')
        base_url = os.getenv('OPENAI_API_BASE')        

        if model_name.startswith("gpt-4") or model.startswith("gpt-3.5"):
            llm = ChatOpenAI(
                temperature=0.0,
                model_name=model_name,
                openai_api_key=api_key,
            )      
        else:
            llm = OpenAI(
                temperature=0.0,
                model_name=model_name,
                openai_api_key=api_key,
            )      


    # Azure OpenAI
    if model == "azure":
        api_key  = os.getenv('AZURE_API_KEY')
        model_name = os.getenv('AZURE_MODEL')
        deployment_name = os.getenv('AZURE_DEPLOYMENT_NAME')
        api_version = os.getenv('AZURE_API_VERSION')
        base_url = os.getenv('AZURE_API_BASE')
        
        if model_name.startswith("gpt-4") or model.startswith("gpt-3.5"):
            llm = AzureChatOpenAI(
                temperature=0.0,
                openai_api_base=base_url,
                openai_api_version=api_version,
                model_name=model_name,
                deployment_name=deployment_name,
                openai_api_key=api_key,
                openai_api_type = "azure",
            )   
        else:
            llm = AzureOpenAI(
                temperature=0.6,
                openai_api_base=base_url,
                openai_api_version=api_version,
                model_name=model_name,
                deployment_name=deployment_name,
                openai_api_key=api_key,
                openai_api_type = "azure",
            )   

    # Google Vertex AI (PaLM)
    if model == "palm":
        llm = ChatVertexAI(
            temperature=0.0,
            model_name=os.getenv('PALM_MODEL'),
        )

    # initialise agent execut
    agent = initialize_agent(
        get_tools(), 
        llm, 
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,         
        memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True),
        handle_parsing_errors="Check your output and make sure it conforms.",
        verbose=True)

    agent.run(specs)
    return agent

# start server
print("\033[96mStarting Ghost at http://127.0.0.1:1337\033[0m")
ghost = Flask(__name__, static_folder=static_dir, template_folder=static_dir)
agent = initAgent()

# server landing page
@ghost.route('/')
def landing():
    return render_template('index.html')

# run
@ghost.route('/run', methods=['POST'])
def run():
    data = request.json
    response = agent.run(data['input'])    
    return jsonify({'input': data['input'],
                    'response': response})

if __name__ == '__main__':
    print("\033[93mGhost started. Press CTRL+C to quit.\033[0m")
    webbrowser.open("http://127.0.0.1:1337")
    serve(ghost, host='127.0.0.1', port=1337)


