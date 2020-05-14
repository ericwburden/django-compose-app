import json

from .models import Counter
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.forms.models import model_to_dict


class CounterConsumer(WebsocketConsumer):
    def connect(self):
        self.counter_name = self.scope['url_route']['kwargs']['counter_name']
        self.counter_group_name = 'chat_%s' % self.counter_name

        # Join counter group
        async_to_sync(self.channel_layer.group_add)(
            self.counter_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave the counter group
        async_to_sync(self.channel_layer.group_discard)(
            self.counter_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        counter = Counter.objects.get(counter_name=self.counter_name)

        if text_data_json['operation'] == 'add':
            counter.increment()
        
        if text_data_json['operation'] == 'subtract':
            counter.decrement()

        dict_obj = model_to_dict(counter)
        
        async_to_sync(self.channel_layer.group_send)(
            self.counter_group_name,
            {
                'type': 'update',
                'counter': json.dumps(dict_obj)
            }
        )

    # Receive message from counter group
    def update(self, event):
        counter = event['counter']
        # Send message to WebSocket
        self.send(text_data=counter)
