# Generated by Django 3.1.5 on 2021-02-04 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0014_auto_20210203_1619'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='problem',
            options={'permissions': (('view_hidden', 'Can view hidden problem'), ('download_testdata', 'Can download problem testdata'))},
        ),
    ]
