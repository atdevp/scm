# Generated by Django 3.0.3 on 2020-02-19 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='grouphostmodel',
            old_name='t_group',
            new_name='group',
        ),
    ]
