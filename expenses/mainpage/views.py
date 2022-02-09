from django.shortcuts import render, get_object_or_404, reverse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

from .models import CostItems, Portals
from .forms import AddCostItemForm, ListCostItemForm


@xframe_options_exempt
@csrf_exempt
def index(request):
    """Метод главной страницы"""

    template: str = 'mainpage/index.html'
    title: str = 'Главная страница Затраты'

    if "add_cost_item" in request.POST:
        add_cost_item_form = AddCostItemForm(request.POST)
        if add_cost_item_form.is_valid():
            new_cost_item = add_cost_item_form.save(commit=False)
            new_cost_item.portal_id = Portals.objects.get(pk=1)
            new_cost_item.save()
            return HttpResponseRedirect(reverse('mainpage:index'))
    else:
        # Создаем форму добавления новой Статьи затрат
        add_cost_item_form = AddCostItemForm()

    if "del_cost_item" in request.POST:
        for id_cost_item in request.POST.getlist('cost_items'):
            cost_item: CostItems = get_object_or_404(CostItems,
                                                     pk=id_cost_item)
            cost_item.delete()
        return HttpResponseRedirect(reverse('mainpage:index'))

    list_cost_item_form = ListCostItemForm()
    # Формируем словарь context
    context: dict[str, any] = {
        'title': title,
        'add_cost_item_form': add_cost_item_form,
        'list_cost_item_form': list_cost_item_form,
    }
    # Рендерим страницу
    return render(request, template, context)
