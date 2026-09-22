import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

farm_ativo = {}

# Lista de categorias válidas da Mudae para o bot conferir
CATEGORIAS_VALIDAS = ["m", "all", "ma", "wa", "ha", "mg", "wg", "hg", "w", "h"]

@bot.event
async def on_ready():
    print(f"✅ Bot de Farm Inteligente ligado: {bot.user.name}")
    print("Pronto para rodar todas as categorias da Mudae!")

@bot.command(name="farm")
async def farm_inteligente(ctx, quantidade: int = 15, categoria: str = "wa"):
    user_id = ctx.author.id
    farm_ativo[user_id] = True
    
    # Limpa o texto da categoria caso o usuário digite com "\$" por engano
    categoria_limpa = categoria.replace("\$", "").lower()
    
    # Se a categoria digitada não for válida, o bot avisa e usa \$wa por padrão
    if categoria_limpa not in CATEGORIAS_VALIDAS:
        await ctx.send(f"⚠️ Categoria `{categoria}` inválida. Usando `$wa` por padrão.")
        categoria_limpa = "wa"
        
    comando_mudae = f"\${categoria_limpa}"
    
    await ctx.send(f"🤖 Iniciando farm automático de {quantidade} rolagens do tipo **{comando_mudae}** para {ctx.author.mention}...")
    
    webhook = await ctx.channel.create_webhook(name=ctx.author.display_name)
    avatar = ctx.author.display_avatar.url
    us_utilizado = False

    try:
        i = 0
        while i < quantity_to_loop(quantidade) and farm_ativo.get(user_id, False):
            # Envia a rolagem escolhida (Ex: \$m, all, wg, etc)
            await webhook.send(content=comando_mudae, username=ctx.author.display_name, avatar_url=avatar)
            i += 1
            await asyncio.sleep(2.0)
            
            # Monitora as últimas mensagens para ver se as rolagens zeraram
            mensagens = [msg async for msg in ctx.channel.history(limit=3)]
            rolagens_esgotadas = False
            
            for msg in mensagens:
                if msg.author.id == 432610292342587392: # ID Oficial da Mudae
                    conteudo = msg.content.lower() or (msg.embeds.description.lower() if msg.embeds else "")
                    if "esgotada" in conteudo or "0 rolls" in conteudo or "limite" in conteudo or "rolls are limited" in conteudo:
                        rolagens_esgotadas = True
                        break
            
            # Se zerou e não usou \$us, ativa o reset automático
            if rolagens_esgotadas and not us_utilizado:
                await ctx.send(f"⚠️ {ctx.author.mention}, suas rolagens acabaram! Usando `$us` automaticamente para resetar...")
                await webhook.send(content="\$us", username=ctx.author.display_name, avatar_url=avatar)
                us_utilizado = True
                await asyncio.sleep(3.0)
                
            elif rolagens_esgotadas and us_utilizado:
                await ctx.send(f"🛑 {ctx.author.mention}, mesmo após o `$us`, as suas rolagens acabaram definitivamente.")
                break
                
        await ctx.send(f"✅ {ctx.author.mention}, sessão de farm de {comando_mudae} finalizada!")
        
    except Exception as e:
        print(f"Erro durante o farm: {e}")
    finally:
        farm_ativo[user_id] = False
        await webhook.delete()

def quantity_to_loop(q):
    return q

@bot.command(name="parar")
async def parar_farm(ctx):
    farm_ativo[ctx.author.id] = False
    await ctx.send(f"🛑 {ctx.author.mention}, seu farm automático foi interrompido.")

# APAGUE O TEXTO ABAIXO E COLE SEU TOKEN ENTRE AS ASPAS
bot.run("MTU1MTc5NDM3MDIxNzM4NjAwNA.GCS1ZU.XdAOw0ZhOOKl71NNn7afhFtIrrORCMrlHJ-nRM")
