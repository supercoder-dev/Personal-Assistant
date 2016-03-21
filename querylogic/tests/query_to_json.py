# Python 2.7.11 

# 21/Mar/2015
# Drapela Jakub; drapejak@fel.cvut.cz 

# script for tranfer qeury to wit.ai response 
# for running this script install wit 
# the website: https://wit.ai/docs/python/1.0.0/quickstart

#its separated because this run in Python 2 and other in Python 3

import wit 

def findResponse(query):
	ACCES_TOKEN = '7BBOPUV5O46MVZC3IUCYMRXOYYTDZJRH' #acces to wit.ai/konrajak/Household database  
	return wit.text_query(query, ACCES_TOKEN)

print 'Test script for query control'
wit.init()

#queries from text file
file = open('queries.txt', 'r')
query_array = file.readlines()
file.close()
querry_array = [s.strip('\n') for s in query_array]


file = open('queries_json.txt', 'w')

for q in querry_array:
	resp = findResponse(q)
	file.write(resp)
	#file.write('\n')

file.close()

wit.close()
