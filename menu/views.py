from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.utils import timezone
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from .models import Menu, Item
from .forms import MenuForm


def menu_list(request):
    all_menus = Menu.objects.all().prefetch_related('items')
    menus = []
    for menu in all_menus:
        if ((menu.expiration_date and
             menu.expiration_date >= timezone.now().date()
             ) or not menu.expiration_date):
            menus.append(menu)
    menus = sorted(menus, key=lambda x: x.expiration_date or date.min)
    return render(request, 'menu/list_all_current_menus.html',
                  {'menus': menus})


def menu_detail(request, pk):
    menu = Menu.objects.get(pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    try:
        item = Item.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'menu/detail_item.html', {'item': item})


def create_new_menu(request):
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.created_date = timezone.now().date()
            menu.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse('menu:menu_detail',
                                                kwargs={'pk': menu.pk}))
    else:
        form = MenuForm()
    return render(request, 'menu/menu_edit.html', {'form': form})


def edit_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    form = MenuForm(instance=menu)
    if request.method == 'POST':
        form = MenuForm(instance=menu, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated menu")
            return HttpResponseRedirect(reverse('menu:menu_list'))
    return render(request, 'menu/change_menu.html', {'form': form})
