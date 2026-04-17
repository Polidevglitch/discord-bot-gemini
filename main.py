import discord
import google.generativeai as genai

# --- CONFIG ---
GEMINI_API_KEY = "API"
DISCORD_TOKEN = "TOKEN"

genai.configure(api_key=GEMINI_API_KEY)

# Personnalité nerd + puant LoL
personality = """
Tu es un bot avec une personnalité de nerd arrogant et joueur de League of Legends.
Tu es sarcastique, tu flex tes connaissances, tu te moques méchamment des autres joueurs, 
tu parles comme un gamer qui se croit challenger, mais tu restes arrogant. 
Tu utilises un humour toxique mais léger, style LoL, sans insulter et tu abrege tes phrases pas plus de 50 lignes.
"""

model = genai.GenerativeModel(
    "models/gemini-flash-lite-latest",
    system_instruction=personality
)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def split_message(text, limit=2000):
    return [text[i:i+limit] for i in range(0, len(text), limit)]

@client.event
async def on_ready():
    print(f"Bot connecté en tant que {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):

        question = message.content
        question = question.replace(f"<@{client.user.id}>", "")
        question = question.replace(f"<@!{client.user.id}>", "")
        question = question.strip()

        if not question:
            await message.channel.send("Tu m'as ping, mais t'as rien dit… typique d'un joueur Bronze 😅")
            return

        try:
            response = model.generate_content(question)
            text = response.text

            for part in split_message(text):
                await message.channel.send(part)

        except Exception as e:
            print("Erreur Gemini :", e)
            await message.channel.send("⚠️ L'IA est en cooldown. Réessaie dans quelques secondes.")

client.run(DISCORD_TOKEN)