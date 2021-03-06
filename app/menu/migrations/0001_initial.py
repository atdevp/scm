# Generated by Django 3.0.3 on 2020-05-02 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MenuModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=60, unique=True)),
                ('show_name', models.CharField(max_length=60)),
                ('is_has_son', models.SmallIntegerField()),
                ('parent_id', models.IntegerField()),
                ('url', models.CharField(max_length=255)),
                ('is_new_blank', models.SmallIntegerField()),
                ('icon', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'tb_menu',
                'managed': True,
            },
        ),
    ]
