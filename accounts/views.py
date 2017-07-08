from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect


def send_login_email(request):
    email = request.POST['email']
    send_mail(
        'Your login link for To-do app MVC',
        'Use this link to login:',
        'noreply@todoapp',
        [email])

    messages.success(request, 'Check your email for login link')
    return redirect('/')


def login(request):
    pass


def logout(request):
    pass
