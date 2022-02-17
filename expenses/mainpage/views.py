import datetime

from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from pybitrix24 import Bitrix24

from .models import CostItems, Portals
from .forms import AddCostItemForm, CostItemForm

CLIENT_ID: str = 'local.6204bf06c900d9.42778754'
CLIENT_SECRET: str = 'm0DLoSHxV0YPxTu2oE8jY2wRZ0DTiC38k1PCQl4MVMHXY1aJqm'


@xframe_options_exempt
@csrf_exempt
def index(request):
    """Метод главной страницы"""

    template: str = 'mainpage/index.html'
    title: str = 'Главная страница Затраты'
    if 'member_id' in request.POST:
        member_id = request.POST['member_id']
    elif request.GET.get('member_id'):
        member_id = request.GET.get('member_id')
    else:
        return render(request, 'error.html', {
            'error_name': 'QueryError',
            'error_description': 'Неизвестный тип запроса'
        })

    portal: Portals = _create_portal(member_id)
    list_cost_item_form = CostItemForm(portal=portal)

    if "add_cost_item" in request.POST:
        add_cost_item_form = AddCostItemForm(request.POST or None)
        if not add_cost_item_form.is_valid():
            context: dict[str, any] = {
                'title': title,
                'add_cost_item_form': add_cost_item_form,
                'list_cost_item_form': list_cost_item_form,
                'member_id': member_id,
            }
            return render(request, template, context)
        add_cost_item_form.save()
        redirect_url = '{url}?member_id={member_id}'.format(
            url=reverse('mainpage:index'), member_id=member_id)
        return redirect(redirect_url)
    else:
        add_cost_item_form = AddCostItemForm(initial={'portal': portal})

    if "del_cost_item" in request.POST:
        for id_cost_item in request.POST.getlist('name'):
            cost_item: CostItems = get_object_or_404(CostItems,
                                                     pk=id_cost_item)
            cost_item.delete()
        redirect_url = '{url}?member_id={member_id}'.format(
            url=reverse('mainpage:index'), member_id=member_id)
        return redirect(redirect_url)

    context: dict[str, any] = {
        'title': title,
        'add_cost_item_form': add_cost_item_form,
        'list_cost_item_form': list_cost_item_form,
        'member_id': member_id,
    }
    return render(request, template, context)


@xframe_options_exempt
@csrf_exempt
def install(request):
    """Метод установки приложения"""

    try:
        portal: Portals = Portals.objects.get(
            member_id=request.POST['member_id'])
        portal.auth_id = request.POST['AUTH_ID']
        portal.refresh_id = request.POST['REFRESH_ID']
        portal.save()
    except Portals.DoesNotExist:
        portal: Portals = Portals.objects.create(
            member_id=request.POST['member_id'],
            name=request.GET.get('DOMAIN'),
            auth_id=request.POST['AUTH_ID'],
            refresh_id=request.POST['REFRESH_ID']
        )

    bx24 = Bitrix24(portal.name)
    bx24._access_token = portal.auth_id
    bx24._refresh_token = portal.refresh_id

    params: dict[str, str] = {
        'PLACEMENT': 'CRM_DEAL_DETAIL_TAB',
        'HANDLER': 'https://expenses.krasprogress24.ru/card/',
        'TITLE': 'Затраты',
        'DESCRIPTION': 'Приложение для учета затрат в сделках по услугам'
    }

    result = bx24.call('placement.bind', params)
    if 'error' in result:
        return render(request, 'error.html', {
            'error_name': result['error'],
            'error_description': result['error_description'],
        })

    return render(request, 'mainpage/install.html')


def _create_portal(member_id: str) -> Portals:
    portal: Portals = get_object_or_404(Portals, member_id=member_id)

    if ((portal.auth_id_create_date + datetime.timedelta(0, 3600)) <
            timezone.now()):
        bx24 = Bitrix24(portal.name)
        bx24._refresh_token = portal.refresh_id
        bx24.client_id = CLIENT_ID
        bx24.client_secret = CLIENT_SECRET
        bx24.refresh_tokens()
        portal.auth_id = bx24._access_token
        portal.refresh_id = bx24._refresh_token
        portal.save()

    return portal
