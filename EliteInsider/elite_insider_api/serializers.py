from django.forms import FileField
from rest_framework import serializers
from .models import GuildMembers, MechanicInfo, PlayerInfo, RaidEncounters, RaidKillTimes


class GuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuildMembers
        fields = [
            "guild_name",
        ]


class GuildMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuildMembers
        fields = [
            "guild_name",
            "account_name",
        ]


class RaidKillTimesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaidKillTimes
        fields = [
            "log_id",
            "encounter_name",
            "qualifying_date",
            "start_time",
            "end_time",
            "kill_duration_seconds",
            "success",
            "cm",
            "input_file",
            "link_to_upload",
        ]


class MechanicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MechanicInfo
        fields = ["log_id", "encounter_name", "mechanic_name", "mechanic_description", "time_info", "actor"]


class PlayerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerInfo
        fields = [
            "log_id",
            "account_name",
            "character_name",
            "profession",
            "target_dps",
            "total_cc",
            "downstates",
            "died",
        ]


class RaidEncounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaidEncounters
        fields = [
            "encounter_name",
            "arc_folder_name",
            "has_cm",
            "raid_wing",
            "boss_position",
            "relevant_boss",
            "wing_name",
        ]


class FullclearStatsSerializer(serializers.Serializer):
    qualifying_date = serializers.DateField()
    encounter_name = serializers.CharField()
    cm = serializers.BooleanField()
    kd_sec = serializers.DecimalField(16, 2)


class UploadSerializer(serializers.Serializer):
    file_uploaded = FileField()

    class Meta:
        fields = ["file_uploaded"]
