# Generated by Django 3.2 on 2022-10-30 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elite_insider_api', '0007_auto_20221012_1658'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfiles',
            fields=[
                ('username', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('account_name', models.CharField(max_length=200)),
                ('gw2_api_key', models.CharField(max_length=200, null=True)),
            ],
            options={
                'db_table': 'user_profiles',
            },
        ),
    ]
