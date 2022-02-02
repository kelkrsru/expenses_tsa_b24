from django import forms

from .models import CostItems


class AddCostItemForm(forms.ModelForm):
    """Форма добавления Статьи затрат"""

    class Meta:
        model = CostItems
        fields = ('name',)


class ListCostItemForm(forms.ModelForm):
    """Форма просмотра существующих Статей затрат"""

    cost_items = forms.ModelChoiceField(
        queryset=CostItems.objects.all(),
        label='Статьи затрат',
        empty_label=None,
        widget=forms.SelectMultiple(),
    )

    class Meta:
        model = CostItems
        fields = ('cost_items',)
