import os
from flask import Flask, render_template, request, jsonify
from waitress import serve
import webbrowser
from datetime import datetime

from agents import Agent
from config import output_file, provider
from config import provider_config as cfg


# get path for static files
static_dir = os.path.join(os.path.dirname(__file__), 'static')
if not os.path.exists(static_dir):
    static_dir = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'static')


def save(prompt, response):
    with open(output_file, 'a') as file:
        file.write("# " + provider.upper() + " " + cfg.model_name.upper() +
                   " <small>[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]</small>" +
                   "\n## PROMPT\n" + prompt +
                   "\n## RESPONSE\n" + response +
                   "\n\n")


# start server
print("\033[96mStarting Ghost at http://127.0.0.1:1337\033[0m")
ghost = Flask(__name__, static_folder=static_dir, template_folder=static_dir)
agent = Agent()

# server landing page
@ghost.route('/')
def landing():
    return render_template('index.html')

# run
@ghost.route('/run', methods=['POST'])
def run():
    data = request.json
    response = agent.run(data['input'])
    save(data['input'], response)
    return jsonify({'input': data['input'],
                    'response': response})

# reset
@ghost.route('/reset', methods=['POST'])
def reset():
    agent.reset()
    return jsonify({
        'response': 'Agent was reset',
    })


if __name__ == '__main__':
    print("\033[93mGhost started. Press CTRL+C to quit.\033[0m")
    # webbrowser.open("http://127.0.0.1:1337")
    serve(ghost, port=1337, threads=16)
