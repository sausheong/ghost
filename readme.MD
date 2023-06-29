# Ghost

[![Ghost AI code assistant that runs on your laptop](https://img.youtube.com/vi/AkfAONksQoA/0.jpg)](https://youtu.be/AkfAONksQoA)

Ghost AI code assistant that runs on your laptop

[![Ghost refactoring itself!](https://img.youtube.com/vi/6aOzgnDGBfo/0.jpg)](https://youtu.be/6aOzgnDGBfo)

Ghost refactoring itself!

[![Ghost searching on the Internet](https://img.youtube.com/vi/hCVyqrrqH7E/0.jpg)](https://youtu.be/hCVyqrrqH7E)

Ghost searching on the Internet

Ghost is a small footprint AI assistant, built to run locally in your computer. It is meant as an interface for developers and everything is minimal and can be changed easily to suit your personal needs.

ghost is written using Langchain and has configured the following tools by default:
1. Python REPL Tool
2. Shell Tool
3. DuckDuckSearch Tool
4. Requests tool

It is also configured for several ChatGPT Plugins. Please check the `tools.py` file for more details.

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

## Google VertexAI

Ghost can also work with Google Cloud Platform (GCP) Vertex AI PaLM. GCP offers an enterprise version of PaLM through Vertex AI. The following instructions assumes you already have an account that has the necessary credentials to use Vertex AI. 

To use Google Cloud Platform Vertex AI PaLM you can do the following:

1. If you don't already have the `gcloud` command-line interface (CLI), you can install it by following instructions here https://cloud.google.com/sdk/docs/install
2. Once you have `gcloud`, run this command in the command line

```
$ gcloud auth application-default login
```

3. This will open up a browser for you to log into the account with the credentials to access Vertex AI. Follow the instructions and click through to login and approve.
4. Once you you're done, an `application_default_credentials.json` file wil be created at the default location. Ghost will know how to locate this file (it's just using Google's default location to find it) to log into Vertex. 