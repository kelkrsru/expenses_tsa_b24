from django.db import models

from mainpage.models import Portals, CostItems


class CompaniesExpense(models.Model):
    """Класс Компаний из Битрикс24, которые могут иметь затраты"""

    id_b24 = models.IntegerField(
        verbose_name='ID компании в Битрикс24',
    )
    name = models.CharField(
        verbose_name='Наименование компании',
        max_length=255,
    )
    portal = models.ForeignKey(
        Portals,
        verbose_name='Портал',
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
        unique_together = ['id_b24', 'portal']
        ordering = ['portal']

    def __str__(self):
        return self.name


class Cargo(models.Model):
    """Класс полученных грузов из Битрикс24"""

    id_b24 = models.IntegerField(
        verbose_name='ID компании в Битрикс24',
    )
    number = models.CharField(
        verbose_name='Номер груза',
        max_length=10
    )
    portal = models.ForeignKey(
        Portals,
        verbose_name='Портал',
        on_delete=models.PROTECT,
    )
    deal_id = models.IntegerField(
        verbose_name='ID сделки в Битрикс24'
    )

    class Meta:
        verbose_name = 'Груз'
        verbose_name_plural = 'Грузы'
        unique_together = ['id_b24', 'portal']
        ordering = ['portal', 'deal_id']

    def __str__(self):
        return self.number


class Employee(models.Model):
    """Класс сотрудников из Битрикс24"""

    id_b24 = models.IntegerField(
        verbose_name='ID сотрудника в Битрикс24',
    )
    name = models.CharField(
        verbose_name='Имя',
        max_length=50,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=50,
    )
    portal = models.ForeignKey(
        Portals,
        verbose_name='Портал',
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        unique_together = ['id_b24', 'portal']
        ordering = ['portal']

    def __str__(self):
        return '{name} {last_name}'.format(name=self.name,
                                           last_name=self.last_name)


class Expenses(models.Model):
    product_id = models.IntegerField(
        verbose_name='ID услуги',
    )
    cost_item = models.ForeignKey(
        CostItems,
        verbose_name='Статья затрат',
        on_delete=models.PROTECT,
        related_name='cost_items',
    )
    deal_id = models.IntegerField(
        verbose_name='ID сделки',
    )
    expense = models.DecimalField(
        verbose_name='Сумма',
        max_digits=12,
        decimal_places=2,
        null=True,
    )
    cargo = models.ForeignKey(
        Cargo,
        verbose_name='Груз',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    company = models.ForeignKey(
        CompaniesExpense,
        verbose_name='Компания',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    employee = models.ForeignKey(
        Employee,
        verbose_name='Сотрудник',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='employee'
    )
    type_cost = models.CharField(
        verbose_name='Вид оплаты',
        max_length=50,
        choices=[('Наличный', 'Наличный')],
        blank=True,
        null=True,
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )
    update_date = models.DateTimeField(
        verbose_name='Дата изменения',
        auto_now=True,
    )
    owner = models.ForeignKey(
        Employee,
        verbose_name='Создатель',
        on_delete=models.PROTECT,
        related_name='owner',
    )
    portal = models.ForeignKey(
        Portals,
        verbose_name='Портал',
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = 'Затраты'
        verbose_name_plural = 'Затраты'
        ordering = ['update_date']

    def __str__(self):
        return 'Затраты #{pk}'.format(pk=self.pk)
