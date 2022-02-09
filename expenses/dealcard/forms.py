from django import forms

from mainpage.models import Expenses


class AddExpensesForm(forms.ModelForm):
    """Форма добавления Затрат для услуги"""

    cargo_number = forms.ChoiceField(
        label='Номер груза',
        required=False,
        widget=forms.Select(),
    )

    def __init__(self, *args, **kwargs):
        super(AddExpensesForm, self).__init__(*args, **kwargs)
        self.fields['cost_item_id'].empty_label = None
        self.fields['cargo_number'].choices = [('', 'Не выбрано')]
        self.fields['cargo_number'].choices += Expenses.objects.values_list(
            'pk', 'cost_item_id')

    class Meta:
        model = Expenses
        fields = ('cost_item_id', 'expense', 'cargo_number', 'company_name',
                  'employee_name')
