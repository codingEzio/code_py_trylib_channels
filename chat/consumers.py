from channels.generic.websocket import WebsocketConsumer
import json


class ChatConsumer(WebsocketConsumer):
    """
    A synchronous WebSocket consumer that accepts all connections, receives
    messages from its client, and echoes those message back to the same client.

    Also, consumers of current implementation can't talk to each other, in
    other words, if I opened a second browser and typed in a message, the
    message would NOT appear in the 1st browser, even though I'm in the same
    chat room.
    """
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.send(text_data=json.dumps({"message": message}))
