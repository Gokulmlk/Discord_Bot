import re
import httpx
import random
from bs4 import BeautifulSoup
from discord.ext import commands, tasks
from discord import Bot, ApplicationContext
import discord


class FunCommandsCog(commands.Cog):
    SEARCH_URL = "https://www.google.com/search?q={}"

    def __init__(self, bot: Bot):
        self.bot = bot
        self.shown_img = []
        self.daily_refresh.start()

    @commands.slash_command(
        name="image",
        description="Get a random quote",
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def image(self, ctx: ApplicationContext, items: str):
        await ctx.defer()

        async with httpx.AsyncClient() as client:
            item = "+".join(items.split())
            url = self.SEARCH_URL.format(item)

            page = await client.get(url)
            page.raise_for_status()

            soup = BeautifulSoup(page.text, "html.parser")

            all_links = map(
                lambda x: f"https://www.google.com{x.get('href')}"
                if "www.google.com" not in x.get("href")
                else x.get("href"),
                soup.find_all("a"),
            )

            images_link = [link for link in all_links if "tbm=isch" in link].pop()
            print(images_link)

            page = await client.get(images_link)
            page.raise_for_status()

            soup = BeautifulSoup(page.text, "html.parser")

            selected_image = random.choice(
                [img.get("src") for img in soup.find_all("img")][1:]
            )

        embed = discord.Embed()
        embed.set_image(url=selected_image)
        embed.set_author(name=f'"{items}"')

        await ctx.respond(embed=embed)

    @tasks.loop(seconds=24, reconnect=True)
    async def daily_refresh(self) -> None:
        self.shown_img.clear()
        # print("refresh")

    @daily_refresh.before_loop
    async def before_refresh(self):
        await self.bot.wait_until_ready()


def setup(bot: Bot):
    bot.add_cog(FunCommandsCog(bot))