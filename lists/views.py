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
        item.save()
    except ValidationError:
        lst.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {'error': error})
    return redirect(f'/lists/{lst.id}/')


def list_page(request, lst_id):
    lst = List.objects.get(id=lst_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], lst=lst)
            item.full_clean()
            item.save()
            return redirect(f'/lists/{lst.id}/')
        except ValidationError as e:
            error = "You can't have an empty list item"
    return render(request, 'lists.html', {'lst': lst, 'error': error})
