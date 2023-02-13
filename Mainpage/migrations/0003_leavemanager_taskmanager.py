# Generated by Django 4.1.6 on 2023-02-11 10:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mainpage', '0002_alter_profiles_dateofbirth_alter_profiles_dateofjoin'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_reasion', models.TextField(default='', max_length=500)),
                ('start_date', models.DateField(default=datetime.date.today)),
                ('end_date', models.DateField(default=datetime.date.today)),
                ('emp_id', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='TaskManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.TextField(default='', max_length=100)),
                ('start_date', models.DateField(default=datetime.date.today)),
                ('end_date', models.DateField(default=datetime.date.today)),
                ('emp_id', models.IntegerField(default=0)),
            ],
        ),
    ]