# Generated by Django 4.2.1 on 2023-05-26 08:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_company_options_alter_ride2passengers_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='destination_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='ride',
            name='spots',
            field=models.IntegerField(default=4),
        ),
    ]
