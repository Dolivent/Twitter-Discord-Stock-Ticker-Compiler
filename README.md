# Twitter-Discord-Stock-Ticker-Compiler
Fork of (https://github.com/Dolivent/Twitter-Stock-Ticker-Compiler). Added Discord extracting feature

".env" file needs to be updated to include discord token and discord server ID:
``#Twitter Details
\nALPHAVANTAGE_API = 62FVCU5O# go to https://www.alphavantage.co/support/#api-key to apply
\nBEARER_TOKEN = AAAAAAAAANQ2jfXow #go to https://apps.twitter.com/ to apply
\nuser_id = 13695990087 #Twitter ID of user. Use https://tweeterid.com/ to find quickly
\n\n#Discord Details
\nGUILD_ID = 74833378 #https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-
\nTOKEN = "NDcyMTMzNjQz8xqOd-rsCo" #https://discordhelp.net/discord-token https://www.youtube.com/watch?v=tI1lzqzLQCs
\n#the above are dummies. replace with your own keys and target twitter IDs (of feed you would like to extract from)``

Discord extractor forked from @moxniso (https://github.com/moxniso/guildsaver). Main changes are:
1. Currently, the channels that I want to extract from are fixed, so they are hard coded in.
2. Only pulls messages from the last 2 days (and tomorrow to adjust for different timezones)
