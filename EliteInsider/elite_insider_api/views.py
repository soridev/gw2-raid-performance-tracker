import os
import shutil
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from elite_insider_api.models import RaidKillTimes, GuildMembers, MechanicInfo, PlayerInfo, RaidEncounters, UserProfiles
from rest_framework import permissions
from .custom_filters import EICustomFilters
from .serializers import *

# import celery tasks
from celery import chain
from tasks import generate_evtc_raw_data, json_to_rdbms

class RaidKillTimesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        killtimes = RaidKillTimes.objects.filter(uploaded_by=request.user.username)
        serializer = RaidKillTimesSerializer(killtimes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RaidKillTimesDetailsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, log_id, user_id):
        """Helper method to get the object with given log_id."""
        try:
            return RaidKillTimes.objects.get(log_id=log_id, uploaded_by=user_id)
        except RaidKillTimes.DoesNotExist:
            return None

    def get(self, request, log_id, *args, **kwargs):
        """Retrieves the log with given log_id."""
        rkt_instance = self.get_object(log_id, user_id=request.user.username)
        if not rkt_instance:
            return Response({"res": "Object with this log-id does not exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RaidKillTimesSerializer(rkt_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GuildsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        guilds = GuildMembers.objects.distinct("guild_name")

        serializer = GuildSerializer(guilds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GuildMembersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        guildmembers = GuildMembers.objects.all()
        serializer = GuildMembersSerializer(guildmembers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GuildMembersDetailsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, guild_name):
        try:
            return GuildMembers.objects.filter(guild_name=guild_name)
        except GuildMembers.DoesNotExist:
            return None

    def get(self, request, guild_name, *args, **kwargs):
        guild_instance = self.get_object(guild_name)
        if not guild_instance:
            return Response({"res": "Object with this guild-name does not exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = GuildMembersSerializer(guild_instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MechanicInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        mechanic_infos = MechanicInfo.objects.all()
        serializer = MechanicInfoSerializer(mechanic_infos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MechanicInfoDetailsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, log_id):
        try:
            return MechanicInfo.objects.filter(log_id=log_id)
        except MechanicInfo.DoesNotExist:
            return None

    def get(self, request, log_id, *args, **kwargs):
        mechanic_infos = self.get_object(log_id)
        if not mechanic_infos:
            return Response({"res": "Object with this guild-name does not exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MechanicInfoSerializer(mechanic_infos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlayerInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        player_infos = PlayerInfo.objects.all()
        serializer = PlayerInfoSerializer(player_infos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlayerInfoDetailsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, log_id):
        try:
            return PlayerInfo.objects.filter(log_id=log_id)
        except PlayerInfo.DoesNotExist:
            return None

    def get(self, request, log_id, *args, **kwargs):
        player_infos = self.get_object(log_id)
        if not player_infos:
            return Response({"res": "Object with this log-id does not exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PlayerInfoSerializer(player_infos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # # 4. Update
    # def put(self, request, todo_id, *args, **kwargs):
    #     """
    #     Updates the todo item with given todo_id if exists
    #     """
    #     todo_instance = self.get_object(todo_id, request.user.id)
    #     if not todo_instance:
    #         return Response({"res": "Object with todo id does not exists"}, status=status.HTTP_400_BAD_REQUEST)
    #     data = {"task": request.data.get("task"), "completed": request.data.get("completed"), "user": request.user.id}
    #     serializer = TodoSerializer(instance=todo_instance, data=data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # # 5. Delete
    # def delete(self, request, todo_id, *args, **kwargs):
    #     """
    #     Deletes the todo item with given todo_id if exists
    #     """
    #     todo_instance = self.get_object(todo_id, request.user.id)
    #     if not todo_instance:
    #         return Response({"res": "Object with todo id does not exists"}, status=status.HTTP_400_BAD_REQUEST)
    #     todo_instance.delete()
    #     return Response({"res": "Object deleted!"}, status=status.HTTP_200_OK)

class RaidEncountersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        raid_encounters = RaidEncounters.objects.all().order_by("raid_wing", "boss_position")
        serializer = RaidEncounterSerializer(raid_encounters, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RaidEncountersDetailsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, encounter_name):
        try:
            return RaidEncounters.objects.filter(encounter_name=encounter_name)
        except RaidEncounters.DoesNotExist:
            return None

    def get(self, request, encounter_name, *args, **kwargs):
        raid_encounter = self.get_object(encounter_name)
        if not raid_encounter:
            return Response({"res": "Object with this log-id does not exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RaidEncounterSerializer(raid_encounter, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UploadSerializer

    def get(self, request):
        return Response("There is no GET data for this request.")

    def post(self, request):
        
        fs = FileSystemStorage()
        given_file = request.FILES["file"]        
        file_name = fs.save(given_file.name, given_file)

        source = os.path.join(settings.MEDIA_ROOT, file_name)
        target = os.path.join(settings.LOG_LANDINGZONE, file_name)

        # move file to landingzone
        shutil.move(source, target)

        # trigger log handling in celery
        chain(generate_evtc_raw_data.s(file_path=target, settings_file=settings.EI_SETTINGS_FILE),
            json_to_rdbms.s()).apply_async()

        response = "Upload successful."
        return Response(response)

#
# Custom filter section
#

class LogCount(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        log_count = EICustomFilters().get_log_count()

        if log_count is None:
            print(log_count)
            return Response({"res": "Unable to fetch the number of logs."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'log_count': log_count}, status=status.HTTP_200_OK)

class LogCountDetailsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        log_count = EICustomFilters().get_log_count(user_id=request.user.username)

        if log_count is None:
            return Response({"res": "Unable to fetch the number of logs for the given user."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'user': request.user.username, 'log_count': log_count}, status=status.HTTP_200_OK)

class FullclearStatsDetailsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, guild_name, *args, **kwargs):
        yearweek_filter = self.request.query_params.get("yearweek")
        fullclear_stats = EICustomFilters().get_fullclear_stats(guild_name, week=yearweek_filter)

        if not fullclear_stats:
            return Response({"res": "Object with this guild-name does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = FullclearStatsSerializer(fullclear_stats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FullclearWingStatsDetailsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, guild_name, *args, **kwargs):        
        yearweek_filter = self.request.query_params.get("yearweek")
        wing_stats = EICustomFilters().get_wing_stats(guild_name=guild_name, week=yearweek_filter)

        if not wing_stats:
            return Response({"res": "Object with this guild-name does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = WingStatSerializer(wing_stats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserProfilesDetailsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, username):
        try:
            return UserProfiles.objects.get(username=username)
        except UserProfiles.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        user_profile = self.get_object(request.user.username)
        if not user_profile:
            return Response({"res": "This user has no configured profile yet."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserGuildsDetailsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_account_name(self, username):
        try:
            up = UserProfiles.objects.get(username=username)
            data = UserProfileSerializer(up).data
            return data["account_name"]

        except UserProfiles.DoesNotExist:
            return None


    def get_object(self, account_name):
        try:
            user_guilds = EICustomFilters().get_users_guilds(account_name)
            return user_guilds
        except Exception as err:
            return None

    def get(self, request, *args, **kwargs):
        account_name = self.get_account_name(request.user.username)
        user_guilds = self.get_object(account_name)

        if not user_guilds:
            return Response({"res": "This user has no configured guilds.", "status_code": 404}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserGuildsSerializer(user_guilds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#
# Entrypoint config.
#

def Entrypoint(request):
    return HttpResponse("Welcome to the elite-api.")
