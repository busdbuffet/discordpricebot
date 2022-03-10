import discord
from discord.ext import tasks
from web3 import Web3
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import tokenABI
import pricebotConfig

bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))
# STEP 1: address of your token
tokenAddress = "YOUR TOKEN"
# STEP 2: address of your LP pair
lpAddress = "YOUR LP PAIR"
# STEP 3: open pricebotConfig.py

wbnbAddress = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"
tokenContract = web3.eth.contract(address=tokenAddress, abi=tokenABI.tokenABI)
wbnbContract = web3.eth.contract(address=wbnbAddress, abi=tokenABI.tokenABI)

dToken = pricebotConfig.DiscordAPI
client = discord.Client()
@client.event
async def on_ready():
    updAll.start()
    updPrice.start()

@tasks.loop(minutes=10)
async def updAll():
    # get BNB price
    bnbURL = 'https://api.pancakeswap.info/api/v2/tokens/'+wbnbAddress
    bnbSession = Session()
    bnbResponse = bnbSession.get(bnbURL)
    bnbData = json.loads(bnbResponse.text)
    bnbValue = float(bnbData["data"]["price"])

    # get Token price
    tokenURL = 'https://api.pancakeswap.info/api/v2/tokens/'+tokenAddress
    tokenSession = Session()
    tokenResponse = tokenSession.get(tokenURL)
    tokenData = json.loads(tokenResponse.text)
    tokenValue = float(tokenData["data"]["price"])

    cmcURL = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    cmcParameters = { 'id': pricebotConfig.cmcTokenID}
    cmcHeaders = { 'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': pricebotConfig.cmcAPI,}
    cmcSession = Session()
    cmcSession.headers.update(cmcHeaders)
    cmcResponse = cmcSession.get(cmcURL, params=cmcParameters)
    cmcData = json.loads(cmcResponse.text)
    cCap = cmcData["data"][str(pricebotConfig.cmcTokenID)]["self_reported_market_cap"]
    cVolume = cmcData["data"][str(pricebotConfig.cmcTokenID)]["quote"]["USD"]["volume_24h"]
    cVolChange = cmcData["data"][str(pricebotConfig.cmcTokenID)]["quote"]["USD"]["volume_change_24h"]
    cPriceChange = cmcData["data"][str(pricebotConfig.cmcTokenID)]["quote"]["USD"]["percent_change_24h"]

    cSupply = tokenContract.functions.getCirculatingSupply().call() / (10 ** 18)
    lpBNB = wbnbContract.functions.balanceOf(lpAddress).call() / (10 **18)
    lpValue = lpBNB * bnbValue

    priceChannel = client.get_channel(pricebotConfig.DiscordChannelID)
    embedVar = discord.Embed(title="Token Info", color=0xE09900)
    embedVar.add_field(name="Price", value='${:,.12f}'.format(tokenValue), inline=True)
    embedVar.add_field(name="24h Change", value='{:.2f}%'.format(cPriceChange), inline=True)
    embedVar.add_field(name="Market Cap", value='${:,.2f}'.format(cCap), inline=True)
    embedVar.add_field(name="Volume", value='${:,.2f}'.format(cVolume), inline=True)
    embedVar.add_field(name="24h Change", value='{:.2f}%'.format(cVolChange), inline=True)
    embedVar.add_field(name="Liquidity", value='${:,.2f}'.format(lpValue)+' ({:.2f}'.format(lpBNB)+' BNB)', inline=True)
    embedVar.add_field(name="Circ Supply", value='{:,.0f}'.format(cSupply), inline=True)
    await priceChannel.send(embed=embedVar)

@tasks.loop(seconds=90)
async def updPrice():
    # get Token price
    tokenURL = 'https://api.pancakeswap.info/api/v2/tokens/'+tokenAddress
    tokenSession = Session()
    tokenResponse = tokenSession.get(tokenURL)
    tokenData = json.loads(tokenResponse.text)
    tokenValue = float(tokenData["data"]["price"])

    priceChannel = client.get_channel(pricebotConfig.DiscordChannelID)
    embedVar = discord.Embed(color=0x00B7ED)
    embedVar.add_field(name="Price", value='${:,.12f}'.format(tokenValue))
    await priceChannel.send(embed=embedVar)

client.run(dToken) 