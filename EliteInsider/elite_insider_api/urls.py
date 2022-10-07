from django.urls import path
from .views import (
    Entrypoint,
    GuildMembersDetailsView,
    GuildMembersView,
    GuildsView,
    MechanicInfoDetailsView,
    PlayerInfoDetailsView,
    PlayerInfoView,
    RaidKillTimesDetailsView,
    RaidKillTimesView,
    MechanicInfoView,
    FullclearStatsDetailsView,
    RaidEncountersView,
    RaidEncountersDetailsView,
    UploadView,
)

urlpatterns = [
    path("", Entrypoint, name="elite-api"),
    path("log-registry/", RaidKillTimesView.as_view()),
    path("log-registry/<str:log_id>/", RaidKillTimesDetailsView.as_view()),
    path("guilds/", GuildsView.as_view()),
    path("guild-members/", GuildMembersView.as_view()),
    path("guild-members/<str:guild_name>/", GuildMembersDetailsView.as_view()),
    path("mechanic-info/", MechanicInfoView.as_view()),
    path("mechanic-info/<str:log_id>/", MechanicInfoDetailsView.as_view()),
    path("player-info/", PlayerInfoView.as_view()),
    path("player-info/<str:log_id>/", PlayerInfoDetailsView.as_view()),
    path("fullclear-stats/<str:guild_name>/", FullclearStatsDetailsView.as_view()),
    path("raid-encounters/", RaidEncountersView.as_view()),
    path("raid-encounters/<str:encounter_name>/", RaidEncountersDetailsView.as_view()),
    path("upload/", UploadView.as_view()),
]
