# Generated by Django 4.1 on 2022-08-06 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_cartitem_variation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='is_acitve',
            new_name='is_active',
        ),
    ]
