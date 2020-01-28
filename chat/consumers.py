from channels.generic.websocket import AsyncWebsocketConsumer

import json


class ChatConsumer(AsyncWebsocketConsumer):
    """
    A synchronous WebSocket consumer that accepts all connections, receives
    messages from its client, and echoes those message back to the same client.

    Also, consumers of current implementation can't talk to each other, in
    other words, if I opened a second browser and typed in a message, the
    message would NOT appear in the 1st browser, even though I'm in the same
    chat room.

    In order to let them be able to communicate, we need a 'channel layer'.
    It allows multiple consumer instances to talk with each other, and with
    other pats of Django.

    What is a `scope` (self.scope)?
    0. https://channels.readthedocs.io/en/latest/topics/consumers.html#scope
    1. it was used to get connection info, just like `request` in views :P

    Why use `async_to_sync`?
    > All channel layer methods are ASYNCHRONOUS, whereas the ChatConsumer is
      a synchronous one. Also, we no longer need this after we've rewritten
      this fully asynchronous.
    """

    async def connect(self):
        # Obtain the 'room_name' from 'chat/routing.py'
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        # Generate a unique group name (for channels) (requires 'ASCII only')
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):
        """
        Receive message from WebSocket.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    async def chat_message(self, event):
        """
        Receive message from room group.
        """
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
