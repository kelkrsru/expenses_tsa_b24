from django.shortcuts import render, get_object_or_404, reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect


def card(request):
    template: str = 'dealcard/card.html'
    title: str = 'Страница карточки сделки'

    context: dict[str, any] = {
        'title': title,
    }
    return render(request, template, context)


def add_expense(request):
    template: str = 'dealcard/add_expense.html'
    title: str = 'Добавить затраты к услуге'

    context: dict[str, any] = {
        'title': title,
    }
    return render(request, template, context)
