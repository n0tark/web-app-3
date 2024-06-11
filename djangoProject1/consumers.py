from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_id = data['user_id']
        is_online = data['is_online']

        await self.channel_layer.group_send(
            'online_users_group',
            {
                'type': 'user_status',
                'user_id': user_id,
                'is_online': is_online
            }
        )

    async def user_status(self, event):
        user_id = event['user_id']
        is_online = event['is_online']

        # Відправка повідомлення про онлайн статус користувача на клієнт
        await self.send(text_data=json.dumps({
            'user_id': user_id,
            'is_online': is_online
        }))


class PhoneConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        phone_number = data['phone_number']

        await self.channel_layer.group_send(
            'phones_group',
            {
                'type': 'phone_message',
                'phone_number': phone_number
            }
        )

    async def phone_message(self, event):
        phone_number = event['phone_number']

        await self.send(text_data=json.dumps({
            'phone_number': phone_number
        }))


# Operation send email and delete contscts
from channels.generic.websocket import AsyncWebsocketConsumer

class OperationsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'operations_group',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'operations_group',
            self.channel_name
        )

    async def send_status_update(self, event):
        status = event['status']
        operation_name = event['operation_name']
        operation_data = event['operation_data']
        result = event['result']
        timestamp = event['timestamp']

        await self.send(text_data='Status update: {} - {} - {} - {} - {}'.format(
            status, operation_name, operation_data, result, timestamp
        ))
