from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.clickjacking import xframe_options_exempt

from .forms import AddExpensesForm
from mainpage.models import Portals, Expenses


def card(request):
    template: str = 'dealcard/card.html'
    title: str = 'Страница карточки сделки'

    expenses = Expenses.objects.filter(deal_id=157)
    produscts = [
        {
            'product_id': 33,
            'product_name': 'Авиадоставка груза',
            'product_cost': 10000.00,
            'product_count': 2,
            'product_sum': 20000.00,
        },
        {
            'product_id': 66,
            'product_name': 'Автодоставка груза',
            'product_cost': 5000.00,
            'product_count': 3,
            'product_sum': 15000.00,
         },
    ]

    context: dict[str, any] = {
        'title': title,
        'expenses': expenses,
        'products': produscts,
    }
    return render(request, template, context)


def add_expense(request):
    """Метод добавления новых Затрат"""

    template: str = 'dealcard/add_expense.html'

    form = AddExpensesForm(request.POST or None)
    if not form.is_valid():
        return render(request, template, {'form': form})
    fields = form.save(commit=False)
    fields.product_id = request.GET['id']
    fields.deal_id = 157
    fields.cargo_id = 12
    fields.employee_id = 1
    fields.owner_id = 1
    fields.owner_name = 'Кириллов Евгений'
    fields.portal_id = Portals.objects.get(pk=1)
    fields.save()
    return redirect('dealcard:card')


def edit_expense(request, expense_id):
    """Метод редактирования Затрат"""

    template: str = 'dealcard/add_expense.html'
    is_edit: bool = True

    expense: Expenses = get_object_or_404(Expenses, pk=expense_id)
    form = AddExpensesForm(request.POST or None, instance=expense)

    context: dict[str, any] = {
        'form': form,
        'is_edit': is_edit,
        'expense_id': expense_id,
    }

    if not form.is_valid():

        return render(request, template, context)
    form.save()
    return redirect('dealcard:card')


def delete_expense(request, expense_id):
    """Метод удаления Затрат"""

    expense: Expenses = get_object_or_404(Expenses, pk=expense_id)
    expense.delete()
    return redirect('dealcard:card')
