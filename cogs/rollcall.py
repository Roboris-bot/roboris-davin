from datetime import datetime

import discord
import pytz
from discord.ext import commands
from discord_slash import SlashContext, cog_ext, SlashCommandOptionType
from discord_slash.utils import manage_commands

import config
from permissions import developer, admin

def stringify(role, ctx):
    string_absent = ""
    string_present = ""
    absents = 0
    presents = 0
    channel = ctx.author.voice.channel.members

    for member in role.members:
        if member in channel:
            string_present += f'**{member.display_name}** est présent·e :green_circle: \n'
            presents+=1
        else:
            string_absent += f'**{member.display_name}** est absent·e :red_circle: \n'
            absents+=1

    if len(string_absent+string_present) < 2048:
        return string_absent + string_present, absents
    elif len(string_absent) < 2048:
        return string_absent, absents
    else:
        return f"Il y a trop d'absents dans ce groupe pour que je puisse les afficher" \
               f" ({absents} absents sur {presents+absents} personnes)\n " \
               f"Vérifiez que vous avez séléctioné le bon rôle à appeler!", absents


class Rollcall(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(
        name="appel",
        description="Faire l'appel",
        guild_ids=config.CONFIG["guilds"],
        options=[
            manage_commands.create_option(
                name="role",
                description="rôle pour lequel faire l'appel",
                option_type=SlashCommandOptionType.ROLE,
                required=True
            )
        ]
    )
    async def _appel(self, ctx: SlashContext, role):

        # First, we check if the user has permissions to call this command
        if not await admin(ctx):
            return

        # Next, we check if he is connected to a voice channel
        try:
            channel = ctx.author.voice.channel
        except AttributeError:
            await ctx.send(content="Vous n'êtes connecté à aucun salon vocal !", hidden=True)
            return

        # If the user has got admin permissions and is connected to a voice channel, we defer the request to prevent
        # it from expiring after 3 seconds
        await ctx.defer()

        # Converting the members list for the selected role to a formatted string
        list_string, absents = stringify(role, ctx)

        # Build the embed
        embed = discord.Embed(
            title=f"Appel dans le salon {ctx.author.voice.channel.name} pour le rôle {role.name}",
            description=f"{list_string}",
            color=0xf43f44
        )

        embed.set_footer(text=f"{absents} absent·s "
                              f"\n{datetime.now(pytz.timezone('Europe/Paris')).strftime('%Y-%m-%d %H:%M:%S')} (heure "
                              f"de paris)")

        # Answer with the embed
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Rollcall(client))
