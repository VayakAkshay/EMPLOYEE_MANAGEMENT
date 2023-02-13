# Generated by Django 4.1.6 on 2023-02-13 04:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mainpage', '0008_leavemanager_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='attendacemanager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_date', models.DateField(default=datetime.date.today)),
                ('arrival_time', models.TimeField(default='09:44:16')),
                ('emp_id', models.IntegerField(default=0)),
            ],
        ),
    ]