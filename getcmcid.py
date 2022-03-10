from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pricebotConfig

cmcURL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
# STEP 8: enter your Token symbol and run this script to get your token CMC ID
cmcParameters = { 'symbol': 'YOUR TOKEN'}
cmcHeaders = { 'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': pricebotConfig.cmcAPI,}
cmcSession = Session()
cmcSession.headers.update(cmcHeaders)
cmcResponse = cmcSession.get(cmcURL, params=cmcParameters)
cmcData = json.loads(cmcResponse.text)

for curToken in cmcData["data"]:
    print(curToken["id"],' - ',curToken["name"],' - ',curToken["platform"])

# STEP 9: once you have your token id, go back to pricebotConfig.py