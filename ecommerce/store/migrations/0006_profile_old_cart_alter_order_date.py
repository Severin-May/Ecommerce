# Generated by Django 4.2.16 on 2024-11-16 21:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_order_date_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='old_cart',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 11, 16, 22, 46, 25, 448654)),
        ),
    ]
