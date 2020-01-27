from django.shortcuts import render


def index(request):
    return render(request=request, template_name="chat/index.html", context={})


def room(request, room_name):
    return render(
        request=request,
        template_name="chat/room.html",
        context={"room_name": room_name},
    )
