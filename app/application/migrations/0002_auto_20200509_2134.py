# Generated by Django 3.0.3 on 2020-05-09 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationmodel',
            name='pro_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='project.ProjectModel'),
        ),
    ]
