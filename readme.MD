<img src="static/logo.png" alt="Ghost logo" width="150px"/>

Ghost is a small footprint AI assistant, built to run locally in your computer. It is meant for developers and can be modified/customised easily to suit your needs. Ghost is built using Langchain.

[![Ghost AI code assistant that runs on your laptop](https://img.youtube.com/vi/JOhN2E7VpIg/0.jpg)](https://youtu.be/JOhN2E7VpIg)

Ghost AI code assistant that runs on your laptop

[![Ghost querying a relational database](https://img.youtube.com/vi/LMUp3OLz9QY/0.jpg)](https://youtu.be/LMUp3OLz9QY)

Ghost can query any relational database, given the connection URL

[![Ghost analysing CSV files](https://img.youtube.com/vi/6LINgbkEy9k/0.jpg)](https://youtu.be/6LINgbkEy9k)

Ghost can analyse CSV files on your laptop

[![Ghost accessing documents](https://img.youtube.com/vi/3J5guAtRLGI/0.jpg)](https://youtu.be/3J5guAtRLGI)

Ghost can access different documents, search for images and read from images too

Ghost is written using Langchain and has configured the following tools:

1. Python REPL 
2. Shell 
3. Search (DuckDuckGo)
4. Ask Document (Unstructured File)
5. Ask CSV (Pandas)
6. Ask Database
7. Requests
8. Image Search (Google Image Search through SerpAPI) -- requires SerpAPI API key (https://serpapi.com)
   
Please check the `tools.py` file for more details.

It is fully customisable and extensible. In fact, while Ghost can be used out-of-the-box, it is meant to be customised for your own personal usage and style. Feel free to add or remove tools accordingly or change everything to what you want!

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

## Saving output

By default, Ghost saves all your output to markdown format in a file named `output.md`. You can change it in the `.env` file.