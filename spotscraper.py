#spotscraper.py
#Tyler Wight
#parses a discord text channel for all instances of spotify songs and then adds them to a playlist
import os
import re
import discord
from discord.ext import commands
from dotenv import load_dotenv
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import time
load_dotenv()
#=============
#Functions
#=============
def URIconverter(inp):
    if re.search("/track/", inp):
        processed = inp.split('track/')
        uri = "spotify:track:" + processed[-1][0:22]
        #uri = processed[-1][0:22]
        return uri
    elif re.search("/album/", inp):
        processed = inp.split('album/')
        uri = "spotify:album:"+processed[-1][0:22]
        return uri
    elif re.search(":playlist:", inp):
        #user = re.search(':user:(.*):playlist:', inp).group(1)
        processed = inp.split('playlist:')
        #playlist = inp.split('playlist:')
        url = "https://open.spotify.com/playlist/" + processed[-1][0:22]
        return url

def album_to_tracks(album_ids):
    result1 = []
    final_result = []
    #print(album_ids)
    for ids in album_ids:
        result1.append(spotify.album_tracks(f'{ids}'))
    for item in result1:
        for x in item['items']:
            final_result.append(x['uri'])
    return final_result

def flatten_list(inputlist):
    flat_list = []
    for element in inputlist:
        if type(element) is list:
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list

def GetPlaylistID(username, playname):
    playid = ''
    playlists = spotify.user_playlists(username)
    for playlist in playlists['items']:  # iterate through playlists I follow
        if playlist['name'] == playname:  # filter for newly created playlist
            playid = playlist['id']
    return playid

#=============
#DISCORD auth
#=============
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()
bot = commands.Bot(command_prefix="$")

#=============
#Spotify auth
#=============
cid = os.getenv('SPOTIPY_CLIENT_ID')
secret = os.getenv('SPOTIPY_CLIENT_SECRET')
username = os.getenv('SPOTIPY_USERNAME')
scope = 'playlist-modify-public'
auth_test=SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri="http://localhost:8080", scope=scope, username=username, open_browser=False)
spottoken = util.prompt_for_user_token(username, scope, client_id=cid, client_secret=secret, redirect_uri="http://localhost:8080", oauth_manager=auth_test)
spotify = spotipy.Spotify(auth=spottoken)


bot.playlist_name = "Discord Playlist"
bot.playlist_id = GetPlaylistID(username, bot.playlist_name) 


@bot.command()
async def ping(ctx):
    await ctx.channel.send("pong")

@bot.command()
async def linksearch(ctx):
    #channel = client.get_channel(533036168892383244)
    #channel = ctx.channel
    word = "spotify.com"
    print("entering long search for " + word)
    messages = await ctx.channel.history(limit=20000).flatten()
    print("I made it out")
    howmany=0
    file1 = open("tmpdata.txt","w+")
    for msg in messages:
        if word in msg.content:
            if "$linksearch" in msg.content or "$keyword" in msg.content:
                print ("test")
                continue
            print(msg.content)
            
            if "spotify.com/track" in msg.content or "spotify.com/album" in msg.content:
                file1.write(msg.content + "\n")
                howmany+=1
    await ctx.channel.send("I found " + str(howmany) + " matching links")
    file1.close()
    await ctx.send(file=discord.File(r"./tmpdata.txt"))

@bot.command()
async def addtoplaylist(ctx):
    #exec(open("./../spotify_python/spotify_python.py").read())
    await ctx.channel.send("added contents of most recent file to spotify.")

@bot.command()
async def setplaylist(ctx , *, name):
    duplicate = 0
    playlists = spotify.user_playlists(username)
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            #print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'], playlist['name']))
            if playlist['name'] == name:
                print("playlist name already exists, will add to it")
                duplicate = 1
                bot.playlist_id = playlist['uri']
                bot.playlist_name = name
        if playlists['next']:
            playlists = spotify.next(playlists)
        else:
            playlists = None
    if duplicate == 0:
        bot.playlist_name = name
        spotify.user_playlist_create(username, name=bot.playlist_name)
        bot.playlist_id = GetPlaylistID(username, bot.playlist_name)
    await ctx.channel.send("Found or created a playlist named: " + str(bot.playlist_name) + " with id: " + str(bot.playlist_id))


@bot.command()
async def addtracks(ctx):
    tracks = []
    atracks = []
    file2 = open ("./tmpdata.txt")
    for line in file2:
        print(line)
        if "/album/" in line:
            tmplist =[]
            tmplist.append(URIconverter(line))
            print(tmplist)
            atracks.append(album_to_tracks(tmplist))
            atracks = flatten_list(atracks)
        

        if "/track/" in line:
            tracks.append(URIconverter(line.strip()))
    

    tracks = tracks + atracks
    group = []
    total = 0
    print(tracks)
    for track in tracks:
        if len(group) >= 75 or total >= (len(tracks)-1):
            #print(group)
            print(len(group))
            spotify.user_playlist_add_tracks(username, bot.playlist_id, group )
            group = []
            time.sleep(2.5)
      
        group.append(track)
        total+=1
    
    
    
    convert="spotify:playlist:" + bot.playlist_id
    print(convert)
    print(bot.playlist_id)
    print(bot.playlist_name)
    output_link=URIconverter(convert)
    file2.close()
    await ctx.channel.send("Added all songs in the queue to playlist " + bot.playlist_name + " located here: " + str(output_link))

        


#client.run(TOKEN)
bot.run(TOKEN)

