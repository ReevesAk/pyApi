import time
import flask
import requests
import json
import threading

apiResponseForTech = "https://api.hatchways.io/assessment/blog/posts?tag=tech"
apiResponseForHealth = "https://api.hatchways.io/assessment/blog/posts?tag=health"
apiResponseForStartups = "https://api.hatchways.io/assessment/blog/posts?tag=startups"
apiResponseForHistory = "https://api.hatchways.io/assessment/blog/posts?tag=history"
apiResponseForScience = "https://api.hatchways.io/assessment/blog/posts?tag=science"
apiResponseForCulture = "https://api.hatchways.io/assessment/blog/posts?tag=culture"
apiResponseForPolitics = "https://api.hatchways.io/assessment/blog/posts?tag=politics"
apiResponseForDesign = "https://api.hatchways.io/assessment/blog/posts?tag=design  "    


apiCallList = [apiResponseForCulture, apiResponseForDesign, apiResponseForHealth, apiResponseForHistory, 
    apiResponseForPolitics, apiResponseForStartups, apiResponseForScience, apiResponseForTech
]


localThread = threading.local()


def printJson(obj):
    # Create a formatted string of the Python JSON object.
    text = json.loads(obj, sort_keys=True, indent=4)
    print(text)


app = flask.Flask(__name__)
app.config["DEBUG"] = True


def getSession():
    if not hasattr(localThread, "session"):
        localThread.session = requests.Session()
    return localThread.session


def singleFetch(api_url):
    session = getSession()
    with session.get(api_url) as response:
        return response.text



@app.route('/api/ping', methods=['GET'])
def pingApi():
    resp = flask.jsonify(success=True)
    return resp
   


def fetchTechTag():
    fetchResult = singleFetch(apiResponseForTech)
    techLoad = json.loads(fetchResult)
    return techLoad


def fetchDesignTag():
    fetchResult = singleFetch(apiResponseForDesign)
    designLoad = json.loads(fetchResult)
    return designLoad


def fetchCultureTag():
    fetchResult = singleFetch(apiResponseForCulture)
    cultureLoad = json.loads(fetchResult)
    return cultureLoad



def fetchScienceTag():
    fetchResult = singleFetch(apiResponseForScience)
    scienceLoad = json.loads(fetchResult)
    return scienceLoad



def fetchStartupsTag():
    fetchResult = singleFetch(apiResponseForStartups)
    startupLoad = json.loads(fetchResult)
    return startupLoad


def fetchHealthTag():
    fetchResult = singleFetch(apiResponseForHealth)
    startupLoad = json.loads(fetchResult)
    return startupLoad


def fetchHistoryTag():
    fetchResult = singleFetch(apiResponseForHistory)
    historyLoad = json.loads(fetchResult)
    return historyLoad


def fetchPoliticsTag():
   fetchResult = singleFetch(apiResponseForPolitics)
   politicsLoad = json.loads(fetchResult)
   return politicsLoad


def collateAllTagPosts(*listOfAllPost):
    return listOfAllPost


tech = fetchTechTag
startup = fetchStartupsTag
design = fetchDesignTag
culture = fetchCultureTag
history = fetchHistoryTag
politics = fetchPoliticsTag
science = fetchScienceTag
health = fetchHealthTag

@app.route('/api/posts', methods=['GET'])
def getll():
    collation = collateAllTagPosts(tech(),startup(),design(),culture(), history(), politics(),science(), health())
    values = ','.join([str(i) for i in collation])

    return values


if __name__ == '__main__':   
    startTime = time.time()
    app.run()