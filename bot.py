import discord
from discord import app_commands
from discord.ext import commands
import yt_dlp
import os
import asyncio
import datetime
import aiohttp
import aiofiles
from PIL import Image, ImageDraw, ImageOps, ImageFont
import io
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# =========================================================
# KONFIGURASI ID
# =========================================================
CHANNEL_WELCOME = 1122779577975054356
CHANNEL_RULES = 1519952696919068754
CHANNEL_TAKE_ROLES = 871753041387327608
CHANNEL_VERIFY = 871753087155505104
ROLE_NPC = 1123109693087293516
ROLE_MEMBERS = 871745198441521152
OWNER_ROLE_ID = 871744219298037811
LOG_CHANNEL_ID = 1520228633808081047

def is_owner(interaction: discord.Interaction):
    role = interaction.guild.get_role(OWNER_ROLE_ID)
    return role in interaction.user.roles

# =========================================================
# FITUR WELCOME CARD
# =========================================================
async def create_welcome_image(member: discord.Member):
    img = Image.new('RGB', (600, 300), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    
    avatar_data = await member.display_avatar.replace(size=128).read()
    avatar = Image.open(io.BytesIO(avatar_data)).resize((128, 128))
    
    mask = Image.new('L', (128, 128), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0, 128, 128), fill=255)
    
    border = Image.new('RGBA', (140, 140), (0, 0, 0, 0))
    draw_border = ImageDraw.Draw(border)
    draw_border.ellipse((0, 0, 140, 140), outline="white", width=6)
    
    img.paste(avatar, (236, 40), mask)
    img.paste(border, (230, 34), border)
    
    try:
        font_welcome = ImageFont.truetype("arialbd.ttf", 40)
        font_nick = ImageFont.truetype("arialbd.ttf", 30)
    except:
        font_welcome = ImageFont.load_default()
        font_nick = ImageFont.load_default()
        
    draw.text((300, 200), "WELCOME", anchor="mm", font=font_welcome, fill="white")
    draw.text((300, 240), member.name, anchor="mm", font=font_nick, fill="white")
    
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return discord.File(buffer, filename="welcome.png")

@bot.event
async def on_member_join(member):
    welcome_channel = member.guild.get_channel(CHANNEL_WELCOME)
    await welcome_channel.send(f"Welcome To My Discord Server {member.mention}\nThere Are Now {len(member.guild.members)} Members")
    file = await create_welcome_image(member)
    await welcome_channel.send(file=file)

async def create_goodbye_image(member: discord.Member):
    img = Image.new('RGB', (600, 300), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    
    avatar_data = await member.display_avatar.replace(size=128).read()
    avatar = Image.open(io.BytesIO(avatar_data)).resize((128, 128))
    mask = Image.new('L', (128, 128), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, 128, 128), fill=255)
    
    border = Image.new('RGBA', (140, 140), (0, 0, 0, 0))
    ImageDraw.Draw(border).ellipse((0, 0, 140, 140), outline="red", width=6)
    
    img.paste(avatar, (236, 40), mask)
    img.paste(border, (230, 34), border)
    
    try:
        font = ImageFont.truetype("arialbd.ttf", 40)
    except:
        font = ImageFont.load_default()
        
    draw.text((300, 200), "GOODBYE", anchor="mm", font=font, fill="red")
    draw.text((300, 240), member.name, anchor="mm", font=font, fill="white")
    
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return discord.File(buffer, filename="goodbye.png")

@bot.event
async def on_member_remove(member):
    welcome_channel = member.guild.get_channel(CHANNEL_WELCOME)
    await welcome_channel.send(f"Goodbye {member.mention}, see you again!")
    file = await create_goodbye_image(member)
    await welcome_channel.send(file=file)

@bot.tree.command(name="test-welcome", description="Test welcome message")
@app_commands.check(is_owner)
async def test_welcome(interaction: discord.Interaction):
    file = await create_welcome_image(interaction.user)
    await interaction.response.send_message(file=file, ephemeral=True)

# =========================================================
# VERIFIKASI & AUTO-ROLE
# =========================================================
@bot.tree.command(name="setup-verify", description="Create verification button")
@app_commands.check(is_owner)
async def setup_verify(interaction: discord.Interaction):
    view = discord.ui.View(timeout=None)
    view.add_item(discord.ui.Button(label="Click to Verify", style=discord.ButtonStyle.green, custom_id="verify_button"))
    await interaction.response.send_message("Click the button below to verify!", view=view)

@bot.tree.command(name="setup-roles", description="Create role button")
@app_commands.check(is_owner)
async def setup_roles(interaction: discord.Interaction):
    view = discord.ui.View(timeout=None)
    view.add_item(discord.ui.Button(label="Get Member Role", style=discord.ButtonStyle.blurple, custom_id="member_button"))
    await interaction.response.send_message("Click the button below to become a member!", view=view)

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        if interaction.data["custom_id"] == "verify_button":
            role_npc = interaction.guild.get_role(ROLE_NPC)
            await interaction.user.add_roles(role_npc)
            await interaction.response.send_message("Verification successful! You are now an NPC.", ephemeral=True)
            
        elif interaction.data["custom_id"] == "member_button":
            role_npc = interaction.guild.get_role(ROLE_NPC)
            role_members = interaction.guild.get_role(ROLE_MEMBERS)
            await interaction.user.add_roles(role_members)
            await interaction.user.remove_roles(role_npc)
            await interaction.response.send_message("Congratulations, you are now a Member and the NPC role has been removed!", ephemeral=True)

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message("Only the Owner can use this command!", ephemeral=True)

# =========================================================
# 4. UPDATE STARTUP BOT (WAJIB TAMBAHIN INI)
# =========================================================
@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
        print(f'Bot sudah online: {bot.user}')
        print(f'Jumlah member yang terdeteksi: {len(bot.guilds[0].members)}')
    except Exception as e:
        print(f'Gagal sync command: {e}')
    
    view = discord.ui.View(timeout=None)
    view.add_item(discord.ui.Button(label="Klik untuk Verifikasi", style=discord.ButtonStyle.green, custom_id="verify_button"))
    view.add_item(discord.ui.Button(label="Ambil Role Members", style=discord.ButtonStyle.blurple, custom_id="member_button"))
    bot.add_view(view)

def progress_hook(d):
    if d['status'] == 'downloading':
        print(f"\rDownload: {d.get('_percent_str', 'N/A')}", end='', flush=True)
    elif d['status'] == 'finished':
        print("\nDownload selesai, proses...")

async def upload_file(filename, service):
    # Pindah ke transfer.sh, jauh lebih stabil buat Termux
    url = f"https://transfer.sh/{os.path.basename(filename)}"
    async with aiohttp.ClientSession() as session:
        async with aiofiles.open(filename, 'rb') as f:
            try:
                # Kirim file langsung tanpa ribet FormData
                async with session.put(url, data=f, timeout=120) as resp:
                    if resp.status == 200:
                        return await resp.text()
            except Exception as e:
                print(f"\nUpload Error: {e}")
    return None

@bot.tree.command(name="download", description="Download video")
async def download(interaction: discord.Interaction, url: str):
    await interaction.response.send_message("Diproses...", ephemeral=True)
    
    if os.path.exists('downloaded_video.mp4'):
        os.remove('downloaded_video.mp4')
        
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'downloaded_video.mp4',
        'progress_hooks': [progress_hook],
        'quiet': True,
        'skip_postprocessors': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        filename = 'downloaded_video.mp4'
        size = os.path.getsize(filename) / (1024 * 1024)
        
        if size <= 24:
            await interaction.followup.send("Ini videonya:", file=discord.File(filename), ephemeral=True)
        else:
            await interaction.followup.send("File besar, upload ke Catbox...", ephemeral=True)
            link = await upload_file(filename, "catbox")
            await interaction.followup.send(f"Tautan: {link}" if link else "Upload gagal.", ephemeral=True)
            
        if os.path.exists(filename):
            os.remove(filename)
            
    except Exception as e:
        await interaction.followup.send(f"Error: {e}", ephemeral=True)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Bot aktif: {bot.user}')

# ====================================================
# 2. COMMAND /CLEAR 
# ====================================================
@bot.tree.command(name="clear", description="Menghapus riwayat chat di channel.")
@app_commands.describe(pilihan="Jumlah pesan yang mau dihapus atau ketik 'all'")
@app_commands.checks.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, pilihan: str):
    await interaction.response.send_message("🧹 Sedang membersihkan riwayat obrolan...", ephemeral=True)
    channel = interaction.channel

    try:
        if pilihan.lower() == 'all':
            deleted = await channel.purge(limit=None)
            await interaction.followup.send(f"🗑️ Berhasil menghapus semua pesan ({len(deleted)} pesan telah dibersihkan).", ephemeral=True)
        else:
            jumlah = int(pilihan)
            deleted = await channel.purge(limit=jumlah)
            await interaction.followup.send(f"🗑️ Berhasil menghapus **{len(deleted)}** pesan dari saluran ini.", ephemeral=True)
    except:
        await interaction.followup.send("❌ Gagal menghapus pesan.", ephemeral=True)

@clear.error
async def clear_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("❌ Anda tidak memiliki izin untuk menggunakan perintah ini.", ephemeral=True)

# ====================================================
# 3. COMMAND /INFO
# ====================================================
@bot.tree.command(name="info", description="Menampilkan informasi profil Anda atau pengguna lain.")
@app_commands.describe(member="Pilih pengguna yang ingin dilihat profilnya (opsional)")
async def info(interaction: discord.Interaction, member: discord.Member = None):
    target = member or interaction.user
    
    embed = discord.Embed(title=f"Profil Pengguna: {target.name}", color=discord.Color.blue())
    embed.set_thumbnail(url=target.display_avatar.url)
    embed.add_field(name="Nama Pengguna", value=target.name, inline=True)
    embed.add_field(name="ID Discord", value=target.id, inline=True)
    embed.add_field(name="Nama Panggilan Server", value=target.display_name, inline=True)
    embed.add_field(name="Akun Dibuat", value=target.created_at.strftime("%d-%m-%Y %H:%M:%S"), inline=False)
    embed.add_field(name="Bergabung ke Server", value=target.joined_at.strftime("%d-%m-%Y %H:%M:%S") if target.joined_at else "N/A", inline=False)
    
    await interaction.response.send_message(embed=embed)
    
# ==========================================================
# COMMAND MODERASI & LOG
# ==========================================================

@bot.tree.command(name="warn", description="Memberikan peringatan kepada member")
@app_commands.checks.has_permissions(manage_messages=True)
async def warn(interaction: discord.Interaction, member: discord.Member, reason: str = "Tidak ada alasan"):
    embed = discord.Embed(title="⚠️ Action: Warn", description=f"**Target:** {member.mention}\n**Reason:** {reason}", color=discord.Color.yellow())
    embed.set_thumbnail(url=member.display_avatar.url)
    log_channel = discord.utils.get(interaction.guild.text_channels, name="mod-logs")
    if log_channel: await log_channel.send(embed=embed)
    await interaction.response.send_message(f"✅ {member.mention} telah diperingatkan.", ephemeral=True)
    try: await member.send(f"Anda menerima peringatan di server kami karena: {reason}")
    except: pass

@bot.tree.command(name="kick", description="Mengeluarkan member dari server")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "Tidak ada alasan"):
    embed = discord.Embed(title="⚠️ Action: Kick", description=f"**Target:** {member.mention}\n**Reason:** {reason}", color=discord.Color.orange())
    embed.set_thumbnail(url=member.display_avatar.url)
    log_channel = discord.utils.get(interaction.guild.text_channels, name="mod-logs")
    if log_channel: await log_channel.send(embed=embed)
    try:
        await member.kick(reason=reason)
        await interaction.response.send_message(f"✅ {member.name} telah di-kick.", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Maaf, saya tidak memiliki izin untuk meng-kick member ini.", ephemeral=True)

@bot.tree.command(name="ban", description="Memblokir member dari server")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "Tidak ada alasan"):
    embed = discord.Embed(title="🚫 Action: Ban", description=f"**Target:** {member.mention}\n**Reason:** {reason}", color=discord.Color.red())
    embed.set_thumbnail(url=member.display_avatar.url)
    log_channel = discord.utils.get(interaction.guild.text_channels, name="mod-logs")
    if log_channel: await log_channel.send(embed=embed)
    try:
        await member.ban(reason=reason)
        await interaction.response.send_message(f"✅ {member.name} telah di-ban.", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Maaf, saya tidak memiliki izin untuk mem-ban member ini.", ephemeral=True)

@bot.tree.command(name="timeout", description="Memberikan timeout kepada member")
@app_commands.checks.has_permissions(moderate_members=True)
async def timeout(interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str = "Tidak ada alasan"):
    duration = datetime.timedelta(minutes=minutes)
    embed = discord.Embed(title="⏳ Action: Timeout", description=f"**Target:** {member.mention}\n**Durasi:** {minutes} menit\n**Reason:** {reason}", color=discord.Color.blue())
    embed.set_thumbnail(url=member.display_avatar.url)
    
    log_channel = discord.utils.get(interaction.guild.text_channels, name="mod-logs")
    if log_channel: await log_channel.send(embed=embed)
    
    try:
        await member.timeout(duration, reason=reason)
        await interaction.response.send_message(f"✅ {member.name} telah di-timeout selama {minutes} menit.", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Maaf, saya tidak memiliki izin untuk melakukan timeout kepada member ini.", ephemeral=True)

bot.run(os.getenv('DISCORD_TOKEN'))
