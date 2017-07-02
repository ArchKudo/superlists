from django.shortcuts import render, redirect
from lists.models import Item, List
from lists.forms import ItemForm
from django.core.exceptions import ValidationError


def home_page(request):
    '''View for home page'''
    # render creates HttpResponse for us
    return render(request, 'home.html', {'form': ItemForm()})


def new_list_page(request):
    form = ItemForm(data=request.POST)

    if form.is_valid():
        lst = List.objects.create()
        Item.objects.create(text=request.POST['text'], lst=lst)
        return redirect(lst)

    else:
        return render(request, 'home.html', {'form': form})


def list_page(request, lst_id):
    lst = List.objects.get(id=lst_id)
    form = ItemForm()

    if request.method == 'POST':
        form = ItemForm(data=request.POST)

        if form.is_valid():
            Item.objects.create(text=request.POST['text'], lst=lst)
            return redirect(lst)

    return render(request, 'lists.html', {'lst': lst, 'form': form, })
