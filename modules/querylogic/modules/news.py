from urllib.request import Request, urlopen, URLError
import json

def init_hook():
    access=Accessories()
    return access

class Accessories:

    def call_guardianAPI(self,content_type='world'):
        request = 'http://content.guardianapis.com/' + content_type + '?show-editors-picks=true&show-fields=webTitle&api-key=03482a77-14c1-497d-84bd-bb40ee3a5fc2'

        try:
            response = urlopen(request)
            stat = 'ok'
        except:
            request = 'http://content.guardianapis.com/world?show-editors-picks=true&show-fields=webTitle&api-key=03482a77-14c1-497d-84bd-bb40ee3a5fc2'
            response = urlopen(request)
            stat = 'wrongURL'

        data = json.loads(response.readall().decode('utf-8'))
        lengthOfEditPick=len(data['response']['editorsPicks'])

        if lengthOfEditPick>2:
            rangeMax=3
        else:
            rangeMax = lengthOfEditPick

            if lengthOfEditPick==0:
                stat='No news'

        resp={}
        for i in range (0,rangeMax):
            resp[i]=data['response']['editorsPicks'][i]['webTitle']
            print(i)

        resp['stat']=stat
        return resp

    def list_news_results(self,data):
        s=''
        for i in range(0,len(data)-1):
            s=s+data[i]   +', '
        return s + '.'

    def call_switcher(self,query):
        if 'entities' in query and 'content_type' in query['entities']:
            data = self.call_guardianAPI(query['entities']['content_type']);
        else:
            data = self.call_guardianAPI();

        if data['stat']=='ok':
            return 'The top hot news headlines are: ' + self.list_news_results(data)
        else:
            if len(data.keys())>1:
                return 'I was unable to get the information, here are the top general hot news headlines: ' + self.list_news_results(data)
            else:
                return 'I was unable to get the information.'

    def query_resolution(self, intent, query, params):
        if intent == 'news':
            return self.call_switcher(query)
        else:
            return 'query not recognised'

