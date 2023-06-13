from django.shortcuts import render

from chat.models import Room, Message
from django.http import JsonResponse

def index_view(request):
    return render(
        request,
        "index.html",
        {
            "rooms": Room.objects.all(),
        },
    )


def room_view(request, room_name):
    chat_room, created = Room.objects.get_or_create(name=room_name)
    messages = []
    if created == False:
        message = Message.objects.filter(room=chat_room)
        for i in message:
            messages.append({
                "username": i.user.username,
                "content": i.content,
                "timestamp": i.timestamp
            })
    return render(
        request,
        "room.html",
        {
            "room": chat_room,
            "messages": messages
        },
    )

def get_messages(request):
    room_name = request.GET['name']
    chat_room, created = Room.objects.get_or_create(name=room_name)
    messages = Message.objects.filter(room=chat_room)
    data = [{"user": message.user.username, "content": message.content, "timestamp":message.timestamp} for message in messages]
    return JsonResponse(data, safe=False)
