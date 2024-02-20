import os
from os import system
import hikari
import random
import datetime
import requests
import simplejson as json
from keep_alive import keep_alive

keep_alive()
token = os.getenv("TOKEN")
PREFIX = "ne "
bot = hikari.GatewayBot(token=token, intents=hikari.Intents.ALL)
COMMAND_GUILD_ID = hikari.UNDEFINED


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
  commandReaksi = event.content[0:18]
  if commandKerang.lower() == "apakah":
    if (event.content.lower() == "apakah"):
      #ciduk
      await event.message.respond(
        f"Kamu tidak bisa berkomunikasi dengan baik ya {event.author.mention}? Lebih baik kamu diam saja."
      )
    elif "atau" in event.content:
      #apakah ... atau ...
      splittedContent = event.content.split(sep=" ")[1:]
      for index in range(len(splittedContent)):
        if (splittedContent[index] == "atau"):
          pilihan.append(splittedContent[0:index])
          pilihan.append(splittedContent[index + 1:])
          separator = " "
          response = pilihan[0] if random.randint(1, 2) == 1 else pilihan[1]
          await event.message.respond(f"{separator.join(response)}")
    else:
      #apakah ...
      listJawabanApakah = ["Ya"] * 40 + ["Tidak"] * 40 + [
        "Mungkin saja"
      ] * 15 + [
        f"Kamu tidak bisa berhenti untuk bertanya ya {event.author.mention}? Bisakah kali ini kau diam dan enyah dari sini? Menyebalkan sekali"
      ] * 5
      await event.message.respond(random.choice(listJawabanApakah))

  if (commandPersen.lower() == "berapa persen"):
    await event.message.respond(f"Menurutku, {random.randint(1,100)}%")

  if (commandReaksi.lower() == "reaksi nene"):
    listJawabanReaksi = [
      "https://cdn.discordapp.com/attachments/479153760862601217/1051785620445466674/eww.jpeg",
      "https://cdn.discordapp.com/attachments/479153760862601217/1051785620667760660/seriously.jpeg",
      "https://cdn.discordapp.com/attachments/479153760862601217/1051785620898459668/nyanpasu.jpeg",
      "https://media.discordapp.net/attachments/479153760862601217/1051878163266941028/hmpt.png?width=500&height=500",
    ]
    await event.message.respond(random.choice(listJawabanReaksi))

  # Command Framework 101 :D
  if event.content.startswith(PREFIX):
    if is_command("meme", event.content):
      #meme
      await event.message.respond("meme section")
    elif is_command("ciduk", event.content):
      #ciduk
      await event.message.respond("processing...")
      #event.message.user_mentions[0]
      await hikari.Member.edit(
        self=event.member,
        reason="makar",
        communication_disabled_until=datetime.datetime.now(
          datetime.timezone.utc) + datetime.timedelta(seconds=10))
      await event.message.respond(hikari.Embed(title=f"hahaha"))

@bot.listen()
async def register_commands(event: hikari.StartingEvent) -> None:
    """Register ping and info commands."""
    application = await bot.rest.fetch_application()
    subcommands = hikari.CommandOption(
      name="coba", description="coba"
    )

    commands = [
        bot.rest.slash_command_builder("ping", "Get the bot's latency.").add_option(option=subcommands ),
        bot.rest.slash_command_builder("info", "Learn something about the bot."),
        bot.rest.slash_command_builder("ephemeral", "Send a very secret message."),
        bot.rest.slash_command_builder("coba_api", "Send request to translator."),
        bot.rest.slash_command_builder("cuaca", "Send weather of inputed city."),
    ]

    await bot.rest.set_application_commands(
        application=application.id,
        commands=commands,
        guild=COMMAND_GUILD_ID,
    )

@bot.listen()
async def handle_interactions(event: hikari.InteractionCreateEvent) -> None:
    """Listen for slash commands being executed."""
    if not isinstance(event.interaction, hikari.CommandInteraction):
        # only listen to command interactions, no others!
        return

    if event.interaction.command_name == "ping":
        await event.interaction.create_initial_response(
            hikari.ResponseType.MESSAGE_CREATE,
            f"Pong! {bot.heartbeat_latency * 1_000:.0f}ms",
        )

    elif event.interaction.command_name == "info":
        await event.interaction.create_initial_response(
            hikari.ResponseType.MESSAGE_CREATE,
            "Hello, this is an example bot written in hikari!",
        )

    elif event.interaction.command_name == "ephemeral":
        await event.interaction.create_initial_response(
            hikari.ResponseType.MESSAGE_CREATE,
            "Only you can see this, keep it a secret :)",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
    elif event.interaction.command_name == "coba_api":
      url = "https://google-translate1.p.rapidapi.com/language/translate/v2"
      payload = "q=Hello%2C%20world!&target=es&source=en"
      headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": "587f07c084msh0d2dbab8d8a3fa3p13e528jsn95e9062268fd",
        "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
      }
      response = requests.request("POST", url, data=payload, headers=headers)
      await event.interaction.create_initial_response(
        hikari.ResponseType.MESSAGE_CREATE,
        response.text
      )
    elif event.interaction.command_name == "cuaca":
      url = "https://weather-by-api-ninjas.p.rapidapi.com/v1/weather"
      querystring = {"city":"yogyakarta"}
      headers = {
        "X-RapidAPI-Key": "587f07c084msh0d2dbab8d8a3fa3p13e528jsn95e9062268fd",
        "X-RapidAPI-Host": "weather-by-api-ninjas.p.rapidapi.com"
      }
      response = requests.request("GET", url, headers=headers, params=querystring)
      await event.interaction.create_initial_response(
        hikari.ResponseType.MESSAGE_CREATE,
        response.text
      )

try:
  bot.run()
except hikari.errors.HTTPResponseError:
  print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
  system("python restarter.py")
  system('kill 1')