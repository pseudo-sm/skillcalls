# Generated by Django 3.0.3 on 2020-02-28 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_customer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': 'Customer', 'verbose_name_plural': 'Customers'},
        ),
        migrations.RemoveField(
            model_name='customer',
            name='name',
        ),
    ]
