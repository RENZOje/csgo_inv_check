# Generated by Django 3.0.6 on 2020-06-12 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0015_profile_friend_search'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='friend_search',
            field=models.TextField(blank=True, default='[]', null=True),
        ),
    ]