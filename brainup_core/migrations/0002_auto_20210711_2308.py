# Generated by Django 3.2.5 on 2021-07-11 18:08

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brainup_core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='brainup_core.cardscollection'),
        ),
        migrations.AlterField(
            model_name='card',
            name='entry_date',
            field=models.DateField(default=datetime.datetime(2021, 7, 11, 23, 8, 29, 464476)),
        ),
    ]
