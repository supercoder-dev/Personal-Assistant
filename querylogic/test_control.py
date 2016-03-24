# Python 3.4.3 

# 21/Mar/2015
# Drapela Jakub; drapejak@fel.cvut.cz 

# for running this script install wit 
# the website: https://wit.ai/docs/python/1.0.0/quickstart

import festival
from query_control import Query_control


file = open('tests/queries_json.txt', 'r')
resp_array = file.readlines()
file.close()
resp_array = [s.strip('\n') for s in resp_array]


for q in resp_array:
	qc = Query_control()
	answer = qc.query_request(q)
	print(answer)
	festival.sayText(answer)



#def wit_answer(my_query):
#	resp = wit.text_query(my_query, 'CZFOG3SALT7JCMXSFJEI6PC3H4IRZESU')
#	print('Wit response: {}'.format(resp), "\n")
#	return resp


#wit.init()
#query=raw_input('Enter query: ');
#print(query)
#resp = wit_answer(query)
#qc=Query_control();
#answer=qc.query_request(resp);
#print(answer);

#wit.close()



## unused







