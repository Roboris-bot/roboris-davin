import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext, SlashCommandOptionType
from discord_slash.utils import manage_commands

import config
from permissions import developer, admin


class DeveloperCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="setstatus", description="Changer le statut affiché", guild_ids=config.CONFIG["guilds"],
                       options=[
                           manage_commands.create_option("statustype",
                                                         "type d'activité a afficher",
                                                         SlashCommandOptionType.STRING,
                                                         True,
                                                         [
                                                             manage_commands.create_choice("playing", "Joue a..."),
                                                             manage_commands.create_choice("listening", "Écoute..."),
                                                             manage_commands.create_choice("watching", "Regarde...")
                                                         ]
                                                         ),
                           manage_commands.create_option("activite",
                                                         "nom de l'activité",
                                                         SlashCommandOptionType.STRING,
                                                         True)
                       ])
    async def _setstatus(self, ctx: SlashContext, statustype, activite):
        if not await developer(ctx):
            return

        if statustype == "playing":
            await self.client.change_presence(activity=discord.Game(activite))
        elif statustype == "listening":
            await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,
                                                                        name=activite))
        elif statustype == "watching":
            await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                        name=activite))
        await ctx.send(content=f"Activité changée: {statustype} {activite}", hidden=True)


def setup(client):
    client.add_cog(DeveloperCommands(client))
