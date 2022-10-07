from unittest.util import _MAX_LENGTH
from django.db import models


class GuildMembers(models.Model):
    guild_name = models.CharField(max_length=300, blank=False)
    account_name = models.CharField(max_length=300, blank=False)

    class Meta:
        db_table = "guild_members"
        constraints = [
            models.UniqueConstraint(fields=["guild_name", "account_name"], name="unique_active_guildmembers")
        ]


class RaidKillTimes(models.Model):
    class Meta:
        db_table = "raid_kill_times"

    log_id = models.CharField(max_length=100, blank=False, primary_key=True)
    encounter_name = models.CharField(max_length=500, blank=False)
    qualifying_date = models.DateField(blank=False)
    start_time = models.DateTimeField(blank=False)
    end_time = models.DateTimeField(blank=False)
    kill_duration_seconds = models.FloatField(blank=False)
    success = models.BooleanField(blank=False)
    cm = models.BooleanField(blank=False)
    input_file = models.CharField(max_length=1000, blank=False)
    link_to_upload = models.CharField(max_length=500, blank=True, null=True)


class MechanicInfo(models.Model):
    class Meta:
        db_table = "mechanic_info"

    log_id = models.CharField(max_length=100, blank=False)
    encounter_name = models.CharField(max_length=500, blank=False)
    mechanic_name = models.CharField(max_length=1000, blank=False)
    mechanic_description = models.CharField(max_length=1000, blank=False)
    time_info = models.FloatField(blank=False)
    actor = models.CharField(max_length=300, blank=False)


class PlayerInfo(models.Model):
    class Meta:
        db_table = "player_info"

    log_id = models.CharField(max_length=100, blank=False)
    account_name = models.CharField(max_length=300, blank=False)
    character_name = models.CharField(max_length=300, blank=False)
    profession = models.CharField(max_length=300, blank=False)
    target_dps = models.FloatField(blank=False)
    total_cc = models.FloatField(blank=False)
    downstates = models.IntegerField(blank=False)
    died = models.BooleanField(blank=False)


class RaidEncounters(models.Model):
    class Meta:
        db_table = "raid_encounters"

    encounter_name = models.CharField(max_length=200, blank=False, primary_key=True)
    arc_folder_name = models.CharField(max_length=200, blank=False)
    has_cm = models.BooleanField(blank=False)
    raid_wing = models.IntegerField(blank=False)
    boss_position = models.IntegerField(blank=False)
    relevant_boss = models.BooleanField(blank=False)
    wing_name = models.CharField(max_length=100, blank=False)
