from django.contrib import admin
from .models import Expenses, CompaniesExpense, Cargo, Employee, Deal


class ExpensesAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'create_date',
        'update_date',
        'portal',
        'deal_id',
    )


class DealAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'create_date',
        'update_date',
        'portal',
        'deal_id',
    )


class CompaniesExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'id_b24',
        'name',
        'portal',
    )


class CargoAdmin(admin.ModelAdmin):
    list_display = (
        'id_b24',
        'number',
        'portal',
        'deal_id',
    )


class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'id_b24',
        'name',
        'last_name',
        'portal',
    )


admin.site.register(Expenses, ExpensesAdmin)
admin.site.register(Deal, DealAdmin)
admin.site.register(CompaniesExpense, CompaniesExpenseAdmin)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(Employee, EmployeeAdmin)
