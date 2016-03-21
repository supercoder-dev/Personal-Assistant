# Python 2.7.11 

# 21/Mar/2015
# Drapela Jakub; drapejak@fel.cvut.cz 

# for running this script install wit 
# the website: https://wit.ai/docs/python/1.0.0/quickstart


# doesnt work in Python 3

import wit
wit.init()
ACCES_TOKEN = '7BBOPUV5O46MVZC3IUCYMRXOYYTDZJRH' #acces to wit.ai/konrajak/Household database 

while True:
	query=raw_input('\n Enter query: ');
	resp = wit.text_query(query, ACCES_TOKEN)
	#print('Response: {}'.format(resp))

wit.close()

#my output:

#[wit] initialized sox: 14.4.1
#[wit] init state machine
#[wit] initialized with device: default

# Enter query: [wit] ready. state=idle
#Should i take an umbrella outside 
#[wit] ready. state=idle
#[wit] received response: {"_text":"Should i take an umbrella outside","msg_id":"9b204aab-75b4-4804-97df-0448c3b99b41","outcomes":[{"_text":"Should i take an umbrella outside","confidence":1,"entities":{"location"[{"suggested":true,"type":"value","value":"outside"}],"weather_detail":[{"type":"value","value":"rain"}]},"intent":"weather"}]}

