# Generated by Django 4.1 on 2022-08-23 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_reviewrating'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='shoes_pair',
            field=models.BooleanField(default=False),
        ),
    ]
