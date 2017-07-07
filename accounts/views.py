from django.core.mail import send_mail
from django.shortcuts import render, redirect


def send_login_email(request):
    email = request.POST['email']
    send_mail(
        'Your login link for to-do app',
        'Use this link to login:',
        'noreply@todoapp',
        [email])
    return redirect('/')


def login(request):
    pass


def logout(request):
    pass
