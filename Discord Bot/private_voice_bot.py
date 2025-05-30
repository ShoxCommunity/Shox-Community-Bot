import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

PRIVATE_CHANNELS = {}

@bot.event
async def on_ready():
    print(f"✅ Bot connesso come {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel and after.channel.name == "➕ Crea stanza":
        guild = member.guild
        category = after.channel.category

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(connect=False),
            member: discord.PermissionOverwrite(connect=True, manage_channels=True),
        }

        new_channel = await guild.create_voice_channel(
            name=f"🎧 {member.display_name}",
            overwrites=overwrites,
            category=category
        )

        await member.move_to(new_channel)
        PRIVATE_CHANNELS[new_channel.id] = member.id

        await wait_for_empty(new_channel)

async def wait_for_empty(channel):
    await asyncio.sleep(5)
    while True:
        await asyncio.sleep(10)
        if len(channel.members) == 0:
            await channel.delete()
            PRIVATE_CHANNELS.pop(channel.id, None)
            break

bot.run("MTM3ODA0MDM2NjI5NjczMTY2OA.G3S8Hw.66tkpU5L1ooXnSGdngO1r8cCTc7lhZerRmmXgE")
