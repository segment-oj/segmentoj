# Generated by Django 3.1rc1 on 2020-07-31 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('captcha', '0003_auto_20200729_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='captchastore',
            name='key',
            field=models.IntegerField(unique=True),
        ),
    ]
