import discord
from discord.ext import commands
import secrets, os, requests

BOT_TOKEN    = os.environ["BOT_TOKEN"]       # токен бота
SERVER_URL   = os.environ["SERVER_URL"]      # https://YOUR-APP.onrender.com
ADMIN_SECRET = os.environ["ADMIN_SECRET"]    # твой секрет
ALLOWED_ROLE = "Admin"                       # роль кто может генерить ключи

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

def has_role(ctx):
    return any(r.name == ALLOWED_ROLE for r in ctx.author.roles)

@bot.command()
async def genkey(ctx):
    if not has_role(ctx):
        await ctx.send("❌ No permission.")
        return
    key = secrets.token_hex(16)  # например: a3f1c2d4e5b6...
    r = requests.get(f"{SERVER_URL}/add?secret={ADMIN_SECRET}&key={key}")
    if r.status_code == 200:
        # отправляем ключ в личку чтобы не светить в чате
        await ctx.author.send(f"✅ Your key: `{key}`")
        await ctx.send("✅ Key generated and sent to your DM.")
    else:
        await ctx.send("❌ Server error.")

@bot.command()
async def revoke(ctx, key: str):
    if not has_role(ctx):
        await ctx.send("❌ No permission.")
        return
    r = requests.get(f"{SERVER_URL}/revoke?secret={ADMIN_SECRET}&key={key}")
    if r.status_code == 200:
        await ctx.send(f"✅ Key `{key}` revoked.")
    else:
        await ctx.send("❌ Key not found.")

bot.run(BOT_TOKEN)
