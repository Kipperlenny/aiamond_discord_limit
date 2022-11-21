from dotenv import load_dotenv
import discord
from discord.ext.commands import Bot
import os

load_dotenv()

lastMessageTime = {};
sec = 180; # Seconds to wait between messages.

class DiscordCommand:
    def __init__(self, name, handler, ctx = False):
      self.name = name
      self.handler = handler
      self.ctx = ctx

    async def execute_command(self, channel, args, ctx):
        await self.handler(channel, args, ctx)

intents = discord.Intents.default()
intents.message_content = True

client = Bot(description="Limit the amount of messages a user can send in time", pm_help = False, intents=intents, command_prefix=False)

@client.event
async def on_ready():
    print("Ready")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.author.bot:
        return

    if message.is_system():
        return

    admin_role = discord.utils.find(lambda r: r.name == 'Admin', message.guild.roles)
    mod_role = discord.utils.find(lambda r: r.name == 'Moderator', message.guild.roles)
      
    if not admin_role and not mod_role:
        if client.user.id in lastMessageTime and message.created_at.timestamp() - (sec * 1000) < lastMessageTime[client.user.id]:
            print("Blocked message")
            return False
        else:
            lastMessageTime[client.user.id] = message.created_at.timestamp();

client.run(os.getenv('DISCORD_TOKEN'))