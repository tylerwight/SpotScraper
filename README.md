# SpotScraper


Discord bot that uses both discord and spotify apis to search the entire history of a discord text channel for all spotify links. It will then take all those spotify links and add them to a new or existing playlist

## How to use:

* Find some guides on creating a bot in discord. Create the bot and auth it to your discord server. Be sure to get the bot token
* Create a file in the same directory as the script named exactly ".env" and put your token in so it looks like this but with your token:
* This .env file will house all our secrets for both spotify and discord. Here is how the file should look:

```
# .env
DISCORD_TOKEN=1lkj23ld8lkj3<blahblah>
DISCORD_GUILD=test_server_name
SPOTIPY_CLIENT_ID='alkjsdfoijwe<blahblahblah>'
SPOTIPY_CLIENT_SECRET='lkjasdf<blahblahblah>'
SPOTIPY_USERNAME='my_user_name'
```
* 

```
python3 discord_reply_bot.py
```
