from accounts.models import Token
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.shortcuts import redirect


def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + '?token=' + str(token.uid))
    message_body = f'Use this link to login:{url}'

    send_mail(
        'Your login link for To-do app MVC',
        message_body,
        'noreply@todoapp',
        [email])

    messages.success(request, 'Check your email for login link')
    return redirect('/')


def login(request):
    return redirect('/')


def logout(request):
    pass
