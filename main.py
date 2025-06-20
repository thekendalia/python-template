import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv('token')
prefix = '!'
print(f"Loaded token: {token}")


# Define intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

client = commands.Bot(command_prefix=prefix, intents=intents)
client.remove_command("help")


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    activity = discord.Game(name=".help", type=3)
    await client.change_presence(status=discord.Status.online, activity=activity)


# Help commands
@client.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(title="IndianDesiMemer Help Center ✨", color=0xF49726)
    embed.add_field(
        name="Command Categories :",
        value=(
            "🐸 `memes    :` Image generation with a memey twist.\n"
            "🔧 `utility  :` Bot utility zone\n"
            "😏 `nsfw     :` Image generation with a memey twist.\n\n"
            "To view the commands of a category, send `.help <category>`"
        ),
        inline=False,
    )
    embed.set_footer(icon_url=ctx.author.avatar.url, text=f"Help requested by: {ctx.author.display_name}")
    await ctx.send(embed=embed)


@help.command()
async def memes(ctx):
    embed = discord.Embed(title="IndianDesiMemer Help Center ✨", description="Commands of **meme** \n`.meme:`Memes")
    embed.set_footer(icon_url=ctx.author.avatar.url, text=f"Command requested by: {ctx.author.display_name}")
    await ctx.send(embed=embed)


@help.command()
async def nsfw(ctx):
    embed = discord.Embed(title="IndianDesiMemer Help Center ✨", description="Commands of **nsfw** \n`.nsfw:`NSFW", color=0xF49726)
    embed.set_footer(icon_url=ctx.author.avatar.url, text=f"Command requested by: {ctx.author.display_name}")
    await ctx.send(embed=embed)


@help.command()
async def utility(ctx):
    embed = discord.Embed(title="IndianDesiMemer Help Center ✨", description="Commands of **utility** \n`.ping:`Latency", color=0xF49726)
    embed.set_footer(icon_url=ctx.author.avatar.url, text=f"Command requested by: {ctx.author.display_name}")
    await ctx.send(embed=embed)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"**Try after {round(error.retry_after, 2)} seconds.**")


@client.command()
@commands.cooldown(1, 10, commands.BucketType.channel)
async def meme(ctx):
    response = requests.get("https://meme-api.herokuapp.com/gimme/")
    m = response.json()

    embed = discord.Embed(title=m["title"], url=m["postLink"], color=0xF49726)
    embed.set_image(url=m["url"])
    embed.set_footer(text=f"👍 {m['ups']}  By: r/{m['subreddit']}")
    await ctx.send(embed=embed)


@client.command()
@commands.cooldown(1, 10, commands.BucketType.channel)
async def nsfw(ctx):
    if ctx.channel.is_nsfw():
        await ctx.send("NSFW content would go here!")  # Add actual NSFW logic if needed
    else:
        await ctx.send("❌ You can only use this command in an NSFW channel!")


@client.command()
@commands.cooldown(1, 10, commands.BucketType.channel)
async def ping(ctx):
    await ctx.send(f'Ping! **{round(client.latency * 1000, 1)}**ms')


client.run(token)
