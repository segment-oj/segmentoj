# Generated by Django 3.0.3 on 2020-02-20 10:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import soj.storage


class Migration(migrations.Migration):

    dependencies = [
        ('soj', '0002_auto_20200220_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='uid',
            field=models.IntegerField(default=8),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='account',
            name='avatar',
            field=models.FileField(storage=soj.storage.AvatarStorage(uid=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='account', to=settings.AUTH_USER_MODEL)), upload_to='avatar'),
        ),
    ]
