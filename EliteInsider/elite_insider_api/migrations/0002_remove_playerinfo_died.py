# Generated by Django 3.2 on 2022-09-03 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elite_insider_api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playerinfo',
            name='died',
        ),
    ]
