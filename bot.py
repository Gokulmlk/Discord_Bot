import os
from discord.ext import commands
from discord import Intents
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = Intents.default()
intents.messages = True
intents.message_content = True  # Required to read message content

bot = commands.Bot(command_prefix="!", intents=intents)

# Load cogs dynamically
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# Load extensions
bot.load_extension("cogs.ai")
bot.load_extension("cogs.fun")

bot.run(TOKEN)
