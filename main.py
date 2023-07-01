import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
import config


intents = discord.Intents.default()     # Подключаем "Разрешения"
intents.message_content = True

YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'False', 'simulate': 'True', 'key': 'FFmpegExtractAudio'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


bot = commands.Bot(command_prefix='-', intents=intents)


@bot.command()  # Вызывается командой -play
async def play(ctx, url):
    vc = await ctx.message.author.voice.channel.connect()   # Подключаем бота к голосовому каналу

    with YoutubeDL(YDL_OPTIONS) as ydl:
        if 'https://' in url:
            info = ydl.extract_info(url, download=False)    # Если на вход получили ссылку на YouTube
        else:
            info = ydl.extract_info(f"ytsearch:{url}", download=False,)['entries'][0]   # Если на вход получили название
    await ctx.send('>>> Сейчас играет: \n' + info['title'])     # Вывод сообщения с названием видео
    link = info['formats'][0]['url']    # Передаём данные из info

    vc.play(discord.FFmpegPCMAudio(executable="ffmpeg\\ffmpeg.exe", source=link, **FFMPEG_OPTIONS))    # Воспроизведение


@bot.command()  # Вызывается командой -exit
async def exit(ctx):
    await ctx.guild.voice_client.disconnect()   # Отключаем бота от голосового канала
    await ctx.send('Я вышел из канала.')


@bot.command()  # Вызывается командой -h
async def h(ctx):
    await ctx.send('```Здесь \nБудет \nСписок \nКоманд```')


bot.run(config.token)
