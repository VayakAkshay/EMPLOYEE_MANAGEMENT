# Generated by Django 4.1.6 on 2023-02-12 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mainpage', '0006_alter_profiles_profile_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='profiles',
            name='profile_id',
            field=models.IntegerField(default=0),
        ),
    ]
