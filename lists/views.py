from django.shortcuts import render, redirect
from lists.models import Item, List
# from django.http import HttpResponse

# Create your views here.


def home_page(request):
    '''View for home page'''
    # render creates HttpResponse for us
    return render(request, 'home.html')


def new_list_page(request):
    lst = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], lst=lst)
    return redirect(f'/lists/{lst.id}/')


def list_page(request, lst_id):
    lst = List.objects.get(id=lst_id)
    return render(request, 'lists.html', {'lst': lst})


def add_item(request, lst_id):
    lst = List.objects.get(id=lst_id)
    Item.objects.create(text=request.POST['item_text'], lst=lst)
    return redirect(f'/lists/{lst.id}/')
