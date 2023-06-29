from langchain.utilities import PythonREPL
from langchain.tools import ShellTool
from langchain.tools import DuckDuckGoSearchRun
from langchain.tools import AIPluginTool
from langchain.agents import Tool, load_tools


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
        wolfram_tool,
        askpdf_tool,
        shell_tool,
        search_tool,
        carpark_tool
    ] + load_tools(["requests_all"])