# Twitter-Discord-Stock-Ticker-Compiler
Fork of previous project. See link for details https://github.com/Dolivent/Twitter-Stock-Ticker-Compiler. This repository added Discord extracting feature.


# Prerequisite
".env" file needs to be updated to include discord token and discord server ID:
```#Twitter Details
ALPHAVANTAGE_API = 62FVCU5O# go to https://www.alphavantage.co/support/#api-key to apply
BEARER_TOKEN = AAAAAAAAANQ2jfXow #go to https://apps.twitter.com/ to apply
user_id = 13695990087 #Twitter ID of user. Use https://tweeterid.com/ to find quickly
#Discord Details
GUILD_ID = 74833378 #https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-
TOKEN = "NDcyMTMzNjQz8xqOd-rsCo" #https://discordhelp.net/discord-token https://www.youtube.com/watch?v=tI1lzqzLQCs
#the above are dummies. replace with your own keys and target twitter IDs (of feed you would like to extract from)```

Discord extractor forked from @moxniso (https://github.com/moxniso/guildsaver). Main changes are:
1. Currently, the channels that I want to extract from are fixed, so they are hard coded in.
2. Only pulls messages from the last 2 days (and tomorrow to adjust for different timezones)
3. File destination directory that the compiled discord text file is moved to is hard coded
