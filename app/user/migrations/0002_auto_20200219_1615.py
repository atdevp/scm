# Generated by Django 3.0 on 2020-02-19 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='mobile',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
