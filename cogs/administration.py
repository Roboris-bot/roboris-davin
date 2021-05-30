import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext, SlashCommandOptionType
from discord_slash.utils import manage_commands

import config
from permissions import developer, admin


class Administration(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(
        name="clear",
        description="Effacer des messages dans le canal actuel",
        guild_ids=config.CONFIG["guilds"],
        options=[
            manage_commands.create_option(
                name="nombre",
                description="nombre de messages à effacer",
                option_type=SlashCommandOptionType.INTEGER,
                required=True
            )
        ]
    )
    async def _clear(self, ctx: SlashContext, nombre):
        if not await admin(ctx):
            return

        await ctx.channel.purge(limit=int(nombre))
        await ctx.send(content=f"J'ai bien supprimé {nombre} message·s", hidden=True)


def setup(client):
    client.add_cog(Administration(client))
