
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
load_dotenv()
mongo_client= os.getenv("MONGO_CLIENT")

cluster = MongoClient(mongo_client)
db = cluster["Discord"]
collection = db["Shows"]

@bot.event
async def on_ready():
    print('Logged in')

# Add SHOW/MOVIE to the users list
@bot.command(name='add', help='Adds a show or movie to the users list')
async def addShow(ctx, *, show_name: str):
    userID = ctx.message.author.id
    collection.update_one({"_id": userID}, {"$addToSet":{'shows': show_name}}, upsert=True)
    await ctx.send(f"Added {show_name} to your list")

# Displays all SHOW/MOVIES a user has on their list
@bot.command(name='list', help='Displays all shows or movies currently on a users list')
async def userList(ctx):
    userID = ctx.message.author.id
    result = collection.find_one({"_id": userID})
    embed = discord.Embed(title="To Watch", color= discord.Color.blue())
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    userShows = []
    cnt = 0
    if result == None:
        value = "** **"
    else:
        for show in result["shows"]:
            cnt+=1
            show = f"{cnt}. {show}\t"
            userShows.append(show)

        value = '\n'.join(userShows)

    embed.add_field(name="_Your currently tracked shows or movies:_", value=value, inline=False)
    await ctx.send(embed=embed)

# Mark a SHOW/MOVIE as watched
@bot.command(name='watched', help='Marks a show or movie on a users list as watched')
async def usersWatched(ctx, *, show_name: str):
    userID = ctx.message.author.id
    collection.update_one({"_id":userID, 'shows': show_name}, {"$set":{'shows.$': '~~' + show_name + '~~'}})
    await ctx.send(f"Watched {show_name}")
    
@bot.command(name='delete', help='Deletes a show or movie on a users list')
async def deleteShow(ctx, *, show_name: str):
    userID = ctx.message.author.id
    collection.update_one({"_id": userID}, {"$pull":{'shows': {"$regex": show_name}}})
    await ctx.send(f"Removed {show_name} from your list")
    
load_dotenv()
token = os.getenv("DISCORD_TOKEN")
bot.run(token)