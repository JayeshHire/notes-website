from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

def t1(request) :
    request.session["message"] = "hello world"
    return HttpResponseRedirect(reverse("notes:test2"))

def t2(request):
    message = request.session.get("username", "no username")
    return HttpResponse(message)

def t3(request):
    del request.session["message"]
    return HttpResponseRedirect(reverse("notes:test2"))