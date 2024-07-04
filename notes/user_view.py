from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


#create user
def user_signup(request):

    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            message = "Your both the passwords are not matching. Enter again"
            context = {
                "message": message
            }
            return render(request, "notes/signup.html", context)
        if User.objects.filter(username=username).exists() or \
                User.objects.filter(email=email).exists():
            message = "username or email exists try another username or login with existing username"
            context = {
                "message": message
            }
            return render(request, "notes/signup.html", context=context)
        user = User.objects.create_user(username=username, email=email, password=password)
        request.session["username"] = username
        return HttpResponseRedirect(reverse("notes:note-list"))

    context = {
        "message": ""
    }
    return render(request, "notes/signup.html", context)

# jay adsfa
# user login
def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                request.session['username'] = username
                return HttpResponseRedirect(reverse("notes:todo-list-index"))
            message = "user password does not match."
            context = {
                'message': message
            }
            return render(request, "notes/login.html", context)
        except User.DoesNotExist:
            message = "user does not exists. enter appropriate username"
            context = {
                'message': message
            }
            return render(request, "notes/login.html", context)

    context = {
        'message': ''
    }
    return render(request, "notes/login.html", context)


# user logout
def logout(request):
    del request.session["username"]
    return HttpResponseRedirect(reverse("notes:login"))


def authorized(view_func):

    def wrapper(request, *args, **kwargs):
        username = request.session.get("username", "")
        if username == "":
            return HttpResponseRedirect(reverse("notes:login"))
        return view_func(request, *args, **kwargs)
    return wrapper





