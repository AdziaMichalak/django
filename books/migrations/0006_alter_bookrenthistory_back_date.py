# Generated by Django 3.2.15 on 2022-08-24 06:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_auto_20220823_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookrenthistory',
            name='back_date',
            field=models.DateField(default=datetime.datetime(2022, 9, 23, 8, 15, 29, 398565)),
        ),
    ]