import random
import string

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from login.forms import LoginForm
from login.models import EmailIndentefication


def generate_alphanum_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = ''.join(random.sample(letters_and_digits, length))
    return rand_string


def base(request):
    return render(request, "login/base.html", {"users": User.objects.all(), "status": EmailIndentefication.objects.all()})

def base_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid:
            user = authenticate(request, username = request.POST["name"], password = request.POST["ps"])
            if user is not None:
                login(request, user)
                return redirect("base")
            else:
                print("a")
                return redirect("base")
    else:
        form = LoginForm()
    return render(request, "login/base_login.html", {"form": form, "users": User.objects.all(), "status": EmailIndentefication.objects.all()})

def base_sign(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request)
            if form.is_valid:
                random_slug = generate_alphanum_random_string(20)
                User.objects.create_user(email = request.POST["email_user"], username = request.POST["name"], password = request.POST["ps"])
                user = authenticate(request, email = request.POST["email_user"], username = request.POST["name"], password = request.POST["ps"])
                print(user)
                if user is not None:
                    EmailIndentefication.objects.create(username=request.POST["name"], slug_indentefication = random_slug)

                    send_mail(
                        'Activate account',
                        'link to for activate: http://127.0.0.1:8000/activate/' + random_slug,
                        'botlogin@ukr.net',
                        [request.POST["email_user"]],
                        fail_silently=False,
                    )

                    print("a")
                    login(request, user)
                return redirect("base")
        else:
            form = LoginForm()
            return render(request, "login/base_sign.html", {"form": form, "users": User.objects.all(), "status": EmailIndentefication.objects.all()})
    else:
        return redirect("base")

def sign_off(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("base")

def activate_email(request, abs_slug_indentefication):
    url_s = get_object_or_404(EmailIndentefication, slug_indentefication=abs_slug_indentefication)
    if url_s.status_account == "no":
        EmailIndentefication.objects.filter(username = url_s.username).update(status_account = "yes")
    return redirect("base")


