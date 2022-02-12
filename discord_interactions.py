import os
import json
from zoneinfo import InvalidTZPathWarning
import discord
import argparse

from discord.ext import tasks
from typing import List

from numpy import require

from arc_data_transformator import ArcDataTransformator

from config_helper import ConfigHelper
from application_logging import init_logger

logger = init_logger(logger_name="discord_interactions")


class RaidHelperClient(discord.Client):
    def __init__(self, fc_dates: List[str], fc_guild_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.test_channel_token = int(ConfigHelper().get_config_item("discord-bot", "testing_channel"))
        self.fc_tempfile = os.path.join(
            os.path.dirname(__file__), ConfigHelper().get_config_item("discord-bot", "temp_file_location")
        )
        self.fc_embed = None
        self.fc_dates = fc_dates
        self.fc_guild_name = fc_guild_name
        self.current_json = None
        self.adt = ArcDataTransformator()

        # start the task to run in the background
        self.my_background_task.start()

    async def on_ready(self):
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")

    @tasks.loop(seconds=10)  # task runs every x seconds
    async def my_background_task(self):

        channel = self.get_channel(self.test_channel_token)  # channel ID goes here

        # update statusfile to current status
        self.adt.manage_fullclear_status(self.fc_dates, self.fc_guild_name)
        data = None

        # load json status-file
        with open(self.fc_tempfile, "r") as status_file:
            data = json.load(status_file)

        # check if json changed
        if data != self.current_json:

            # create discord embed
            discord_embed = discord.Embed(
                title=f"""{self.fc_guild_name} [{','.join(self.fc_dates)}]""",
                color=0x00FDFD,
            )

            deimos_info = next((item for item in data if item["encounter_name"] == "Deimos"), None)
            discord_embed.add_field(
                name="W4",
                value=f"""{deimos_info["encounter_name"]} [{deimos_info["duration"]} seconds] - {deimos_info["upload_link"]}""",
                inline=True,
            )

            if self.fc_embed:
                await self.fc_embed.edit(embed=discord_embed)
            else:
                self.fc_embed = await channel.send(embed=discord_embed)

            self.current_json = data

            # discord_embed.add_field(name="W1", value="Vale Guardian\nGorseval\nSabetha", inline=True)
            # discord_embed.add_field(name="W2", value="Vale Guardian\nGorseval\nSabetha", inline=True)
            # discord_embed.add_field(name="W3", value="Vale Guardian\nGorseval\nSabetha", inline=True)
            # discord_embed.add_field(name="W4", value="Vale Guardian\nGorseval\nSabetha", inline=True)

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in


def startup_fc_watcher(fc_dates: List[str], guild_name: str):
    discord_server_token = ConfigHelper().get_config_item("discord-bot", "discord_token")

    client = RaidHelperClient(fc_dates=fc_dates, fc_guild_name=guild_name)
    client.run(discord_server_token)


def main():
    """Startup the discord bot to update and manage messages for a fullclear."""

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--fc-dates",
        dest="fc_dates",
        help="Add one or more dates sperated by comma under quotes, format: YYYY-MM-DD.",
        required=True,
    )
    parser.add_argument("--guild", dest="guild_name", help="The guild name to look for.", required=True)

    args = parser.parse_args()

    input_dates = args.fc_dates.strip().split(",")
    guild_name = args.guild_name

    startup_fc_watcher(fc_dates=input_dates, guild_name=guild_name)


if __name__ == "__main__":
    main()
