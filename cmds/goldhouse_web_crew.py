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
import re
import aiohttp



# 黃金屋爬蟲
class goldhouse(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def goldhouse_zip_directory(self, ctx, title, source_directory, output_zipfile):
        with zipfile.ZipFile(output_zipfile, 'w', zipfile.ZIP_DEFLATED) as zipFile:
            for root, dirs, files in os.walk(source_directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    archive_name = os.path.relpath(file_path, source_directory)
                    zipFile.write(file_path, archive_name)
        return f"{title} 壓縮完畢"



    async def get_novel_page(self, title, chapter_link, headers):
        if '-' in chapter_link:
            chapter_title, chapter_url = chapter_link.strip().split(" - ", 1)
            chapter_title = chapter_title.strip().split(" ")[0]
            chapter_title = chapter_title.replace('/', '').replace('?', '')
        else:
            print(f"無法解析章節連結：{chapter_link}，重複檢查無效，開始打包")
            # return
        
        # chapter_title, chapter_url = chapter_link.strip().split(" - ", 1)
        # chapter_title = chapter_title.strip().split(" ")[0]

        async with aiohttp.ClientSession() as session:
            try:
                semaphore = asyncio.Semaphore(5) 
                async with semaphore:
                    async with session.get(chapter_url, headers=headers, timeout=20) as response:
                        if response.status == 200:
                            request_text = await response.text()
                        else:
                            print(f"找不到章節: {chapter_url}")
                            # 紀錄在另一個txt內
                            # with open('unprocessed_chapters.txt', 'a', encoding='utf-8') as unprocessed_file:
                            #     unprocessed_file.write(f"{chapter_link}\n")
                            # return
                        
            except asyncio.exceptions.LimitOverrunError as e:
                print(f"Error fetching chapter: {chapter_title}. Error: {str(e)}")
                # 紀錄單張有問題的 chapter_title - chapter_url
                # with open('unprocessed_chapters.txt', 'a', encoding='utf-8') as unprocessed_file:
                #     unprocessed_file.write(f"{chapter_link}\n")
                # return
            

        soup = BeautifulSoup(request_text, 'html.parser')
        path = f"{title}/{chapter_title}.txt"
        content_div = soup.find('div', style='font-size: 20px; line-height: 30px; word-wrap: break-word; table-layout: fixed; word-break: break-all; width: 750px; margin: 0 auto; text-indent: 2em;')

        with open(f'{path}', 'w', encoding='utf-8') as file:
            if content_div:
                for content in content_div:
                    content = content.get_text().strip()
                    if '請記住本站域名:' in content or '黃金屋' in content:
                        content = ''  
                    file.write(content + '\n')
            else:
                file.write('Chapter content not found')
                # with open('unprocessed_chapters.txt', 'a', encoding='utf-8') as unprocessed_file:
                #     unprocessed_file.write(f"{chapter_link}\n")
                # return

        with open(f'{path}', 'r', encoding = 'utf-8') as file:
            original_text = file.read()

        lines = original_text.split('\n')
        for i, line in enumerate(lines):
            if f'{title}' in line:
                lines = lines[i:]
                break

        result_text = '\n'.join(lines)
        with open(f'{path}', 'w', encoding='utf-8') as file:
            file.write(result_text)

        with open(f'{path}', 'r', encoding = 'utf-8') as file:
            original_text = file.read()

        origin_text = re.sub(r'^\s*('+ re.escape(title) + r'[\s\S]*)', r'\1', original_text)
        origin_text = re.sub(r'\n\s*\n', '\n', origin_text)
        lines = original_text.split('\n')
        result_text = '\n'.join(lines)
        with open(f'{path}', 'w', encoding='utf-8') as file:
            file.write(result_text)
        # print(path, ' ok')



    # async def process_unprocessed_chapters(self, title, headers):
    #     # 重新處理導回去
    #     with open('unprocessed_chapters.txt', 'r', encoding='utf-8') as unprocessed_file:
    #         unprocessed_chapter_links = unprocessed_file.readlines()

    #     for chapter_link in unprocessed_chapter_links:
    #         chapter_link = chapter_link.strip()
    #         await self.get_novel_page(title, chapter_link, headers)
        




    # 存好目錄，如
    # 第一章 這人是個傻子 - https://tw.hjwzw.com/Book/Read/44549,20633992
    # 第二章 求賢若渴 - https://tw.hjwzw.com/Book/Read/44549,20633993
    async def get_catalog(self, url, book_nums, headers):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers = headers, timeout = 20) as response:
                html_content = await response.text()

        soup = BeautifulSoup(html_content, 'html.parser')
        title = soup.find('title').text.strip().split('/')[0].strip()

        if not os.path.exists(title):
            os.makedirs(title)

        chapter_elements = soup.find_all('td')
        chapter_links = []
        for chapter_element in chapter_elements:
            link_element = chapter_element.find('a')
            if link_element:
                chapter_url = link_element['href'].strip()
                chapter_url = 'https://tw.hjwzw.com' + chapter_url
                chapter_title = link_element.get_text().strip()
                chapter_url_title = f"{chapter_title} - {chapter_url}\n"
                chapter_links.append(chapter_url_title)

        with open(f'{title}.txt', 'w', encoding='utf-8') as file:
            file.writelines(chapter_links)
        new_lines = []
        with open(f'{title}.txt', 'r', encoding = 'utf-8') as file:
            lines = file.readlines()

        for line in lines:
            if 'https://tw.hjwzw.com/Book/Read/' in line:
                new_lines.append(line)

        with open(f'{title}.txt', 'w', encoding = 'utf-8') as file:
            file.writelines(new_lines)
        return title


    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def goldhouse(self, ctx, book_nums: int):
        server_id = ctx.guild.id
        if server_id == 1047167757038403655:    
            try:
                start = time.time()
                ua = UserAgent()
                headers = {
                    'user-agent': ua.random,
                }
                url = f'https://tw.hjwzw.com/Book/Chapter/{book_nums}'
                title = await self.get_catalog(url, book_nums, headers)
                await ctx.channel.send(f'爬取完畢! - {title}.txt')
                # chapter_links = []
                with open(f'{title}.txt', 'r', encoding = 'utf-8') as file:
                    lines = file.readlines()
                    
                tasks = [self.get_novel_page(title, chapter_link, headers) for chapter_link in lines]
                await asyncio.gather(*tasks)

                # await self.process_unprocessed_chapters(title, headers)

                end = time.time()
                source_directory = f'{title}'
                output_zipfile = f'{title}.zip'
                await asyncio.sleep(3)
                zip_end = await self.goldhouse_zip_directory(ctx, title, source_directory, output_zipfile)
                # 頻道id
                channel_id = 1169913780591927296
                my_files = [
                    discord.File(f'{title}.zip'),
                ]
                await asyncio.sleep(3)
                f = f"執行時間: %f 秒" %(end - start)
                send_ctx_to_channel = self.bot.get_channel(channel_id)
                if send_ctx_to_channel:
                    await send_ctx_to_channel.send(f"{title}耗時 - {f}")
                    await send_ctx_to_channel.send(files = my_files)
                os.remove(f"{title}.txt")
                # os.remove(f"unprocessed_chapters.txt")
                os.remove(output_zipfile)
                shutil.rmtree(source_directory)

            except asyncio.TimeoutError as te:
                print(f"{str(te)}")

            except EOFError as ce:
                await ctx.send(f"問題: {ce}")
            else:
                await ctx.send('輸入有問題！請修正！')
        else:
            return
                                        

async def setup(bot: commands.Bot):
    await bot.add_cog(goldhouse(bot))