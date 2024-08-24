import asyncio
import os
import random
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
KICK_USERS_INTERVAL = float(os.getenv('KICK_USERS_INTERVAL'))
JOIN_VOICE_PLAY_BRUD_NA_DIEGUSKA_INTERVAL = float(os.getenv('JOIN_VOICE_PLAY_BRUD_NA_DIEGUSKA_INTERVAL'))

# Set up intents
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

users_to_kick = [line.rstrip('\n') for line in open('users_to_kick.txt')]


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    kick_users.start()
    join_voice_play_brud_na_dieguska.start()


@tasks.loop(minutes=KICK_USERS_INTERVAL)
async def kick_users():
    if users_to_kick:
        print(f'Attempting to kick users: {users_to_kick}')
        for guild in bot.guilds:
            for channel in guild.voice_channels:
                print(f'Checking voice channel: {channel.name}')
                for member in channel.members:
                    for user_to_kick in users_to_kick:
                        if member.name == user_to_kick:
                            print(f'Found user to kick: {member.display_name} in channel: {channel.name}')
                            try:
                                await member.move_to(None)
                                print(f'{member.display_name} has been kicked from {channel.name}')
                            except discord.Forbidden:
                                print(f'Permission error: Unable to kick {member.display_name} from {channel.name}')
                            except discord.HTTPException as e:
                                print(f'HTTP error: {e}')
                            except Exception as e:
                                print(f'Unexpected error: {e}')


@kick_users.before_loop
async def before_kick_users():
    await bot.wait_until_ready()


def get_recording(directory):
    file = random.choice(os.listdir(directory))
    return file


@tasks.loop(minutes=JOIN_VOICE_PLAY_BRUD_NA_DIEGUSKA_INTERVAL)
async def join_voice_play_brud_na_dieguska():
    for guild in bot.guilds:
        for channel in guild.voice_channels:
            for member in channel.members:
                if member.name == 'wbatek':
                    file = get_recording('recordings')
                    file = f'recordings/{file}'
                    voice_channel = await channel.connect()

                    def after_playing(error):
                        if voice_channel.is_connected():
                            coro = voice_channel.disconnect()
                            fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
                            fut.result()

                    voice_channel.play(discord.FFmpegPCMAudio(file), after=after_playing)
                    break


bot.run(TOKEN)
