from django.shortcuts import render
from .models import Item

def item_list(request):
    items = Item.objects.all()
    context = {
        'items': items,
        'total_items': items.count(),
    }
    return render(request, 'core/item_list.html', context)