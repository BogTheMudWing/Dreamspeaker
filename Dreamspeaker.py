from asyncio import sleep
import os
import random
import discord
from discord.ext import commands
from discord.utils import get
import torch
from TTS.api import TTS
from io import BytesIO

# Replace 'YOUR_DISCORD_BOT_TOKEN' with your bot token
TOKEN = 'YOUR_DISCORD_BOT_TOKEN'

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# List available 🐸TTS models
print(TTS().list_models())

# Init TTS
engine = TTS("tts_models/multilingual/multi-dataset/xtts_v1.1").to(device)

# Ensures only one clip plays at a time
SERVING_REQUEST = False

# Ensures clips are played in order of request
queuedClips = list()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}\nUse !tts <message> to use TTS!')

@bot.command(pass_context=True)
async def tts(ctx, *, text):
    
    global SERVING_REQUEST
        
    # Make sure message isn't empty
    if text is None:
        print("Message is empty.")
        await ctx.send("Your message cannot be empty.")
        return
    
    # Replace acronym with word
    fixedtext = " " + str(text) + " "
    fixedtext = fixedtext.replace(" brb ","be right back").replace(" fr ","for real").replace(" imo ","in my opinion").replace(" tbh ","to be honest").replace(" wb ","welcome back").replace(" rn ","right now").replace(" nvm ","never mind").replace(" idk ","I don't know").replace(" ig ","I guess").replace(" dw ","don't worry").strip()
    
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
    
    # Run TTS
    # ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
    # Text to speech to a file
    engine.tts_to_file(text=fixedtext, speaker_wav=file, language="en", file_path=filename)
    print("File written.")

    # Add to list
    queuedClips.append(filename)
    
    # Wait for previous request to complete
    while SERVING_REQUEST:
        await sleep(.1)
    print("Serving file.")
    
    SERVING_REQUEST = True
    
    # Play the message
    try:
        vc = await voice_channel.connect()
    except discord.errors.ClientException:
        vc = get(bot.voice_clients, guild=ctx.guild)
        print("Already connected to VC.")
    vc.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=queuedClips[0]))
    # Sleep while audio is playing.
    while vc.is_playing():
        await sleep(.1)
    # await vc.disconnect()
    
    # Delete file after playing
    os.remove(queuedClips.pop(0))
    
    SERVING_REQUEST = False
    print("Done!")

@bot.command(pass_context=True)
async def voice(ctx, voice, *, text):
            
    # Make sure message isn't empty
    if text is None:
        print("Message is empty.")
        await ctx.send("Your message cannot be empty.")
        return

    # Replace acronym with word
    fixedtext = " " + str(text) + " "
    fixedtext = fixedtext.replace(" brb ","be right back").replace(" fr ","for real").replace(" imo ","in my opinion").replace(" tbh ","to be honest").replace(" wb ","welcome back").replace(" rn ","right now").replace(" nvm ","never mind").replace(" idk ","I don't know").replace(" ig ","I guess").replace(" dw ","don't worry").strip()
    
    # Get reference file from username
    print("Getting reference for " + voice)
    file = "voices/" + voice + ".wav"
    
    # Check if exists
    if not os.path.isfile(file):
        print("Reference file does not exist.")
        await ctx.send("That voice could not be found.")
        return

    # Create random filename (in case of multiple requests)
    filename = "generated/" + str(random.randint(0, 1000)) + ".wav"
    
    # Run TTS
    # ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
    # Text to speech to a file
    engine.tts_to_file(text=fixedtext, speaker_wav=file, language="en", file_path=filename)
    print("File written.")

    # Send the synthesized voice as a Discord voice message
    await ctx.send("File generated.", file=discord.File(filename))
    
    # Delete file
    os.remove(filename)
    
    print("Done!")

@bot.command(pass_context=True)
async def leave(ctx):
    
    if not ctx.voice_client:
        await ctx.send('I am not currently connected to a voice channel.')
        return
    
    if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send('You have to be connected to the same voice channel to disconnect me.')

bot.run(TOKEN)
