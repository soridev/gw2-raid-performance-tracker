import os
import pandas
import discord
import argparse
import datetime

from discord.ext import tasks
from typing import List

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
        self.current_df = []
        self.adt = ArcDataTransformator()

        # start the task to run in the background
        self.my_background_task.start()

    async def on_ready(self):
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")

    @tasks.loop(seconds=10)  # task runs every x seconds
    async def my_background_task(self):

        channel = self.get_channel(self.test_channel_token)  # channel ID goes here

        # update statusfile to current status
        data = self.adt.get_fullclear_status(self.fc_dates, self.fc_guild_name)
        wing_and_boss_info = self.adt.get_wing_and_boss_info()

        # check if json changed

        if len(data) != len(self.current_df):

            # create discord embed
            fc_embed = self.create_fc_embed(data, wing_and_boss_info)

            if self.fc_embed:
                await self.fc_embed.edit(embed=fc_embed)
            else:
                self.fc_embed = await channel.send(embed=fc_embed)

            self.current_df = data

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in

    def create_fc_embed(self, data: pandas.DataFrame, boss_info):

        discord_embed = discord.Embed(
            title=f"""{self.fc_guild_name} [{','.join(self.fc_dates)}]""",
            color=0x00FDFD,
        )

        data.sort_values(by=["raid_wing", "boss_position"])
        df_grouped = data.groupby("raid_wing")

        # group df by wings and loop over groups
        for group_name, df_group in df_grouped:
            current_wing_name = f"Wing {group_name}"
            boss_info_lines = []

            # loop over rows in df group
            for row_index, row in df_group.iterrows():
                kill_time_formatted = str(datetime.timedelta(seconds=round(row["kill_duration_seconds"], 0)))
                dr_log = f" - [dps.report]({row['link_to_upload']})" if row["link_to_upload"] else ""
                boss_info_lines.append(
                    f""":white_check_mark: {row["encounter_name"]} [{kill_time_formatted}]{dr_log}"""
                )

            content_string = "\n".join(entry for entry in boss_info_lines)
            discord_embed.add_field(name=current_wing_name, value=content_string, inline=True)

        return discord_embed


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
