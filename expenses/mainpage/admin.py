from django.contrib import admin
from .models import CostItems, Portals


class PortalsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'member_id',
        'name',
        'auth_id_create_date',
    )


class CostItemsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
    )


admin.site.register(CostItems, CostItemsAdmin)
admin.site.register(Portals, PortalsAdmin)
