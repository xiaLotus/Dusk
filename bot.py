from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import discord
import os


intents = discord.Intents.all()
bot = commands.Bot(command_prefix = '!', intents = intents)

load_dotenv(dotenv_path = 'token.env')
token = os.getenv('TOKEN')

@bot.event
async def on_ready():
    slash = await bot.tree.sync()
    print(f"目前登入機器人 --> {bot.user}")
    print(f"載入 {len(slash)} 個斜線指令")

@bot.command()
async def load(ctx: commands.Context, extension):
    await bot.load_extension(f"cmds.{extension}")
    await ctx.send(f"Loaded {extension} done.")


    # 卸載指令檔案
@bot.command()
async def unload(ctx: commands.Context, extension):
    await bot.unload_extension(f"cmds.{extension}")
    await ctx.send(f"UnLoaded {extension} done.")

    # 重新載入程式檔案
@bot.command()
async def reload(ctx: commands.Context, extension):
    await bot.reload_extension(f"cmdss.{extension}")
    await ctx.send(f"ReLoaded {extension} done.")


# bot 開機開啟.py檔案
async def load_extensions():

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

    for filename in os.listdir("./cmds"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cmds.{filename[:-3]}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(token)

# 確定執行此py檔才會執行
if __name__ == "__main__":
    asyncio.run(main())