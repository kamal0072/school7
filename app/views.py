from django.shortcuts import render,HttpResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Group, Chat


def index(request,group_name):
    print("Group Name: ",group_name)
    group=Group.objects.filter(name=group_name).first()
    if group:
        chat=Chat.objects.filter(group=group)
    else:
        group=Group(name=group_name)
        group.save()
    return render(request,'index.html',{"group_name":group_name,"chat":chat})

def msgfromview(request):
    channel_layer=get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "India",
        {
            "type":'chat.message',
            'message':'message from outside consumer',
        }
    )
    return HttpResponse("Message sent from view to conusmer")
