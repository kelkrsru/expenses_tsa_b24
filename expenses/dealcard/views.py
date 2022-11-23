import datetime
import decimal
import json

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from pybitrix24 import Bitrix24

from mainpage.models import Portals
from .forms import ExpensesForm
from .models import Expenses, Cargo, CompaniesExpense, Employee

CLIENT_ID: str = 'local.63467384b9f750.01806162'
CLIENT_SECRET: str = 'Phmcn8NpEzGqssG2Zj7m4tIaLylHHSj4QoIOFVr8Z7qqFJbsGN'
SMART_ID: int = 177
FIELD_NAME_COMPANY_EXPENSE_FILTER = 'UF_CRM_1644559561'


@xframe_options_exempt
@csrf_exempt
def card(request):
    template: str = 'dealcard/card.html'
    title: str = 'Страница карточки сделки'

    if request.method == 'POST':
        member_id: str = request.POST['member_id']
        deal_id: int = int(json.loads(request.POST['PLACEMENT_OPTIONS'])['ID'])
    elif request.method == 'GET':
        member_id: str = request.GET.get('member_id')
        deal_id: int = int(request.GET.get('deal_id'))
    else:
        return render(request, 'error.html', {
            'error_name': 'QueryError',
            'error_description': 'Неизвестный тип запроса'
        })

    portal: Portals = _create_portal(member_id)

    try:
        bx24_obj = ObjBitrix24(portal, deal_id)
        # Получаем сделку и товары
        bx24_obj.get_deal_products()
        if not bx24_obj.deal_products:
            return render(request, 'dealcard/no_products.html')
        # Получаем грузы
        bx24_obj.get_cargo(SMART_ID)
        for item in bx24_obj.cargo:
            if item['ufCrm3_1642060927620']:
                Cargo.objects.update_or_create(
                    id_b24=item['id'],
                    portal=portal,
                    defaults={
                        'id_b24': item['id'],
                        'number': item['ufCrm3_1642060927620'],
                        'portal': portal,
                        'deal_id': deal_id,
                    })
        # Получаем компании
        bx24_obj.get_companies(FIELD_NAME_COMPANY_EXPENSE_FILTER)
        for item in bx24_obj.companies:
            CompaniesExpense.objects.update_or_create(
                id_b24=item['ID'],
                portal=portal,
                defaults={
                    'id_b24': item['ID'],
                    'name': item['TITLE'],
                    'portal': portal,
                })
        # Получаем сотрудников
        bx24_obj.get_users()
        for user in bx24_obj.users:
            Employee.objects.update_or_create(
                id_b24=user['ID'],
                portal=portal,
                defaults={
                    'id_b24': user['ID'],
                    'name': user['NAME'],
                    'last_name': user['LAST_NAME'],
                    'portal': portal,
                }
            )
    except RuntimeError as ex:
        return render(request, 'error.html', {
            'error_name': ex.args[0],
            'error_description': ex.args[1]
        })

    expenses = Expenses.objects.filter(deal_id=deal_id)

    calculations: dict[str, int] = {
        'proceeds': 0,
        'sum_expenses': 0,
        'income': 0,
        'profitability': 0,
    }

    # Выручка
    for product in bx24_obj.deal_products:
        calculations['proceeds'] += (decimal.Decimal(product['PRICE'])
                                     * int(product['QUANTITY']))
        calculations['proceeds'] = round(calculations['proceeds'], 2)

    # Затраты
    for expense in expenses:
        calculations['sum_expenses'] += expense.expense

    # Прибыль
    calculations['income'] = (calculations['proceeds']
                              - calculations['sum_expenses'])

    # Рентабельность
    if calculations['proceeds'] != 0:
        calculations['profitability'] = round(calculations['income']
                                              / calculations['proceeds'] * 100)
    else:
        calculations['profitability'] = 0

    context: dict[str, any] = {
        'title': title,
        'portal': portal,
        'expenses': expenses,
        'deal_id': deal_id,
        'bx24_obj': bx24_obj,
        'calculations': calculations,
    }
    return render(request, template, context)


@xframe_options_exempt
@csrf_exempt
def add_expense(request):
    """Метод добавления новых Затрат"""

    template: str = 'dealcard/add_expense.html'
    deal_id: int = int(request.GET.get('deal_id'))
    product_id: int = int(request.GET.get('product_id'))
    member_id: str = request.GET.get('member_id')

    portal: Portals = _create_portal(member_id)

    try:
        bx24_obj = ObjBitrix24(portal)
        bx24_obj.get_current_user()
        owner = get_object_or_404(Employee, id_b24=bx24_obj.current_user['ID'],
                                  portal=portal)
    except RuntimeError as ex:
        return render(request, 'error.html', {
            'error_name': ex.args[0],
            'error_description': ex.args[1]
        })

    form = ExpensesForm(request.POST or None, portal=portal, deal_id=deal_id)
    if not form.is_valid():
        context: dict[str, any] = {
            'form': form,
            'deal_id': deal_id,
            'product_id': product_id,
            'member_id': member_id,
        }
        return render(request, template, context)

    fields = form.save(commit=False)
    fields.product_id = product_id
    fields.deal_id = deal_id
    fields.owner = owner
    fields.portal = portal
    fields.save()
    redirect_url = '{url}?member_id={member_id}&deal_id={deal_id}'.format(
        url=reverse('dealcard:card'), member_id=member_id, deal_id=deal_id)
    return redirect(redirect_url)


@xframe_options_exempt
@csrf_exempt
def edit_expense(request, expense_id):
    """Метод редактирования Затрат"""

    template: str = 'dealcard/add_expense.html'
    is_edit: bool = True
    deal_id: int = int(request.GET.get('deal_id'))
    member_id: str = request.GET.get('member_id')

    portal: Portals = _create_portal(member_id)
    expense: Expenses = get_object_or_404(Expenses, pk=expense_id)

    form = ExpensesForm(request.POST or None, instance=expense,
                        portal=portal, deal_id=deal_id)

    context: dict[str, any] = {
        'form': form,
        'is_edit': is_edit,
        'expense_id': expense_id,
        'deal_id': deal_id,
        'member_id': member_id,
    }

    if not form.is_valid():
        return render(request, template, context)
    form.save()
    redirect_url = '{url}?member_id={member_id}&deal_id={deal_id}'.format(
        url=reverse('dealcard:card'), member_id=member_id, deal_id=deal_id)
    return redirect(redirect_url)


@xframe_options_exempt
@csrf_exempt
def delete_expense(request, expense_id):
    """Метод удаления Затрат"""

    deal_id: int = int(request.GET.get('deal_id'))
    member_id: str = request.GET.get('member_id')

    expense: Expenses = get_object_or_404(Expenses, pk=expense_id)
    expense.delete()
    redirect_url = '{url}?member_id={member_id}&deal_id={deal_id}'.format(
        url=reverse('dealcard:card'), member_id=member_id, deal_id=deal_id)
    return redirect(redirect_url)


class ObjBitrix24:
    """Класс объекта Битрикс24"""

    def __init__(self, portal: Portals, deal_id: int = None):
        self.portal = portal
        self.deal_id = deal_id
        self.bx24 = Bitrix24(portal.name)
        self.bx24._access_token = portal.auth_id
        self.users = None
        self.deal_products = None
        self.deal_props = None
        self.companies = None
        self.company = None
        self.cargo = None
        self.current_user = None
        self.user = None

    @staticmethod
    def check_error(result):
        if 'error' in result:
            raise RuntimeError(result['error'], result['error_description'])
        elif 'result' in result:
            return result['result']
        else:
            raise RuntimeError('Error', 'No description error')

    def get_users(self):
        """Получить всех пользователей портала"""

        method_rest = 'user.search'
        params = {
            'filter': {
                'USER_TYPE': 'employee',
            },
        }
        result = self.bx24.call(method_rest, params)
        self.users = self.check_error(result)

    def get_current_user(self):
        """Получить текущего пользователя"""

        method_rest = 'user.current'
        result = self.bx24.call(method_rest)
        self.current_user = self.check_error(result)

    def get_user(self, user_id):
        """Получить пользователя по id"""
        method_rest = 'user.get'
        params = {'id': user_id}
        result = self.bx24.call(method_rest, params)
        self.user = self.check_error(result)

    def get_deal_products(self):
        """Получить все продукты сделки"""

        method_rest = 'crm.deal.productrows.get'
        params = {'id': self.deal_id}
        result = self.bx24.call(method_rest, params)
        self.deal_products = self.check_error(result)

    def get_deal_props(self):
        """Получить все данные по сделке"""

        method_rest = 'crm.deal.get'
        params = {'id': self.deal_id}
        result = self.bx24.call(method_rest, params)
        self.deal_props = self.check_error(result)

    def get_companies(self, field_filter):
        """Получить все компании, которые могут иметь затраты"""

        method_rest = 'crm.company.list'
        params = {
            'filter': {
                field_filter: 1,
            },
            'select': ['TITLE']
        }
        result = self.bx24.call(method_rest, params)
        if 'error' in result:
            raise RuntimeError(result['error'], result['error_description'])
        elif 'result' in result:
            self.companies = result['result']
            if 'next' in result:
                while 'next' in result:
                    params = {
                        'filter': {
                            field_filter: 1,
                        },
                        'select': ['TITLE'],
                        'start': result['next']
                    }
                    result = self.bx24.call(method_rest, params)
                    self.companies += result['result']
        else:
            raise RuntimeError('Error', 'No description error')

    def get_company(self, company_id):
        """Получить компанию по id"""

        method_rest = 'crm.company.get'
        params = {
            'id': company_id,
        }
        result = self.bx24.call(method_rest, params)
        self.company = self.check_error(result)

    def get_cargo(self, smart_id):
        """Получить все грузы сделки"""

        method_rest = 'crm.item.list'
        params = {
            'entityTypeId': smart_id,
            'filter': {
                '=parentId2': self.deal_id,
            }
        }
        result = self.bx24.call(method_rest, params)
        result = self.check_error(result)
        self.cargo = result['items']


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
