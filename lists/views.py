from django.shortcuts import render, redirect
from lists.models import Item, List
from django.core.exceptions import ValidationError


def home_page(request):
    '''View for home page'''
    # render creates HttpResponse for us
    return render(request, 'home.html')


def new_list_page(request):
    lst = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], lst=lst)
    try:
        item.full_clean()
    except ValidationError:
        lst.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {'error': error})
    return redirect(f'/lists/{lst.id}/')


def list_page(request, lst_id):
    lst = List.objects.get(id=lst_id)
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'], lst=lst)
        return redirect(f'/lists/{lst.id}/')
    return render(request, 'lists.html', {'lst': lst})
