"""
Date created: 5.3.2016
Author: Jiri Burant

Script testing the weather api and geolocation library
"""

from query_control import Query_control

while True:
    query=input('Enter query: ');

    qc=Query_control()
    answer=qc.query_request(query)
    print(answer)
