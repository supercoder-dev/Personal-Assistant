#!/usr/bin/env python



import wit
#import wit2 as wit

import json
access_token = 'NUFTF6VJH6EC3BN5S2EK2STCPYGKPPNR'
wit.init()
response = wit.voice_query_auto(access_token)

print('Response: {}'.format(response))
print('msg_id')
r = json.loads(response)
print(r["_text"])
wit.close()
