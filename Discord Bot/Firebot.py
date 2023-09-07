import discord
from discordapi import discord_api
from discord.ext import commands
from weatherapi import weather_api
import requests
from googletrans import Translator

intents = discord.Intents.all()
client = discord.Client(intents=intents)


bot = commands.Bot(command_prefix="!", intents=intents)


#Event Handler
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name="💻Beep Boop💻", url = 'test'))
    print(f'{bot.user.name} is up and ready')

#Welcome Message
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1148492475300859974)
    embed=discord.Embed(title="Welcome!",description=f"{member.mention} has been born")
    await channel.send(embed=embed)

#status command
@bot.command(brief = 'Change bot activity status', help = 'Usage - !status <status>')
async def status(ctx, * , status: str):
    activity = discord.Streaming(name=status.strip('()\''), url = 'test')
    await bot.change_presence(activity=activity)

#Change prefix
@bot.command(brief = 'Change the bot prefix', help = 'Usage - !prefix <new prefix>')
async def prefix(ctx, new_prefix):
    await ctx.message.delete()
    bot.command_prefix = new_prefix
    await ctx.send(f'Prefix has been changed to {new_prefix}')

#Shutdown
@bot.command(brief = 'Shutdown the bot', help = 'Usage - !shutdown (Owner Only)')
@commands.is_owner()
async def shutdown(ctx):
    await ctx.message.delete()
    await ctx.send('Shutting Down...', delete_after = 5.0)
    await exit()

#ban requiring admin perms
@bot.command(brief ='Used to ban users', help = 'Usage - !ban <@user> <reason>')
async def ban(ctx, member : discord.Member, *, reason=None):
    await ctx.message.delete()
    if ctx.author.guild_permissions.administrator:
        if reason == None:
            await ctx.send(f"{ctx.author.mention}, Please provide a reason!")
        else:
            await member.send(f"You have been banned from {ctx.guild.name} for: {reason}")
            await ctx.send(f'{member.mention} has been banned')
            await member.ban(reason=reason)
    else:
        await ctx.send("You do not have the permissions to use this command", delete_after=5.0)

#Unban
@bot.command(brief = 'Used to unban users', help = 'Usage - !unban <userid>')
async def unban(ctx, id: int):
    await ctx.message.delete()
    user = await bot.fetch_user(id)
    try:
        test = await ctx.guild.fetch_ban(user)
    except discord.NotFound:
        await ctx.send('User is not Banned')
        return
    await ctx.guild.unban(user)
    await ctx.send("User Succesfully Unbanned")


@bot.command(brief = 'Used to obtain the Weather of a specific town', help = 'Usage - !weather <town> <state>')
async def weather(ctx,* ,location):
    await ctx.message.delete()
    prlocation = location.strip('()\'')
    try:
        data = weatherdata(location)
        temperature = data['main']['temp']
        newtemp =  "{:.0f}".format(temperature * (1.8) + 32)
        await ctx.send(f'It is {newtemp}°F in {prlocation}')
    except Exception as error:
        await ctx.send(f'Sorry, I couldn\'t fetch the weather for {prlocation}')
        print(error)

def weatherdata(town):
    params =  {'q': town, 'units': 'metric', "appid": weather_api}
    response = requests.get('https://api.openweathermap.org/data/2.5/weather', params = params)
    return response.json()

@bot.command(brief= 'Used to translate text to a different language', help = 'Usage - !translate "<language>" <text>\n (Quotation marks around the desired language are needed for languages that are multi worded such as \'Chinese (simplified)\')')
async def translate(ctx, language , * , text):
    await ctx.message.delete()
    translator = Translator()
    try:
        translated = translator.translate(text, dest=language)
        await ctx.send(f"Original: {text}\n{language} translation: {translated.text}")
    except Exception as error:
        await ctx.send("Something went wrong, Please check the spelling on the language specified")
        print(error)

# Run the bot with your token
bot.run(discord_api)