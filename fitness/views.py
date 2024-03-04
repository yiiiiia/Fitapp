from django.http import HttpResponse


def login(request):
    return HttpResponse(b"You need to login to use this app!")
