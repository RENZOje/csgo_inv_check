# Generated by Django 3.0.6 on 2020-06-05 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0006_query_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='time_q',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
