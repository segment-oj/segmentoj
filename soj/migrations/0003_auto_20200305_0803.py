# Generated by Django 3.0.3 on 2020-03-05 00:03

from django.db import migrations, models
import soj.storage


class Migration(migrations.Migration):

    dependencies = [
        ('soj', '0002_auto_20200220_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='lang',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='account',
            name='avatar',
            field=models.FileField(storage=soj.storage.AvatarStorage(), upload_to='avatar'),
        ),
    ]