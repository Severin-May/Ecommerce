# Generated by Django 4.2.16 on 2024-11-30 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_order_orderitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='address1',
            new_name='address',
        ),
    ]