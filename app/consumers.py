#Generic Consumer- JsonWebsocketConsumer- and AsyncJsonWebsocketConsumer
#chat-app with redis channel layer
from channels.generic.websocket import JsonWebsocketConsumer,AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync

from .models import Chat,Group
from channels.db import database_sync_to_async

#MyJsonWebSocketCunsumer
class MyJsonWebSocketCunsumer(JsonWebsocketConsumer):
    def connect(self):
        print("Json Websocket Connected!!")
        print("Channel Layer: ",self.channel_layer)
        print("Channel Name: ",self.channel_name)

        self.group_name=self.scope['url_route']['kwargs']['groupkaname']
        print("Group Name: ",self.group_name)
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()  #To accpt the connection

    def receive_json(self, content,**kwargs):   
        print("Message recieved from client!!",content)
        # print("Real message From client: ",content['msg'])
        #finding group object
        group=Group.objects.filter(name=self.group_name).first()
        if self.scope['user'].is_authenticated:
            chat=Chat(
                content=content['msg'],
                group=group
            )
            chat.save()

            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type':'chat-message',
                    'message':content['msg']
                }
            )
        else:
            self.send_json({
                'message':"login-Required!!!"
            })
    def chat_message(self,event):
        print("event: ",event)
        self.send_json({
            'message':event['message']
        })

    def disconnect(self, code):
        print("Json Websocket Disconnected!!")
        print("close code: ",code)
        print('Channle layer: ',self.channel_layer)
        print('Channle Name: ',self.channel_name)
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )


#MyasyncJsonWebSocketCunsumer
class MyasyncJsonWebSocketCunsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        #This handler is called when client initially opens a connection 
        #and is about to finish the websocket
        print("Json Websocket Connected!!")
        print("Channel Layer: ",self.channel_layer)
        print("Channel Name: ",self.channel_name)

        self.group_name=self.scope['url_route']['kwargs']['groupkaname']
        print("Group Name: ",self.group_name)
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()  #To accpt the connection

    async def receive_json(self, content,**kwargs):   
        print("Json messages recieved from client!!")
        group=await database_sync_to_async(Group.objects.filter)(name=self.group_name).first()
        if self.scope['user'].is_authenticated:
            chat=Chat(
                content=content['msg'],
                group=group
            )
            await database_sync_to_async(chat.save)()
            await self.channel_layer.group_add(
                self.group_name,
                {
                    'type':'chat-message',
                    'message':content['msg']
                }
            )
        else:
            self.send_json({
                'message':"login-Required!!!"
            })
    async def chat_message(self,event):
        print("event: ",event)
        self.send_json({
            'message':event['message']
        })
    async def disconnect(self, code):
        print("Json Websocket Disconnected!!")
        print("close code: ",code)
        print('Channle layer: ',self.channel_layer)
        print('Channle Name: ',self.channel_name)
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )