# Ghost

Now you see it. Now you don't.

Ghost is a small footprint UI for interacting with online LLMs including OpenAI, Azure OpenAI and Google Vertex AI. It is meant as an interface for developers and everything is minimal and can be changed easily to suit your personal needs.

ghost is written using Langchain and has configured the following tools:
1. Python REPL Tool
2. Shell Tool
3. DuckDuckSearch Tool

It is fully customisable and extensible.

## Setup

After you have clone the repo, rename the `.env.example` file to `.env` and provide the necessary API key and other information from your provider.

Then set up the packages needed to run Ghost with pip.

```
$ pip install -r requirements.txt
```

You can consider setting up its own environment using Conda or pyenv or any of these similar tools.

Then you can run the app by doing this at the command line:

```
$ python ghost.py
```

## Ghost specifications

You can change how Ghost behaves by changing `specs.md` or pointing the specs to a different file in the `.env` file. The specifications determine how Ghost will react to your prompts.