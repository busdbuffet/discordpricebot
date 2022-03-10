# discordpricebot

This will only work once your token is listed on CMC, and currently only supports a single LP pair
You will need to install web3 and Discord for python if you haven't already

Start by getting a free CMC API key - https://coinmarketcap.com/api/pricing/

Then configure your Discord bot and generate a token for it - https://www.writebots.com/discord-bot-token/
Make sure you give the bot the following permissons
 - Send Messages
 - Embed Links

Make sure your bot has access to the channel you want to display pricing info in

Get the channel ID for the pricebot channel by right clicking on the channel in Discord and hitting Copy ID

Once all that is done, open up pricebot.py and follow the 10 STEPS inside

Once you are all done, you should be good to go.

I run mine from within screen on ubuntu

Just type "screen", run the pricebot with
  python3 pricebot.py
  
You can exit the screen session with CTRL+A and D
