# Generated by Django 4.0.1 on 2022-02-14 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Portals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_id', models.CharField(max_length=255, verbose_name='Уникальный код портала')),
                ('name', models.CharField(max_length=255, verbose_name='Имя портала')),
                ('auth_id', models.CharField(max_length=255, verbose_name='Токен аутентификации')),
                ('auth_id_create_date', models.DateTimeField(auto_now=True, verbose_name='Дата получения токена аутентификации')),
                ('refresh_id', models.CharField(max_length=255, verbose_name='Токен обновления')),
            ],
            options={
                'verbose_name': 'Портал',
                'verbose_name_plural': 'Порталы',
            },
        ),
        migrations.CreateModel(
            name='CostItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите наименование статьи затрат', max_length=200, unique=True, verbose_name='Наименование')),
                ('portal_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mainpage.portals', verbose_name='Портал')),
            ],
            options={
                'verbose_name': 'Статья затрат',
                'verbose_name_plural': 'Статьи затрат',
                'ordering': ['name'],
            },
        ),
    ]
