# Generated by Django 3.1.8 on 2021-04-16 05:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_account_avatar_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='frontend_config',
            new_name='extra_data',
        ),
    ]