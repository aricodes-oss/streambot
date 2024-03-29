# streambot

[![Build Status](https://drone.aricodes.net/api/badges/aricodes-oss/streambot-go/status.svg)](https://drone.aricodes.net/aricodes-oss/streambot)

[Invite this bot to your server](https://discord.com/api/oauth2/authorize?client_id=878381224794656778&permissions=0&scope=bot)

## What does this bot do?

StreamBot will maintain a list of currently live Twitch streams in your Discord server, categorized by game. It will automatically delete old messages when the streamer goes offline, making a fully automated solution for your speedrunning community or other game-centric discord.

## How to use

1. Invite the bot to your server
2. Create a channel in your server that you want to act as a stream catalog
3. Give the bot "manage channel" and "manage messages" permissions for that channel
4. In that channel, send a message reading `!subscribe nameofgame` or `!speedrun nameofgame` for every game you want to have catalogued in there

For example, you can send:

```
!subscribe Axiom Verge
!subscribe Axiom Verge 2
```

to keep the channel updated with both games. The `!speedrun` command filters the list to only streams that have the `speedrun` tag enabled:

```
!speedrun Minecraft
!speedrun Super Mario 64
```

You can unsubscribe from these messages at any time in a similar manner:

```
!unsubscribe Axiom Verge
!unsubscribe Axiom Verge 2
```
