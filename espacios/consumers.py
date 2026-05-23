from channels.generic.websocket import WebsocketConsumer

from asgiref.sync import async_to_sync

import json


class KanbanConsumer(WebsocketConsumer):

    """
    Consumer realtime principal del
    tablero colaborativo Kanban.
    """

    def connect(self):

        self.room_group_name = (
            'kanban_general'
        )

        async_to_sync(
            self.channel_layer.group_add
        )(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        self.send(text_data=json.dumps({

            'tipo': 'conexion_exitosa',

            'mensaje': (
                'WebSocket conectado correctamente.'
            )

        }))

    def disconnect(self, close_code):

        async_to_sync(
            self.channel_layer.group_discard
        )(
            self.room_group_name,
            self.channel_name
        )

        print(
            'Usuario desconectado.'
        )

    def receive(self, text_data):

        datos_recibidos = json.loads(
            text_data
        )

        async_to_sync(
            self.channel_layer.group_send
        )(

            self.room_group_name,

            {

                'type': 'evento_kanban',

                'mensaje': datos_recibidos

            }

        )

    def evento_kanban(self, event):

        mensaje_socket = event['mensaje']

        self.send(text_data=json.dumps({

            'tipo': 'evento_realtime',

            'contenido': mensaje_socket

        }))