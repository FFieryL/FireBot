import discord
from discordapi import discord_api
from discord.ext import commands


intents = discord.Intents.all()
client = discord.Client(intents=intents)


bot = commands.Bot(command_prefix="!", intents=intents)

#Event Handler
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1148492475300859974)
    embed=discord.Embed(title="Welcome!",description=f"{member.mention} Just Joined")
    await channel.send(embed=embed)
    
@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.message.delete()
    await ctx.send('Shutting Down...', delete_after = 5.0)
    await exit()

@bot.command()
async def ban(ctx, member : discord.Member, reason=None):
    await ctx.message.delete()
    if ctx.author.guild_permissions.administrator:
        if reason == None:
            await ctx.send(f"{ctx.author.mention}, Please provide a reason!")
        else:
            await member.send(f"You have been banned from {ctx.guild.name} for {reason}")
            await member.ban(reason=reason)
    else:
        await ctx.send("You do not have the permissions to use this command", delete_after=5.0)

@bot.command()
async def unban(ctx, id: int):
    await ctx.message.delete()
    user = await bot.fetch_user(id)
    try:
        test = await ctx.guild.fetch_ban(user)
    except discord.NotFound:
        await ctx.send('User is not Banned')
        return
    await ctx.guild.unban(user)
    await ctx.send("User Succesfully unbanned")


# Run the bot with your token
bot.run(discord_api)