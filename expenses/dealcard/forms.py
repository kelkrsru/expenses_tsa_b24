from django import forms

from .models import Expenses, Cargo, CompaniesExpense, Employee


class ExpensesForm(forms.ModelForm):
    """Форма Затрат для услуги"""

    count = forms.DecimalField(
        min_value=0,
        max_digits=10,
        decimal_places=2,
        label='Количество',
        required=False,
    )
    price = forms.DecimalField(
        min_value=0,
        max_digits=10,
        decimal_places=2,
        label='Цена',
        required=False,
    )

    def __init__(self, *args, **kwargs):
        portal = kwargs.pop('portal')
        deal_id = kwargs.pop('deal_id')
        super(ExpensesForm, self).__init__(*args, **kwargs)
        self.fields['cost_item'].empty_label = None
        self.fields['cargo'] = forms.ModelChoiceField(
            required=False,
            queryset=Cargo.objects.filter(portal=portal, deal_id=deal_id),
            label='Груз'
        )
        self.fields['company'] = forms.ModelChoiceField(
            required=False,
            queryset=CompaniesExpense.objects.filter(portal=portal),
            label='Компания'
        )
        self.fields['employee'] = forms.ModelChoiceField(
            required=False,
            queryset=Employee.objects.filter(portal=portal),
            label='Сотрудник'
        )

    class Meta:
        model = Expenses
        fields = ('cost_item', 'count', 'price', 'expense', 'cargo', 'company',
                  'employee', 'type_cost', 'document')
