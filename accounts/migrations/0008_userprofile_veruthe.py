# Generated by Django 4.1 on 2022-08-26 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_rename_mobile_phone_userprofile_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='veruthe',
            field=models.CharField(blank=True, max_length=302),
        ),
    ]
