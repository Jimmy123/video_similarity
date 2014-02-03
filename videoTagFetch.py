import urllib2
import urllib
import json
import urlfetch 
 

def fetchVideo_OMDB(videoName):
    # The OMDB API's constant for searching video titles
    # Fetches a video from OMDB API as a Json object
    # Note: expects a full title name
    try:
        titleUrl = "http://www.omdbapi.com/?i=&"
        pred={}
        pred["t"]=videoName
        pred= urllib.urlencode(pred)
        request = urllib2.Request(titleUrl + pred)
        opener = urllib2.build_opener()
        stream = opener.open(request)
        response=json.load(stream)
        if response["Response"]=="True":
            return response["Title"], response["Genre"], response["Type"]
        else:
            return None, None, None
    except:
        return None, None, None
     
    # get actors, 
    
def fetchVideo_DBpedia(videoName):

    def is_person(url, response):
        try:
            for item in response[url.replace('data', 'resource')[:-5]]['http://www.w3.org/1999/02/22-rdf-syntax-ns#type']:
                if item['value'] == 'http://dbpedia.org/ontology/Person':
                    return True
            return False
        except:
            return False

    def find_disambiguates(url, response):
        ret = []
        try:
            for item in response[url.replace('data', 'resource')[:-5]]['http://dbpedia.org/ontology/wikiPageDisambiguates']:
                ret.append(item['value'])
        except:
            pass
        return ret

    try:
        url="http://dbpedia.org/"
        videoName='_'.join(word[0] + word[1:] for word in videoName.title().split())
        titleUrl = url+"data/"+videoName+".json"
        response = json.loads(urllib2.urlopen(titleUrl).read())
        if is_person(titleUrl, response):
            return True
        ds = find_disambiguates(titleUrl, response)
        for d in ds:
            d = d.replace('resource', 'data') + ".json"
            if is_person(d, json.loads(urllib2.urlopen(d).read())):
                return True
    except:
        return False
    return False
    
    
    
if __name__ == '__main__':
    print fetchVideo_DBpedia("kate walsh")
    print fetchVideo_DBpedia("Jodie Foster")
