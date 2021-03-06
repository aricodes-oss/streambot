from . import twitch
from .db import Reservation
from .logging import logger


async def handle(message, game_name, speedrun_only=False):
    await message.channel.send("Sure! One moment while I look up that game.")
    guild_id = message.guild.id
    channel_id = message.channel.id
    available_games = await twitch.get_game(game_name)

    if available_games is None or len(available_games) != 1:
        await message.channel.send(
            f"I couldn't find a match for {game_name} - maybe you spelled it differently from"
            " Twitch's database?",
        )
        return

    game_id = available_games[0]["id"]

    # Check to make sure we're not duplicating it
    try:
        Reservation.get(
            guild_id=guild_id,
            channel_id=channel_id,
            game_id=game_id,
        )

        await message.channel.send(
            f"This channel is already subscribed to {game_name} streams!",
        )

        return
    except Exception:
        pass

    logger.info(
        f"Creating reservation for guild {guild_id}/channel {channel_id}/game"
        f" {game_id} ({game_name}), speedrun_only={speedrun_only}",
    )
    Reservation.create(
        guild_id=guild_id,
        channel_id=channel_id,
        game_id=game_id,
        speedrun_only=speedrun_only,
    )

    await message.channel.send("Subscribed!")
