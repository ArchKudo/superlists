from django.shortcuts import render, redirect
from lists.models import Item
# from django.http import HttpResponse

# Create your views here.


def home_page(request):
    # render creates HttpResponse for us
    return render(request, 'home.html')


def list_page(request):
    items = Item.objects.all()
    return render(request, 'lists.html', {'items': items})


def new_list_page(request):
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/first_list/')
