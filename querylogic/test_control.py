# Python 3.4.3 

# 24/Mar/2015
# Drapela Jakub; drapejak@fel.cvut.cz 

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





