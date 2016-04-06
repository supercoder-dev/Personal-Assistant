#!/usr/bin/env python




import wit2 as wit
import json


access_token = 'NUFTF6VJH6EC3BN5S2EK2STCPYGKPPNR'
response = wit.message(access_token, 'what is the weather in Prague')
json_response = json.dumps(response)

r = json.loads(json_response)
print(r["_text"])
print(r["outcomes"])



