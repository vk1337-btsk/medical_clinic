# Generated by Django 5.0.7 on 2024-08-06 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passport_id', models.IntegerField(db_comment='Даннаые паспорта', verbose_name='Данные паспорта')),
                ('passport_date', models.DateField(db_comment='Дата выдачи паспорта', verbose_name='Дата выдачи паспорта')),
                ('country', models.CharField(blank=True, db_comment='Страна', max_length=255, null=True, verbose_name='Страна')),
                ('city', models.CharField(blank=True, db_comment='Город', max_length=255, null=True, verbose_name='Город')),
                ('street', models.CharField(blank=True, db_comment='Улица', max_length=255, null=True, verbose_name='Улица')),
                ('blood_group', models.CharField(blank=True, db_comment='Группа крови', max_length=2, null=True, verbose_name='Группа крови')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
                'db_table': '_us_clients',
                'db_table_comment': 'Клиенты',
                'ordering': ['passport_id'],
            },
        ),
        migrations.CreateModel(
            name='RegistredServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_services', models.DateTimeField(db_comment='Дата и время записи услуги', verbose_name='Дата записи')),
                ('status_service', models.CharField(db_comment='Статус услуги', default='CR', max_length=15, verbose_name='Статус услуги')),
                ('status_paid', models.BooleanField(blank=True, db_comment='Статус оплаты', null=True, verbose_name='Статус оплаты')),
                ('is_analyz', models.BooleanField(blank=True, db_comment='Флаг анализа', null=True, verbose_name='Флаг анализа')),
                ('is_vizit', models.BooleanField(blank=True, db_comment='Флаг визита', null=True, verbose_name='Флаг визита')),
            ],
            options={
                'verbose_name': 'Зарегистрированная услуга',
                'verbose_name_plural': 'Зарегистрированные услуги',
            },
        ),
    ]