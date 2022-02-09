from django.contrib import admin
from .models import CostItems, Portals, Expenses


class PortalsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'member_id',
        'url',
        'name',
    )


class CostItemsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
    )


class ExpensesAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'create_date',
        'update_date',
        'portal_id',
        'deal_id',
    )


admin.site.register(CostItems, CostItemsAdmin)
admin.site.register(Portals, PortalsAdmin)
admin.site.register(Expenses, ExpensesAdmin)
