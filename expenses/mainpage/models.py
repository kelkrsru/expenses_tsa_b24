from django.db import models


class Portals(models.Model):
    member_id = models.CharField(
        verbose_name='Уникальный код портала',
        max_length=255,
        unique=True,
    )
    name = models.CharField(
        verbose_name='Имя портала',
        max_length=255,
    )
    auth_id = models.CharField(
        verbose_name='Токен аутентификации',
        max_length=255,
    )
    auth_id_create_date = models.DateTimeField(
        verbose_name='Дата получения токена аутентификации',
        auto_now=True,
    )
    refresh_id = models.CharField(
        verbose_name='Токен обновления',
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
    )
    portal = models.ForeignKey(
        Portals,
        verbose_name='Портал',
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = 'Статья затрат'
        verbose_name_plural = 'Статьи затрат'
        unique_together = ['name', 'portal']
        ordering = ['name']

    def __str__(self):
        return self.name
