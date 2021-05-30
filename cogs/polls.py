import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext, SlashCommandOptionType
from discord_slash.utils import manage_commands

import config
from permissions import developer, admin


class Polls(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(
        name="sondage",
        description="Créer un sondage",
        guild_ids=config.CONFIG["guilds"],
        options=[
            manage_commands.create_option(name="question",
                                          description="question à poser",
                                          option_type=SlashCommandOptionType.STRING,
                                          required=True
                                          )
        ]
    )
    async def _sondage(self, ctx: SlashContext, question):
        if not await admin(ctx):
            return

        message = await ctx.send(
            content=f'**Sondage:** *{question}*'
        )
        await message.add_reaction("🟥")
        await message.add_reaction("🟩")


def setup(client):
    client.add_cog(Polls(client))
