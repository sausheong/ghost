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

def ask_document(str):
    """ Asks queries about a given document. Can take in multiple document types including PDF, text, Word, images  and so on except CSV files"""
    doc, query = str.split(",")
    loader = UnstructuredFileLoader(doc)
    documents = loader.load()
    llm, embeddings = get_provider_model()
    text_splitter = CharacterTextSplitter(chunk_size=2048, chunk_overlap=0)
    documents = text_splitter.split_documents(documents)
    vectorstore = Chroma.from_documents(documents, embeddings)
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="map_reduce", retriever=vectorstore.as_retriever())
    results=qa.run(query)
    return results

ask_document_tool = Tool(
    name="ask_document",
    description="Asks queries about a given document. Can take in multiple document types \
        including PDF, text, Word and so on except CSV files. The input to this tool should be a comma separated \
        list of length two. The first string in the list is the file path for the document you \
        want  you want query and the second is the query itself. \
        For example, `dir/attention.pdf,What is the summary of the document?` would be the input \
        if you wanted to query the dir/attention.pdf file.",
    func=ask_document)

def ask_csv(str):
    """ Asks queries about a given csv file. """
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
    description="Asks queries about a given csv file. The input to this tool should be a comma separated \
        list of length two. The first string in the list is the file path for the csv file you \
        want  you want query and the second is the query itself. \
        For example, `dir/data.csv,How many rows are there in the csv?` would be the input \
        if you wanted to query the dir/data.csv file.",
    func=ask_csv)    

def ask_db(str):
    """ Asks queries about a given database. """
    uri, query = str.split("|")
    llm, _ = get_provider_model()
    db = SQLDatabase.from_uri(uri)
    llm, _ = get_provider_model()
    db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
    results = db_chain.run(query)
    return results

ask_db_tool = Tool(
    name="ask_db",
    description="Asks queries about a given database. The input to this tool should be a vertical bar (|) separated \
        list of length two. The first string in the uri of the database you \
        want  you want query and the second is the query itself. \
        For example, `postgresql://u:pwd@db.server.com:5432/dbase|How many rows are there in the users table?` would be the input \
        if you wanted to query the postgresql://u:pwd@db.server.com:5432/dbase database.",
    func=ask_db)    





def get_tools():
    # Python REPL
    repl_tool = Tool(
        name="python_repl",
        description="A Python shell. Use this to execute python commands \
            only when explicitly asked to. Input should be a valid python \
            command. If you want to see the output of a value, you should \
            print it ut with `print(...)`.",
        func=PythonREPL().run)
    # ChatGPT Plugin - Wolfram Alpha
    wolfram = AIPluginTool.from_plugin_url("https://www.wolframalpha.com/.well-known/ai-plugin.json")
    wolfram_tool = Tool(
        name="wolfram_tool",
        description=wolfram.description,
        func=wolfram.run)
    # ChatGPT Plugin - AskPDF
    askpdf = AIPluginTool.from_plugin_url("https://plugin.askyourpdf.com/.well-known/ai-plugin.json")
    askpdf_tool = Tool(
        name="askpdf_tool",
        description=askpdf.description,
        func=askpdf.run)
    carpark = AIPluginTool.from_plugin_url("https://carpark.sausheong.com/.well-known/ai-plugin.json")
    carpark_tool = Tool(
        name="carpark_tool",
        description=carpark.description,
        func=carpark.run)

    # shell
    shell_tool = ShellTool()
    # DuckDuckGo search
    search_tool = DuckDuckGoSearchRun()

    return [
        repl_tool,
        # wolfram_tool,
        # askpdf_tool,
        shell_tool,
        search_tool,
        ask_document_tool,
        ask_csv_tool,
        ask_db_tool
        # carpark_tool
    ] + load_tools(["requests_all"])