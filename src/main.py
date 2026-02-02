import discord
from discord.ext import commands
import asyncio
import fortnite_api
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")
key = os.getenv("FORTNITE_API_KEY")


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='+', intents=intents)

@bot.event
async def on_ready():
    print("Loading FortniteLabs...")
    print("Loaded! - {bot.user.name}")

    await bot.tree.sync()

    await bot.change_presence(
        activity=discord.CustomActivity(
            "🔫FortniteLabs | v1.0"
        )
    )


@bot.tree.command(name="ping", description="Veja se o Fortnite Labs está funcionando!")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"🏓 Pong! \nLatência: `{latency}ms`")

@bot.tree.command(name="player_status", description="Veja as estatísticas de um jogador")
async def player_status(interaction: discord.Interaction, username: str):
    await interaction.response.defer()

    try:
        async with fortnite_api.Client(api_key=os.getenv(key)) as api:
            # Buscando os dados
            status = await api.fetch_br_stats(name=username)
            
            # DEBUG: Isso vai mostrar no  terminal a estrutura que a API enviou
            # print(f"Dados recebidos: {status}") 

            embed = discord.Embed(
                title=f"📊 Estatísticas de {status.user.name}",
                color=discord.Color.blue()
            )
            
            # Tentando acessar os dados globais
            overall = status.stats.all.overall
            
            embed.add_field(name="Nível da Conta", value=str(status.battle_pass.level), inline=True)
            embed.add_field(name="Vitórias", value=str(overall.wins), inline=True)
            embed.add_field(name="K/D", value=str(overall.kd), inline=True)
            embed.add_field(name="Partidas", value=str(overall.matches), inline=True)

            await interaction.followup.send(embed=embed)

    except fortnite_api.NotFound:
        await interaction.followup.send("❌ Usuário não encontrado.")
    except fortnite_api.Forbidden:
        await interaction.followup.send("🔒 Perfil privado.")
    except Exception as e:
        
        print(f"ERRO REAL QUE ESTÁ ACONTECENDO: {e}") 
        await interaction.followup.send(f"⚠️ Erro técnico: {e}")

bot.run(TOKEN)
