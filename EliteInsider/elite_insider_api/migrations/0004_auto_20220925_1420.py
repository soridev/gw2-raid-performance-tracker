# Generated by Django 3.2 on 2022-09-25 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elite_insider_api', '0003_playerinfo_died'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='guildmembers',
            table='guild_members',
        ),
        migrations.AlterModelTable(
            name='mechanicinfo',
            table='mechanic_info',
        ),
        migrations.AlterModelTable(
            name='playerinfo',
            table='player_info',
        ),
        migrations.AlterModelTable(
            name='raidkilltimes',
            table='raid_kill_times',
        ),
    ]