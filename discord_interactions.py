import sys
import os
import configparser

import discord
from discord.ext import commands
from discord.ext import tasks
from matplotlib.pyplot import title

from config_helper import ConfigHelper


class RaidHelperClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.test_channel_token = int(
            ConfigHelper().get_config_item("discord-bot", "testing_channel")
        )

        # start the task to run in the background
        self.my_background_task.start()

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")

    @tasks.loop(seconds=60)  # task runs every 60 seconds
    async def my_background_task(self):
        print(self.test_channel_token)
        channel = self.get_channel(self.test_channel_token)  # channel ID goes here

        discord_embed = discord.Embed(
            title="[ZETA] Raid clear - 20/01/2022", color="#00fdfd"
        )

        await channel.send("test message")

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in


def main():
    discord_server_token = ConfigHelper().get_config_item(
        "discord-bot", "discord_token"
    )

    client = RaidHelperClient()
    client.run(discord_server_token)


if __name__ == "__main__":
    main()
