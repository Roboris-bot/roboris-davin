import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext

import config


class Noperms(commands.Cog):
    """
    Commands which do ne require any permissions
    """
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(
        name="arche",
        description="Obtenir le lien vers arche",
        guild_ids=config.CONFIG["guilds"])
    async def _arche(self, ctx: SlashContext):
        await ctx.send(content=f"Voici le lien vers Arche : {config.CONFIG['url_arche']}", hidden=True)

    @cog_ext.cog_slash(
        name="ent",
        description="Obtenir le lien vers l'ENT",
        guild_ids=config.CONFIG["guilds"])
    async def _ent(self, ctx: SlashContext):
        await ctx.send(content=f"Voici le lien vers l'ENT : {config.CONFIG['url_ent']}", hidden=True)


def setup(client):
    client.add_cog(Noperms(client))
