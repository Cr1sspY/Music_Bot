import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
import config


intents = discord.Intents.default()     # Подключаем "Разрешения"
intents.message_content = True

YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'False', 'simulate': 'True', 'key': 'FFmpegExtractAudio'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


bot = commands.Bot(command_prefix='-', intents=intents)


@bot.command()  # Вызывается командой -play и коннектит бота в канал
async def play(ctx, url):
    vc = await ctx.message.author.voice.channel.connect()   # Подключаем бота к голосовому каналу

    with YoutubeDL(YDL_OPTIONS) as ydl:
        if 'https://' in url:
            info = ydl.extract_info(url, download=False)    # Если на вход получили ссылку на YouTube
        else:
            info = ydl.extract_info(f"ytsearch:{url}", download=False,)['entries'][0]   # Если на вход получили название
    await ctx.send('>>> Сейчас играет: \n```' + info['title'] + '```')     # Вывод сообщения с названием видео
    link = info['formats'][0]['url']    # Передаём данные из info

    vc.play(discord.FFmpegPCMAudio(executable="ffmpeg\\ffmpeg.exe", source=link, **FFMPEG_OPTIONS))    # Воспроизведение


@bot.command()  # Вызывается командой -exit и отключает бота от канала
async def exit(ctx):
    await ctx.guild.voice_client.disconnect()   # Отключаем бота от голосового канала
    await ctx.send('Я вышел из канала.')


@bot.command()  # Вызывается командой -h и показывает список команд
async def h(ctx):
    await ctx.send('```-play — Включает музыку по ссылке или названию (YouTube only) \n-exit — Выход из голосового канала \n-q — Показывает очередь [in dev]\n-pause — Ставит воспроизведение на паузу [in dev]\n-clear — Очищает очередь [in dev]```')


@bot.command()  # Вызывается командой -q и показывает очередь
async def q(ctx):
    await ctx.send('Показываю очередь. [in dev]')


@bot.command()  # Вызывается командой -pause и ставит трек на паузу
async def pause(ctx):
    await ctx.send('Ставлю музыку на паузу. [in dev]')


@bot.command()  # Вызывается командой -clear и очищает очередь
async def clear(ctx):
    await ctx.send('Очищаю очередь. [in dev]')


bot.run(config.token)
