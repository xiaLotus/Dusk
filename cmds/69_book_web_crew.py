from discord.ext import commands
import discord
import aiohttp
from fake_useragent import UserAgent
import os
from bs4 import BeautifulSoup
import asyncio
import io
import sys
from datetime import datetime
import zipfile
import shutil
import time
import json
import random
import aiohttp

class SixNine_bookstore(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def six_nine_zip_directory(self, ctx, title, source_directory, output_zipfile):
        with zipfile.ZipFile(output_zipfile, 'w', zipfile.ZIP_DEFLATED) as zipFile:
            for root, dirs, files in os.walk(source_directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    archive_name = os.path.relpath(file_path, source_directory)
                    zipFile.write(file_path, archive_name)
        return f"{title} 壓縮完畢"
    
    async def six_nine_chapter_name_crew(self, ctx, title, public_headers):
        
        if os.path.exists(title):
            print(f'{title} - 資料夾已經存在。')
        else:
            os.makedirs(f'{title}')

        async with aiohttp.ClientSession() as session:
            try:
                with open(f'{title}.txt', 'r', encoding = 'utf-8') as title_file:
                    chapter_links = title_file.read().split('\n')
                
                for i, chapter_link in enumerate(chapter_links, start = 1):
                    if chapter_link.strip():
                        chapter_title, chapter_url = chapter_link.strip().split(" - ", 1)

                        # print(f'正在抓 - {chapter_title} - {chapter_url}')
                    async with session.get(chapter_url, headers = public_headers, timeout = 10) as res:
                        if res.status == 200:
                            chapter_text = await asyncio.wait_for(res.text(), timeout = 30)
                            soup = BeautifulSoup(chapter_text, 'html.parser')
                            text_element = soup.find('div', class_ = 'txtnav')
                            if text_element:
                                text = text_element.get_text()
                                aligned_left_text = '\n'.join(line.strip() for line in text.strip().split('\n'))

                            chapter_file = f"{title}/{chapter_title}.txt"

                            with open(chapter_file, 'w', encoding = 'utf-8') as chapter_file:
                                chapter_file.write(aligned_left_text)
                        else:
                            print(f"無法下載章節 - {chapter_title}")
            except Exception as e:     
                print(f'不太行，肯定是有毛病: {e}')
        return "我好了"
        
    async def six_nine_get_link(self, ctx, public_headers, url, book_num):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers = public_headers ,timeout = 5) as res:
                    print(res.status)
                    if res.status == 200:
                        page_content = await res.text()
                        soup = BeautifulSoup(page_content, 'html.parser')
                        # 找到title(書名)
                        title = soup.find('title').text.strip().split("最")[0].strip()

                        chapters = soup.select('.catalog li a')

                        with open(f'{title}.txt', 'w', encoding='utf-8') as file:
                            for i, chapter in enumerate(chapters, start=1):
                                chapter_title = chapter.text.strip()
                                if chapter_title != " - #":
                                    chapter_url = chapter['href']
                                    file.write(f"{chapter_title} - {chapter_url}\n")
                        with open(f'{title}.txt', 'r', encoding = 'utf-8') as file:
                            line = file.readlines()
                            try:
                                line = line[1:]
                                f = open(f'{title}.txt', 'w', encoding = 'utf-8')
                                f.writelines(line)
                                f.close()
                            except:
                                pass
                    else:
                        await ctx.send(f'無法下載 - {url}, {res.status}')
                    
            except aiohttp.ClientError as ce:
                print(f'出現異常狀況 - {ce}')

            await session.close()
        return title

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def download(self, ctx, web_name: str, book_num: int):
        # 限制伺服器
        server_id = ctx.guild.id
        if server_id == 1047167757038403655:
            if web_name == "69":
                try:
                    start = time.time()
                    ua = UserAgent()
                    public_headers = {
                        'user-agent': ua.random,
                        "Accept-Encoding": "gzip, deflate, br",
                    }
                    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding = 'utf-8')
                    url = f'https://www.69shuba.com/book/{book_num}/'
                    await ctx.channel.send(f'收到 - {web_name} - {url}')

                    title = await self.six_nine_get_link(ctx, public_headers, url, book_num)
                    await ctx.channel.send(f'爬取完畢! - {title}.txt')

                    end = await self.six_nine_chapter_name_crew(ctx, title, public_headers)
                    # await ctx.channel.send(f'爬取完畢! - folder - {title} - {end}')
                    # await ctx.channel.send(f"開始壓縮 - {title}這個follder")
                    
                    source_directory = f'{title}'
                    output_zipfile = f'{title}.zip'
                    await asyncio.sleep(3)
                    zip_end = await self.six_nine_zip_directory(ctx, title, source_directory, output_zipfile)
                    # await ctx.channel.send(zip_end)

                    my_files = [
                        discord.File(f'{title}.zip'),
                    ]
                    
                    await asyncio.sleep(3)
                    # await ctx.channel.send(f'已上傳{title}.zip檔')
                    await asyncio.sleep(3)
                    # await ctx.channel.send('嘗試另一個下載任務')
                    end = time.time()
                    channel_id = 1168855250959073291
                    f = f"執行時間: %f 秒" %(end - start)

                    send_ctx_to_channel = self.bot.get_channel(channel_id)
                    if send_ctx_to_channel:
                        await send_ctx_to_channel.send(f"{title}耗時 - {f}")
                        await send_ctx_to_channel.send(files = my_files)
                    os.remove(f'{title}.txt')
                    shutil.rmtree(source_directory)
                    os.remove(output_zipfile)

                except asyncio.TimeoutError:
                    await ctx.send('指令超時')

                except EOFError as ce:
                    await ctx.send(f"問題: {ce}")
            else:
                await ctx.send('輸入有問題！請修正！')
        else:
            return



    @download.error
    async def download_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.channel.send(f'請等待 {error.retry_after:.0f} 秒後再試著下載！')


async def setup(bot: commands.Bot):
    await bot.add_cog(SixNine_bookstore(bot))