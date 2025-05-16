from django.shortcuts import render # type: ignore


def index(request):
    return render(request, 'menu/index.html')


def view_menu(request, item_name):
    return render(request, 'menu/index.html', {'active': item_name})
