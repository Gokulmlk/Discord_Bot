from discord.ext import commands
from discord import Bot, ApplicationContext, Message
from classes.ai import AiClient


class AiCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.active_sessions = []
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.id == self.bot.user.id:  # type: ignore
            return

        if "@here" in message.content or "@everyone" in message.content:
            return

        if self.bot.user not in message.mentions:
            return

        response = await AiClient().respond(
            {"role": "user", "content": message.content}
        )

        await message.reply(response)

    # @commands.slash_command()


def setup(bot: Bot):
    bot.add_cog(AiCog(bot))