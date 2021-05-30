import os
import discord
import config
from discord.ext import commands
from discord_slash import SlashCommand  # Importing the newly installed library.

client = commands.Bot(intents=discord.Intents.all(), command_prefix="~#>")
slash = SlashCommand(client, sync_commands=True)  # Declares slash commands through the client.


@client.event
async def on_ready():
    print("Roboris est prêt !")


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(config.CONFIG["token"])
