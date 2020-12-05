# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import Message
from django.conf import settings
from .views import get_last_10_messages,get_curent_chat
# from channels.db import database_sync_to_sync
# from user.models import Message

from accounts.models import User
#User=settings.AUTH_USER_MODEL

class ChatConsumer(WebsocketConsumer):


    def fetch_messages(self,data):
        print('fetching')
        messages=get_last_10_messages(int(self.room_name))
        context ={
            'command': 'messages',
            'messages' : self.messages_to_json(messages,self.room_name)
        }
        self.send_message(context)
      
    

    def typing(self,data) :
        person = User.objects.get(username=data['username'])

        context ={
            'command':'typing',
            'type':data['type'],
            'message':{
                'name':person.username
            }
        }
        self.send_chat_message(context)
    

    """    def online(self,data) :
        person= User.objects.get(username=data['username']) 
        context ={
            'command':'online',
            'message':{
                'name':person.username
            }
        }
        self.send_chat_message(context)"""




    def new_messages(self,data) :
        
        user = User.objects.get(username =data["from"])
        
        # author_user=User.objects.filter(username=contact)[0]
        message = Message.objects.create(user=user,content=data['message'])
       
        content={
            'command':'new_message',
            'message':self.message_to_json(message,self.room_name)
        }
        current_chat = get_curent_chat(self.room_name)
        current_chat.messages.add(message)
        current_chat.save()
         
        # print(data['message'])

        return self.send_chat_message(content)


    def send_media(self,data) :
        user = User.objects.get(username=data['from'])
        content = {
                "command":media ,
                "type" :data['type'],
                 "url" : data["url"]
                }
        self.send_chat_message(content)


    def messages_to_json(self,messages,id) :
        result = []
        for  message in messages :
            result.append(self.message_to_json(message,id))
        return result
    

    def message_to_json(self,message,id):
        return {
            'id':message.id,
            'author':message.user.username,
            'content':message.content,
            'timestamp':str(message.timestamp),
            'chatId':id
        }

    commands ={
            'fetch_messages': fetch_messages,
            'new_message'  : new_messages,
          #  'online':online,
            'typing':typing,
            'media':send_media
         }

    def connect(self):
        print("connecting")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
            # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    # Receive message from WebSocket
    
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self,data)


    def send_chat_message(self,message) :
     
        #message =data_json['message']

        # Send message to room group
      
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        print(self.room_group_name)
        

    

    def send_message(self,context) :
       
         self.send(text_data=json.dumps(context
        ))


    # Receive message from room group
    def chat_message(self, event):
        # print('on chat.message worked')
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message':message
        }
        ))
