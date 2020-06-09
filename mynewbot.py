import discord #Adding in the libary
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
import youtube_dl
import os
import time
filelist = []
counter = 0
#To specfiy how to command is going to be triggered
client = commands.Bot(command_prefix = '?')
songnumber = [0]
def timer(ctx):
    os.remove(filelist[0])
    filelist.pop(0)
    if filelist != []:
        name = filelist[0]
        # await ctx.send(name)
        voice = get(client.voice_clients, guild=ctx.guild)
        voice.play(discord.FFmpegPCMAudio(name), after=lambda e: timer(ctx))
# Async is to make sure that when the bot
# is ready the function will run
@client.event
async def on_ready():
    
    print("Bot is reday.")
 
#Listen to message sent
@client.listen()
async def on_message(message):
    author = message.author
    content = message.content
    print(f'{author}: {content}')
   
 
 
#Listen to message getting deleting
@client.listen()
async def on_message_delete(message):
    author = message.author
    content = message.content
    channel = message.channel
 
    #To send messages
    await channel.send(f'{author}: {content}')
 
 
#Create a command
#ctx is a Context
@client.command()
async def ping(ctx):
    await ctx.send("Pong!")
   
@client.command()
async def echo(ctx, *args):
    output = ''
    for word in args:
        output += word
        output += ' '
 
    await ctx.send(output)
 
 

 
#leave the voice channel
@client.command()
async def leave(ctx):
 
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
 
    if voice and voice.is_connected():
        print(f"The bot has left {channel}")
        await voice.disconnect()
    else:
        print("Bot was told to leave a voice channel, but was not in a voice channel")
 
 
@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
 
    if voice and voice.is_playing():
        print("Music paused")
        voice.pause()
        await ctx.send("Music paused")
    else:
        print("Music not playing failed pause")
        await ctx.send("Music not playing failed pause")
 
 
@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
 
    if voice and voice.is_paused():
        print("Resumed music")
        voice.resume()
        await ctx.send("Resumed music")
    else:
        print("Music is not paused")
        await ctx.send("Music is not paused")
 
 
@client.command()
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
 
    if voice and voice.is_playing():
        songnumber[0] = 0
        filelist.clear()
        print("Music stopped")
        voice.stop()
        # timer(ctx, False)
        await ctx.send("Music stopped")
    else:
        print("No music playing failed to stop")
        await ctx.send("No music playing failed to stop")
 
@client.command()
async def play(ctx, url: str):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    song_there = os.path.isfile("song.mp3")
    if not(voice.is_playing()):
        print('player')
        try:
            if song_there:
                os.remove("song.mp3")
                print("Removed old song file")
        except PermissionError:
            print("Trying to delete song file, but it's being played")
            await ctx.send("ERROR: Music playing")
            return
    
        await ctx.send("Getting everything ready now")
        voice = get(client.voice_clients, guild=ctx.guild)
    
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '1000',
            }],
            'outtmpl': 'song{}.mp3'.format(songnumber)
        }
    
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])
            filelist.append('song{}.mp3'.format(songnumber))
        songnumber[0] += 1
        name = filelist[0]

        #         print(f"Renamed File: {file}\n")
        #         os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio(name), after= lambda x: timer(ctx))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 10
        await ctx.send(f"Playing: {name}")
        print("playing\n")
    else:
        print('notplaying')
    
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '1000',
            }],
            'outtmpl': 'song{}.mp3'.format(songnumber)
        }
    
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])
            filelist.append('song{}.mp3'.format(songnumber))
        songnumber[0] += 1
        
        # for file in os.listdir("./"):
        #     if file.endswith(".mp3"):
        #         name = file
        #         print(f"Renamed File: {file}\n")
        #         os.rename(file, "song.mp3")
@client.command()
async def list(ctx):
    for i in filelist:
        await ctx.send(i)
#TODO: Add the token into the client to run

client.run('') # DO NOT SHARE THIS