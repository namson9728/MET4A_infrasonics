import os, slack
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter


env_path = Path('./src') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'], '/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])


import model.setup as setup

channel = os.environ['CHANNEL']
setup.sayhi(client, channel)

if __name__ == "__main__":
    app.run(debug="True")