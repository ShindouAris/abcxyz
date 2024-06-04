import disnake
from disnake.ext import commands

token = ""
print('Hello Python World')
intents = disnake.Intents.default()
intents.message_content = True

bot = commands.Bot("?", intents=intents)
bot.load_extension("xoxo")

bot.run(token)
