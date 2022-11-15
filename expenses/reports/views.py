import decimal
import datetime

from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.utils.dateparse import parse_date

from .forms import ReportFinanceForm, ReportBuhForm
from dealcard.models import Expenses, CompaniesExpense
from mainpage.models import Portals
from dealcard.views import ObjBitrix24


@xframe_options_exempt
@csrf_exempt
def report_finance(request):
    template: str = 'reports/report_finance.html'

    member_id: str = request.GET.get('member_id')
    portal: Portals = Portals.objects.get(member_id=member_id)

    form: ReportFinanceForm = ReportFinanceForm(request.POST or None)
    context = {
        'form': form,
        'member_id': member_id,
    }
    if not form.is_valid():
        return render(request, template, context)
    deal_type = request.POST.get('deal_type')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    deals_for_reports: list[dict[str, any]] = list(dict())
    expenses_deals = (Expenses.objects
                      .values('deal_id')
                      .filter(portal=portal)
                      .annotate(sum=Sum('expense'))
                      .order_by()
                      )

    if expenses_deals.count() != 0:
        for expense in expenses_deals:
            bx24_obj = ObjBitrix24(portal, expense['deal_id'])
            bx24_obj.get_deal_props()
            if deal_type == 'close' and bx24_obj.deal_props['OPENED'] == 'Y':
                continue
            elif deal_type == 'open' and bx24_obj.deal_props['CLOSED'] == 'Y':
                continue
            deal_date = datetime.datetime.strptime(
                bx24_obj.deal_props['DATE_CREATE'].split('T')[0],
                "%Y-%m-%d").date()
            if not (parse_date(start_date) <= deal_date <= parse_date(end_date)):
                continue

            try:
                bx24_obj.get_user(bx24_obj.deal_props['ASSIGNED_BY_ID'])
            except RuntimeError as err:
                context = {
                    'error_name': 'RuntimeError',
                    'error_description': err.args[1],
                }
                return render(request, 'error.html', context)
            try:
                bx24_obj.get_company(bx24_obj.deal_props['COMPANY_ID'])
            except RuntimeError:
                bx24_obj.company = {
                    'ID': 'error',
                    'TITLE': 'Нет компании в сделке',
                }

            manager = '{name} {last_name}'.format(
                name=bx24_obj.user[0]['NAME'],
                last_name=bx24_obj.user[0]['LAST_NAME']
            )
            company = bx24_obj.company['TITLE']
            company_id = bx24_obj.company['ID']
            opportunity = bx24_obj.deal_props['OPPORTUNITY']
            sum_expenses = expense['sum']
            income = decimal.Decimal(opportunity) - sum_expenses
            profitability = round(income/decimal.Decimal(opportunity)*100)
            deals_for_reports.append(
                {
                    'deal_id': expense['deal_id'],
                    'manager': manager,
                    'opportunity': opportunity,
                    'sum_expenses': sum_expenses,
                    'profitability': profitability,
                    'income': income,
                    'portal_name': portal.name,
                    'company': company,
                    'company_id': company_id,
                }
            )
        context['deals_for_reports'] = deals_for_reports
    return render(request, template, context)


@xframe_options_exempt
@csrf_exempt
def report_buh(request):
    template: str = 'reports/report_buh.html'

    member_id: str = request.GET.get('member_id')
    portal: Portals = Portals.objects.get(member_id=member_id)

    form: ReportBuhForm = ReportBuhForm(request.POST or None)
    context = {
        'form': form,
        'member_id': member_id,
    }
    if not form.is_valid():
        return render(request, template, context)

    expenses_for_reports: list[dict[str, any]] = list(dict())
    expenses_deals = (Expenses.objects
                      .select_related('company')
                      .filter(portal=portal)
                      )
    for expense in expenses_deals:
        if request.POST.get('company'):
            company_pk = int(request.POST.get('company'))
            company = CompaniesExpense.objects.get(pk=company_pk)
            if not expense.company:
                continue
            elif company.pk != expense.company.pk:
                continue
        if request.POST.get('start_date') and request.POST.get('end_date'):
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            if not (parse_date(start_date) <= expense.create_date.date()
                    <= parse_date(end_date)):
                continue
        elif request.POST.get('start_date'):
            start_date = request.POST.get('start_date')
            if parse_date(start_date) > expense.create_date.date():
                continue
        elif request.POST.get('end_date'):
            end_date = request.POST.get('end_date')
            if parse_date(end_date) < expense.create_date.date():
                continue
        if request.POST.get('sum'):
            sum_expense = decimal.Decimal(request.POST.get('sum'))
            if sum_expense != expense.expense:
                continue
        if request.POST.get('no_company_visible') == 'n' and not expense.company:
            continue
        if request.POST.get('document'):
            document = request.POST.get('document')
            if not expense.document:
                continue
            elif not document.lower() in expense.document.lower():
                continue
        expenses_for_reports.append(
            {
                'date': expense.create_date,
                'company': expense.company,
                'company_id': expense.company,
                'deal_id': expense.deal_id,
                'sum_expense': expense.expense,
                'document': expense.document,
                'portal_name': portal.name,
            }
        )
    context['expenses_for_reports'] = expenses_for_reports
    return render(request, template, context)
