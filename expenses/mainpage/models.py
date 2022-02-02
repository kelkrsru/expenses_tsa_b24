from django.db import models


class Portals(models.Model):
    member_id = models.CharField(
        verbose_name='Уникальный код портала',
        max_length=255,
    )
    url = models.URLField(
        verbose_name='Адрес портала',
        max_length=255,
    )
    name = models.CharField(
        verbose_name='Имя портала',
        max_length=255,
    )

    class Meta:
        verbose_name = 'Портал'
        verbose_name_plural = 'Порталы'

    def __str__(self):
        return self.name


class CostItems(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Наименование',
        help_text='Введите наименование статьи затрат',
        unique=True,
    )
    portal_id = models.ForeignKey(
        Portals,
        verbose_name='Портал',
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = 'Статья затрат'
        verbose_name_plural = 'Статьи затрат'
        ordering = ['name']

    def __str__(self):
        return self.name


class Expenses(models.Model):
    product_id = models.IntegerField(
        verbose_name='ID услуги',
    )
    cost_item_id = models.ForeignKey(
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
    cargo_id = models.IntegerField(
        verbose_name='ID груза',
        null=True,
        blank=True,
    )
    cargo_number = models.CharField(
        verbose_name='Номер груза',
        max_length=8,
        null=True,
        blank=True,
    )
    company_name = models.CharField(
        verbose_name='Компания',
        max_length=255,
        null=True,
        blank=True,
    )
    employee_id = models.IntegerField(
        verbose_name='ID сотрудника',
        null=True,
        blank=True,
    )
    employee_name = models.CharField(
        verbose_name='ФИО сотрудника',
        max_length=255,
        null=True,
        blank=True,
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )
    update_date = models.DateTimeField(
        verbose_name='Дата изменения',
        auto_now=True,
    )
    owner_id = models.IntegerField(
        verbose_name='ID пользователя',
    )
    owner_name = models.CharField(
        verbose_name='ФИО пользователя',
        max_length=255,
    )
    portal_id = models.ForeignKey(
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
