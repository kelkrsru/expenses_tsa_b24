from django import forms

from .models import CostItems


class AddCostItemForm(forms.ModelForm):
    """Форма добавления Статьи затрат"""

    class Meta:
        model = CostItems
        fields = ('name', 'portal')
        widgets = {
            'portal': forms.HiddenInput(),
        }


class CostItemForm(forms.ModelForm):
    """Форма просмотра существующих Статей затрат"""

    def __init__(self, *args, **kwargs):
        portal = kwargs.pop('portal')
        super(CostItemForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.ModelChoiceField(
            queryset=CostItems.objects.filter(portal=portal),
            label='Статьи затрат',
            empty_label=None,
            widget=forms.SelectMultiple(),
        )

    class Meta:
        model = CostItems
        fields = ('name',)
