from django import forms

from dealcard.models import CompaniesExpense


class ReportFinanceForm(forms.Form):
    """Форма параметров отчета финансиста"""

    DEAL_TYPE_CHOICES = [
        ('close', 'Закрытые'),
        ('open', 'Открытые'),
        ('all', 'Все'),
    ]

    deal_type = forms.ChoiceField(
        label='Тип сделок',
        choices=DEAL_TYPE_CHOICES,
    )

    start_date = forms.DateField(
        label='Начальная дата',
        widget=forms.widgets.DateInput(attrs={
            'type': 'date',
            'class': 'form-control datepicker-input',
        })
    )

    end_date = forms.DateField(
        label='Конечная дата',
        widget=forms.widgets.DateInput(attrs={
            'type': 'date',
            'class': 'form-control datepicker-input',
        })
    )


class ReportBuhForm(forms.Form):
    """Форма параметров отчета бухгалтера"""

    NO_COMPANY_VISIBLE_CHOICES = [
        ('y', 'Показывать'),
        ('n', 'Не показывать'),
    ]

    start_date = forms.DateField(
        label='Начальная дата',
        widget=forms.widgets.DateInput(attrs={
            'type': 'date',
            'class': 'form-control datepicker-input',
        }),
        required=False,
    )

    end_date = forms.DateField(
        label='Конечная дата',
        widget=forms.widgets.DateInput(attrs={
            'type': 'date',
            'class': 'form-control datepicker-input',
        }),
        required=False,
    )

    no_company_visible = forms.ChoiceField(
        label='Показывать без поставщика',
        choices=NO_COMPANY_VISIBLE_CHOICES,
    )

    company = forms.ModelChoiceField(
        label='Поставщик',
        queryset=CompaniesExpense.objects.all(),
        required=False,
    )

    document = forms.CharField(
        label='Документ',
        required=False,
    )

    sum = forms.DecimalField(
        label='Сумма',
        required=False,
    )
