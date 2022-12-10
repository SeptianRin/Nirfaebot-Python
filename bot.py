import hikari
import os
from dotenv import load_dotenv
import random
import datetime
load_dotenv()

PREFIX = "ne "
bot = hikari.GatewayBot(token=os.environ["TOKEN"],intents=hikari.Intents.ALL)

def is_command(cmd_name: str, content: str) -> bool:
    """Check if the message sent is a valid command."""
    return content == f"{PREFIX}{cmd_name}"

@bot.listen()
async def message(event: hikari.GuildMessageCreateEvent) -> None:
    """Listen for messages being created."""
    if not event.is_human or not event.content:
        return
    pilihan = []
    commandKerang = event.content[0:6]
    commandPersen = event.content[0:13]
    if commandKerang.lower() == "apakah":
        if(event.content.lower() == "apakah"):
            #ciduk
            await event.message.respond(f"Kamu tidak bisa berkomunikasi dengan baik ya {event.author.mention}? Lebih baik kamu diam saja.")
        elif "atau" in event.content:
            #apakah ... atau ...
            splittedContent = event.content.split(sep= " ")[1:]
            for index in range(len(splittedContent)):
                if(splittedContent[index] == "atau") :
                    print(index)
                    pilihan.append(splittedContent[0:index])
                    pilihan.append(splittedContent[index+1:])
                    separator = " "
                    response = pilihan[0] if random.randint(1,2) == 1 else pilihan[1]
                    await event.message.respond(f"{separator.join(response)}")
        else :
            #apakah ...
            listJawabanApakah = ["Ya"] * 40 + ["Tidak"] * 40 + ["Mungkin saja"] * 15 + [f"Kamu tidak bisa berhenti untuk bertanya ya {event.author.mention}? Bisakah kali ini kau diam dan enyah dari sini? Menyebalkan sekali"] * 5
            await event.message.respond(random.choice(listJawabanApakah))

    if(commandPersen.lower() == "berapa persen"):
         await event.message.respond(f"Menurutku, {random.randint(1,100)}%")

    # Command Framework 101 :D
    if event.content.startswith(PREFIX):
        if is_command("meme", event.content):
            #meme 
            await event.message.respond("meme section")
        elif is_command("ciduk", event.content):
            #ciduk
            await event.message.respond("processing...")
            #event.message.user_mentions[0]
            await hikari.Member.edit(self=event.member,reason="makar",communication_disabled_until=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=10))
            await event.message.respond(hikari.Embed(
                title= f"hahaha"
            ))

bot.run()