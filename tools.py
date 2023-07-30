from langchain.utilities import PythonREPL
from langchain.tools import ShellTool
from langchain.tools import DuckDuckGoSearchRun
from langchain.tools import AIPluginTool
from langchain.agents import Tool, load_tools

from langchain.document_loaders import UnstructuredFileLoader
from models import get_provider_model

from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.agents import create_csv_agent
from langchain.agents.agent_types import AgentType
from langchain import SQLDatabase, SQLDatabaseChain

from langchain.utilities import SerpAPIWrapper

from config import tools_config

# Initialize empty list of tools
tools_list = []

# Ask a document


def ask_document(str):
    doc, query = str.split(",")
    loader = UnstructuredFileLoader(doc)
    documents = loader.load()
    llm, embeddings = get_provider_model()
    text_splitter = CharacterTextSplitter(chunk_size=2048, chunk_overlap=0)
    documents = text_splitter.split_documents(documents)
    vectorstore = Chroma.from_documents(documents, embeddings)
    qa = RetrievalQA.from_chain_type(
        llm=llm, chain_type="map_reduce", retriever=vectorstore.as_retriever())
    results = qa.run(query)
    return results


ask_document_tool = Tool(
    name="ask_document",
    description="Asks queries about a given document. Can take in multiple document \
        types including PDF, text, Word and so on except CSV files. The input to this \
        tool should be a comma separated list of length two. The first string in the \
        list is the file path for the document you want  you want query and the second \
        is the query itself. For example, `dir/attention.pdf,What is the summary of \
        the document?` would be the input if you wanted to query the dir/attention.pdf file.",
    func=ask_document)
tools_list.append(ask_document_tool)

# Ask a CSV file


def ask_csv(str):
    doc, query = str.split(",")
    llm, _ = get_provider_model()
    agent = create_csv_agent(
        llm,
        doc,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )
    results = agent.run(query)
    return results


ask_csv_tool = Tool(
    name="ask_csv",
    description="Asks queries about a given csv file. The input to this tool \
        should be a comma separated list of length two. The first string in \
        the list is the file path for the csv file you want  you want query \
        and the second is the query itself. For example, `dir/data.csv,How many \
        rows are there in the csv?` would be the input if you wanted to query \
        the dir/data.csv file.",
    func=ask_csv)
tools_list.append(ask_csv_tool)

# Ask a relational database


def ask_db(str):
    uri, query = str.split("|")
    llm, _ = get_provider_model()
    db = SQLDatabase.from_uri(uri)
    llm, _ = get_provider_model()
    db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
    results = db_chain.run(query)
    return results


ask_db_tool = Tool(
    name="ask_db",
    description="Asks queries about a given database. The input to this tool \
        should be a vertical bar (|) separated list of length two. The first \
        string in the uri of the database you want  you want query and the \
        second is the query itself. For example, \
        `postgresql://u:pwd@db.server.com:5432/dbase|How many rows are there \
        in the users table?` would be the input if you wanted to query the \
        postgresql://u:pwd@db.server.com:5432/dbase database.",
    func=ask_db)
tools_list.append(ask_db_tool)

# Python REPL
repl_tool = Tool(
    name="python_repl",
    description="A Python shell. Use this to execute python commands \
        only when explicitly asked to. Input should be a valid python \
        command. If you want to see the output of a value, you should \
        print it ut with `print(...)`.",
    func=PythonREPL().run)
tools_list.append(repl_tool)

# shell
shell_tool = ShellTool()
tools_list.append(shell_tool)

# DuckDuckGo search
search_tool = DuckDuckGoSearchRun()
tools_list.append(search_tool)

# Image search using Google Images, through SerpAPI, you need to have an API key from https://serpapi.com
if (cfg := tools_config['serpapi']) is not None:
    params = {
        "engine": "google_images",
    }
    image_search = SerpAPIWrapper(
        params=params,
        serpapi_api_key=cfg.serpapi_api_key,
    )
    image_search_tool = Tool(
        name="image_search_tool",
        description="An image search tool based on SerpAPI, using Google images. Use this to search for images.",
        func=image_search.run,
    )
    tools_list.append(image_search_tool)


def get_tools():
    return tools_list + load_tools(["requests_all"])
