# Generated by Django 3.0.3 on 2020-04-20 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20200219_1615'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermodel',
            name='role',
        ),
    ]