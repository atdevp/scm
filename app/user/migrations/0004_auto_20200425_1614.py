# Generated by Django 3.0.3 on 2020-04-25 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_remove_usermodel_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='mobile',
            field=models.BigIntegerField(blank=True, default=0),
        ),
    ]
