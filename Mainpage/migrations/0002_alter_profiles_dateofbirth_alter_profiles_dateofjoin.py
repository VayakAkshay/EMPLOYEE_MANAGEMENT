# Generated by Django 4.1.6 on 2023-02-11 10:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mainpage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profiles',
            name='dateofbirth',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='dateofjoin',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
