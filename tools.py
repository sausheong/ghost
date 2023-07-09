from langchain.utilities import PythonREPL
from langchain.tools import ShellTool
from langchain.tools import DuckDuckGoSearchRun
from langchain.tools import AIPluginTool
from langchain.agents import Tool, load_tools

from langchain.document_loaders import UnstructuredFileLoader
from langchain.chains.question_answering import load_qa_chain
from models import get_provider_model

from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA

def ask_document(str):
    """ Asks queries about a given document. Can take in multiple document types including PDF, text, Word, images and so on """
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
        including PDF, text, Word and so on. The input to this tool should be a comma separated \
        list of length two. The first string in the list is the file path for the document you \
        want  you want query and the second is the query itself. \
        For example, `dir/attention.pdf,What is the summary of the document?` would be the input \
        if you wanted to query the dir/attention.pdf file.",
    func=ask_document)


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
        ask_document_tool
        # carpark_tool
    ] + load_tools(["requests_all"])