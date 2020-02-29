# Generated by Django 3.0.3 on 2020-02-25 05:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200225_1059'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='city',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.City', verbose_name='city'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='serviceprovider',
            name='area',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.Area', verbose_name='area'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='serviceprovider',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.City', verbose_name='city'),
        ),
    ]