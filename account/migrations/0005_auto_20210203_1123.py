# Generated by Django 3.1.5 on 2021-02-03 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20201125_1829'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='editor_theme',
        ),
        migrations.RemoveField(
            model_name='account',
            name='list_column',
        ),
        migrations.RemoveField(
            model_name='account',
            name='nav_color',
        ),
        migrations.AddField(
            model_name='account',
            name='frontend_config',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='lang',
            field=models.TextField(default='cxx;17,clang,O2'),
        ),
    ]
