from django.shortcuts import render, redirect
from lists.models import Item
# from django.http import HttpResponse

# Create your views here.


def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/first_list/')

    items = Item.objects.all()

    # render creates HttpResponse for us
    return render(request, 'home.html', {'items': items})


def list_page(request):
    items = Item.objects.all()
    return render(request, 'lists.html', {'items': items})
