# Generated by Django 3.2.15 on 2022-08-23 18:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_auto_20220823_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='comment',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Komentarz'),
        ),
        migrations.AlterField(
            model_name='bookrenthistory',
            name='back_date',
            field=models.DateField(default=datetime.datetime(2022, 9, 22, 20, 32, 22, 320885)),
        ),
    ]
