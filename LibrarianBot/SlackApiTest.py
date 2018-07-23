import os
from slackclient import SlackClient
from Constants import SLACK_TOKEN

sc = SlackClient(SLACK_TOKEN)

print(sc.api_call("api.test"))

# sc.api_call(
#     "chat.postMessage",
#     channel="#general",
#     text="Hello from Python! :tada:"
# )