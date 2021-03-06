from .logging import logger

from . import env, subscribe, unsubscribe
from .discord import client
from .constants import AUTH_TOKEN


def _t(w):
    return w.replace("!", "!d") if env.bool("DEBUG", default=False) else w


SUBSCRIBE = _t("!subscribe")
UNSUBSCRIBE = _t("!unsubscribe")
SPEEDRUN = _t("!speedrun")

TRIGGERS = [SUBSCRIBE, UNSUBSCRIBE, SPEEDRUN]


@client.event
async def on_ready():
    logger.info(f"Logged in as {client.user}")
    logger.info("Ret-2-Go!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    command = None

    for trigger in TRIGGERS:
        if message.content.lower().startswith(trigger):
            command = trigger
            break

    if command is None:
        return

    # Vet permissions
    if not message.author.guild_permissions.administrator:
        await message.channel.send("You lack the permissions to do this")

    # Get the name of the game they want
    game_name = message.content[len(command) + 1 :]
    if len(game_name) < 1:
        await message.channel.send("Please specify a game name!")
        return

    await {
        SUBSCRIBE: subscribe.handle,
        SPEEDRUN: subscribe.handle,
        UNSUBSCRIBE: unsubscribe.handle,
    }[command](message, game_name, speedrun_only=command == SPEEDRUN)


def main():
    logger.info("Connecting...")
    client.run(AUTH_TOKEN)
