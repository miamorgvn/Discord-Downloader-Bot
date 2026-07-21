import discord
from discord import app_commands
from discord.ext import commands
import yt_dlp
import os
import asyncio
import datetime
import aiohttp
import aiofiles
import io
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# =========================================================
# ID CONFIGURATION
# =========================================================
OWNER_ROLE_ID = 871744219298037811

def is_owner(interaction: discord.Interaction):
    role = interaction.guild.get_role(OWNER_ROLE_ID)
    return role in interaction.user.roles

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message("Only the Owner can use this command!", ephemeral=True)

@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
        print(f'Bot is online: {bot.user}')
        print(f'Detected member count: {len(bot.guilds[0].members)}')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

def progress_hook(d):
    if d['status'] == 'downloading':
        print(f"\rDownload: {d.get('_percent_str', 'N/A')}", end='', flush=True)
    elif d['status'] == 'finished':
        print("\nDownload finished, processing...")

async def upload_file(filename, service):
    url = f"https://transfer.sh/{os.path.basename(filename)}"
    async with aiohttp.ClientSession() as session:
        async with aiofiles.open(filename, 'rb') as f:
            try:
                async with session.put(url, data=f, timeout=120) as resp:
                    if resp.status == 200:
                        return await resp.text()
            except Exception as e:
                print(f"\nUpload Error: {e}")
    return None

@bot.tree.command(name="download", description="Download video")
async def download(interaction: discord.Interaction, url: str):
    await interaction.response.send_message("Processing...", ephemeral=True)
    
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
            await interaction.followup.send("Here is your video:", file=discord.File(filename), ephemeral=True)
        else:
            await interaction.followup.send("File is too large, uploading to Catbox...", ephemeral=True)
            link = await upload_file(filename, "catbox")
            await interaction.followup.send(f"Link: {link}" if link else "Upload failed.", ephemeral=True)
            
        if os.path.exists(filename):
            os.remove(filename)
            
    except Exception as e:
        await interaction.followup.send(f"Error: {e}", ephemeral=True)

# ====================================================
# COMMAND /CLEAR 
# ====================================================
@bot.tree.command(name="clear", description="Clear chat history in the channel.")
@app_commands.describe(choice="Number of messages to delete or type 'all'")
@app_commands.checks.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, choice: str):
    await interaction.response.send_message("🧹 Cleaning chat history...", ephemeral=True)
    channel = interaction.channel

    try:
        if choice.lower() == 'all':
            deleted = await channel.purge(limit=None)
            await interaction.followup.send(f"🗑️ Successfully deleted all messages ({len(deleted)} messages cleared).", ephemeral=True)
        else:
            amount = int(choice)
            deleted = await channel.purge(limit=amount)
            await interaction.followup.send(f"🗑️ Successfully deleted **{len(deleted)}** messages from this channel.", ephemeral=True)
    except:
        await interaction.followup.send("❌ Failed to delete messages.", ephemeral=True)

@clear.error
async def clear_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("❌ You do not have permission to use this command.", ephemeral=True)

# ====================================================
# COMMAND /INFO
# ====================================================
@bot.tree.command(name="info", description="Display profile information for yourself or another user.")
@app_commands.describe(member="Select the user to view profile (optional)")
async def info(interaction: discord.Interaction, member: discord.Member = None):
    target = member or interaction.user
    
    embed = discord.Embed(title=f"User Profile: {target.name}", color=discord.Color.blue())
    embed.set_thumbnail(url=target.display_avatar.url)
    embed.add_field(name="Username", value=target.name, inline=True)
    embed.add_field(name="Discord ID", value=target.id, inline=True)
    embed.add_field(name="Server Nickname", value=target.display_name, inline=True)
    embed.add_field(name="Account Created", value=target.created_at.strftime("%d-%m-%Y %H:%M:%S"), inline=False)
    embed.add_field(name="Joined Server", value=target.joined_at.strftime("%d-%m-%Y %H:%M:%S") if target.joined_at else "N/A", inline=False)
    
    await interaction.response.send_message(embed=embed)
    
# ==========================================================
# MODERATION & LOG COMMANDS
# ==========================================================

@bot.tree.command(name="warn", description="Issue a warning to a member")
@app_commands.checks.has_permissions(manage_messages=True)
async def warn(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    embed = discord.Embed(title="⚠️ Action: Warn", description=f"**Target:** {member.mention}\n**Reason:** {reason}", color=discord.Color.yellow())
    embed.set_thumbnail(url=member.display_avatar.url)
    log_channel = discord.utils.get(interaction.guild.text_channels, name="mod-logs")
    if log_channel: await log_channel.send(embed=embed)
    await interaction.response.send_message(f"✅ {member.mention} has been warned.", ephemeral=True)
    try: await member.send(f"You received a warning in our server for: {reason}")
    except: pass

@bot.tree.command(name="kick", description="Kick a member from the server")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    embed = discord.Embed(title="⚠️ Action: Kick", description=f"**Target:** {member.mention}\n**Reason:** {reason}", color=discord.Color.orange())
    embed.set_thumbnail(url=member.display_avatar.url)
    log_channel = discord.utils.get(interaction.guild.text_channels, name="mod-logs")
    if log_channel: await log_channel.send(embed=embed)
    try:
        await member.kick(reason=reason)
        await interaction.response.send_message(f"✅ {member.name} has been kicked.", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Sorry, I do not have permission to kick this member.", ephemeral=True)

@bot.tree.command(name="ban", description="Ban a member from the server")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    embed = discord.Embed(title="🚫 Action: Ban", description=f"**Target:** {member.mention}\n**Reason:** {reason}", color=discord.Color.red())
    embed.set_thumbnail(url=member.display_avatar.url)
    log_channel = discord.utils.get(interaction.guild.text_channels, name="mod-logs")
    if log_channel: await log_channel.send(embed=embed)
    try:
        await member.ban(reason=reason)
        await interaction.response.send_message(f"✅ {member.name} has been banned.", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Sorry, I do not have permission to ban this member.", ephemeral=True)

@bot.tree.command(name="timeout", description="Timeout a member")
@app_commands.checks.has_permissions(moderate_members=True)
async def timeout(interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str = "No reason provided"):
    duration = datetime.timedelta(minutes=minutes)
    embed = discord.Embed(title="⏳ Action: Timeout", description=f"**Target:** {member.mention}\n**Duration:** {minutes} minutes\n**Reason:** {reason}", color=discord.Color.blue())
    embed.set_thumbnail(url=member.display_avatar.url)
    
    log_channel = discord.utils.get(interaction.guild.text_channels, name="mod-logs")
    if log_channel: await log_channel.send(embed=embed)
    
    try:
        await member.timeout(duration, reason=reason)
        await interaction.response.send_message(f"✅ {member.name} has been timed out for {minutes} minutes.", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Sorry, I do not have permission to timeout this member.", ephemeral=True)

bot.run(os.getenv('DISCORD_TOKEN'))
