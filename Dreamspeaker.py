from asyncio import sleep
import asyncio
import os
import random
import discord
from discord.ext import commands
from discord.utils import get
import torch
import torchaudio
from pydub import AudioSegment, effects
import time
import typing
import functools
import emoji
from collections import deque
from TTS.api import TTS
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Init TTS
engine = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# Ensures only one clip plays at a time
SERVING_REQUEST = False

# Ensures clips are played in order of request
queuedClips: deque = deque()
requests: deque = deque()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}\nUse !tts <message> to use TTS!")


def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)

    return wrapper


@to_thread
def generate(file, fixedtext, filename):
    engine.tts_to_file(text=fixedtext, speaker_wav=file, language="en", file_path=filename)
    return


@bot.command(pass_context=True)
async def tts(ctx, *, text):

    global queuedClips
    global requests

    # Make sure message isn't empty
    if text is None:
        print("Message is empty.")
        await ctx.send("Your message cannot be empty.")
        return

    # Replace acronym with word
    fixedtext = " " + str(text) + " "
    fixedtext = (
        fixedtext.replace(" brb ", " be right back ")
        .replace(" fr ", " for real ")
        .replace(" imo ", " in my opinion ")
        .replace(" tbh ", " to be honest ")
        .replace(" wb ", " welcome back ")
        .replace(" rn ", " right now ")
        .replace(" nvm ", " never mind ")
        .replace(" idk ", " I don't know ")
        .replace(" ig ", " I guess ")
        .replace(" dw ", " don't worry ")
        .replace(" yk ", " you know ")
        .replace(" thx ", " thanks ")
        .replace(" gn ", " good night ")
        .replace(" mb ", " my bad ")
        .replace(" smth ", " something ")
        .replace(" fsr ", " for some reason ")
        .strip()
    )
    # Replace emojis with their names
    fixedtext = emoji.demojize(fixedtext)

    # Gets voice channel of message author
    try:
        voice_channel = ctx.author.voice.channel
    except AttributeError:
        print("Not in a voice channel.")
        await ctx.send("You are not in a voice channel.")
        return

    # Get reference file from username
    username = ctx.message.author.name
    print("Getting reference for " + username)
    file = "reference/" + username + ".wav"

    # Check if exists
    if not os.path.isfile(file):
        print("Reference file does not exist.")
        await ctx.send("You do not have a reference voice clip.")
        return

    # Create random filename (in case of multiple requests)
    filename = "generated/" + str(random.randint(0, 1000)) + ".wav"
    requests.append(filename)
    print("Added to queue")

    # Add to list
    queuedClips.append(filename)

    asyncio.create_task(ctx.message.add_reaction("⏳"))

    # Wait for previous request to complete
    while requests[0] is not filename:
        await sleep(0.1)
    print("Generating file.")

    # Run TTS
    # Text to speech to a file
    asyncio.create_task(ctx.message.clear_reaction("⏳"))
    asyncio.create_task(ctx.message.add_reaction("⚙️"))

    await generate(file, fixedtext, filename)

    requests.popleft()

    # Normalize audio
    rawsound = AudioSegment.from_file(filename, "wav")
    normalizedsound = effects.normalize(rawsound)
    normalizedsound.export(filename, format="wav")

    print("File written.")

    asyncio.create_task(ctx.message.clear_reaction("⚙️"))
    asyncio.create_task(ctx.message.add_reaction("🔈"))

    # Wait for previous request to complete
    while queuedClips[0] is not filename:
        await sleep(0.1)
    print("Serving file.")

    # Play the message
    try:
        print("Attempting to connnect to VC.")
        vc = await voice_channel.connect()
        print("Connected.")
        await sleep(3)
    except discord.errors.ClientException:
        vc = get(bot.voice_clients, guild=ctx.guild)
        print("Already connected to VC.")

    print("Connected to voice. Playing file...")
    try:
        asyncio.create_task(ctx.message.clear_reaction("🔈"))
        asyncio.create_task(ctx.message.add_reaction("🔊"))
        vc.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=queuedClips[0]))
    except discord.ClientException:
        print("Client error. Aborting.")
        return
    print("Playback started")

    # Sleep while audio is playing.
    while vc.is_playing():
        await sleep(0.1)

    print("Playback finished")
    asyncio.create_task(ctx.message.clear_reaction("🔊"))
    asyncio.create_task(ctx.message.add_reaction("✅"))

    # Delete file after playing
    os.remove(queuedClips.popleft())

    print("Done!")


@bot.command(pass_context=True)
async def leave(ctx):

    if not ctx.voice_client:
        await ctx.send("I am not currently connected to a voice channel.")
        return

    if (
        ctx.author.voice.channel
        and ctx.author.voice.channel == ctx.voice_client.channel
    ):
        await ctx.voice_client.disconnect()
        queuedClips.clear()
        requests.clear()
    else:
        await ctx.send(
            "You have to be connected to the same voice channel to disconnect me."
        )

@bot.command(pass_context=True)
async def ref(ctx):
    # Check if there are attachments in the message
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            # Check if the attachment is an audio file
            if attachment.filename.endswith(('.mp3', '.wav', '.ogg', '.flac', '.m4a')):
                # Download the file into memory (no need to save it first)
                audio_data = await attachment.read()
                                
                # Use pydub to process the audio and convert it to WAV format
                try:
                    audio = AudioSegment.from_file(BytesIO(audio_data), format=attachment.filename.split('.')[-1])
                    wav_filename = ctx.message.author.name + ".wav"
                    file_path = os.path.join("./reference", wav_filename)
                    
                    # Export the audio as a WAV file
                    audio.export(file_path, format="wav")
                    await ctx.send(f"Audio saved and converted to WAV as {wav_filename}")
                except Exception as e:
                    await ctx.send(f"Error converting audio: {e}")
            else:
                await ctx.send("The attached file is not an audio file.")
    else:
        await ctx.send("No attachments found in the message.")


bot.run(TOKEN)
