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

    log_id = models.CharField(max_length=100, blank=False, null=False, primary_key=True)
    encounter_name = models.CharField(max_length=500, null=False)
    qualifying_date = models.DateField(null=False)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    kill_duration_seconds = models.FloatField(null=False)
    success = models.BooleanField(null=False)
    cm = models.BooleanField(null=False)
    input_file = models.CharField(max_length=1000, null=False)
    link_to_upload = models.CharField(max_length=500, null=True)
    uploaded_by = models.CharField(max_length=500, null=False, default="admin")


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

class UserProfiles(models.Model):
    class Meta:
        db_table = "user_profiles"

    username = models.CharField(max_length=200, blank=False, primary_key=True)
    account_name = models.CharField(max_length=200, blank=False, null=False)
    gw2_api_key = models.CharField(max_length=200, blank=False, null=True)
