import logging  # These are neseccary libraries we are importing

from rasa.core.channels.channel import CollectingOutputChannel
from rasa.core.channels.channel import InputChannel
from rasa.core.channels.channel import UserMessage
from sanic import Blueprint, response

logger = logging.getLogger(__name__)


class GoogleConnector(InputChannel):
    """A custom http input channel.
    This implementation is the basis for a custom implementation of a chat
    frontend. You can customize this to send messages to Rasa Core and
    retrieve responses from the agent."""

    @classmethod
    def name(cls):
        return "google_assistant"

    def blueprint(self, on_new_message):  # Here, we define the webhook that Google Assistant
        # will use to pass the user inputs to Rasa Core,
        google_webhook = Blueprint('google_webhook',
                                   __name__)  # collect the responses and send them to Google Assistant

        @google_webhook.route("/", methods=['GET'])
        async def health(request):  # We design a Health route to control the connection
            return response.json({"status": "ok"})  # is established by returning 200 ok message

        @google_webhook.route("/webhook", methods=['POST'])
        async def receive(request):
            # Then we define the main route for our purpose
            payload = request.json
            intent = payload['inputs'][0]['intent']
            text = payload['inputs'][0]['rawInputs'][0]['query']

            if intent == 'actions.intent.MAIN':  # This is the initial message we ask to recieve when the assitant is invoked
                message = "Hello! Welcome to the Rasa-powered Google Assistant, Football Information"
            else:
                try:
                    out = CollectingOutputChannel()
                    await on_new_message(UserMessage(text, out))
                    responses = [m["text"] for m in out.messages]
                    message = responses[0]
                except Exception as e:
                    print(e)
                    print(payload)
                    message = "Sorry! I don't get your point. Could you repeat please!"

            r = {
                "expectUserResponse": 'true',
                "expectedInputs": [
                    {
                        "possibleIntents": [
                            {
                                "intent": "actions.intent.TEXT"
                                # This is our second intent defined in action.json, remember?
                            }
                        ],
                        "inputPrompt": {
                            "richInitialPrompt": {
                                "items": [
                                    {
                                        "simpleResponse": {
                                            "textToSpeech": message,
                                            "displayText": message
                                        }
                                    }
                                ]
                            }
                        }
                    }
                ]
            }
            return response.json(r)
        return google_webhook
