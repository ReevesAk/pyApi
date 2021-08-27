import time
import flask
import requests
import sys
import json
import threading
import requests_cache
from nose.tools import assert_true

# Server side cache to API requests.
# This is used to avoid making too many API requests calls.
requests_cache.install_cache("hatchwayCache", backend='SQLite', expire_after=-1)

techTag = {"tag" : "tech"}
historyTag = {"tag" : "history"}
designTag = {"tag" : "design"}
cultureTag = {"tag" : "culture"}
startupsTag = {"tag" : "startups"}
scienceTag = {"tag" : "science"}
politicsTag = {"tag" : "politics"}
healthTag = {"tag" : "health"}

# API url.
api = "https://api.hatchways.io/assessment/blog/posts"

localThread = threading.local()

# Initialize flask for API server.
app = flask.Flask(__name__)
app.config["DEBUG"] = True


def getSession():
    if not hasattr(localThread, "session"):
        localThread.session = requests.Session()
    return localThread.session


def singleFetch(api_url, queryTag):
    session = getSession()
    with session.get(api_url, params=queryTag) as response:
        return response.text


# API ping route. 
@app.route('/api/ping', methods=['GET'])
def pingApi():
    resp = flask.jsonify(success=True)
    return resp
   

# Fetches result for API url with tech tag.
def fetchTechTag():
    try:
        fetchResult = singleFetch(api, techTag)
        techLoad = json.loads(fetchResult)
        return techLoad
        # Check and catch missing tag error.
    except:
        fetchResult = singleFetch(api, "")
        return flask.jsonify(error="Tags parameter is required")


# Fetches result for API url with design tag.
def fetchDesignTag():
    try:
        fetchResult = singleFetch(api, designTag)
        designLoad = json.loads(fetchResult)
        return designLoad
        # Check and catch missing tag error.
    except:
        fetchResult = singleFetch(api, "")    
        return flask.jsonify(error="Tags parameter is required")


# Fetches result for API url with culture tag.
def fetchCultureTag():
    try:
        fetchResult = singleFetch(api, cultureTag)
        cultureLoad = json.loads(fetchResult)
        return cultureLoad
        # Check and catch missing tag error.
    except:
        fetchResult = singleFetch(api, "")    
        return flask.jsonify(error="Tags parameter is required")
    


# Fetches result for API url with science tag.
def fetchScienceTag():
    try:
        fetchResult = singleFetch(api, scienceTag)
        scienceLoad = json.loads(fetchResult)
        return scienceLoad
        # Check and catch missing tag error.
    except:
        fetchResult = singleFetch(api, "")    
        return flask.jsonify(error="Tags parameter is required")



# Fetches result for API url with startups tag.
def fetchStartupsTag():
    try:   
        fetchResult = singleFetch(api, startupsTag)
        startupLoad = json.loads(fetchResult)
        return startupLoad
        # Check and catch missing tag error. 
    except:
        fetchResult = singleFetch(api, "")    
        return flask.jsonify(error="Tags parameter is required")
    

# Fetches result for API url with health tag.
def fetchHealthTag():
    try:
        fetchResult = singleFetch(api, healthTag)
        startupLoad = json.loads(fetchResult)
        return startupLoad
        # Check and catch missing tag error. 
    except:
        fetchResult = singleFetch(api, "")    
        return flask.jsonify(error="Tags parameter is required")
    

# Fetches result for API url with history tag.
def fetchHistoryTag():
    try:
        fetchResult = singleFetch(api, historyTag)
        historyLoad = json.loads(fetchResult)
        return historyLoad
        # Check and catch missing tag error. 
    except:
        fetchResult = singleFetch(api, "")    
        return flask.jsonify(error="Tags parameter is required")
    

# Fetches result for API url with politics tag.
def fetchPoliticsTag():
    try:
        fetchResult = singleFetch(api, politicsTag)
        politicsLoad = json.loads(fetchResult)
        return politicsLoad
        # Check and catch missing tag error. 
    except:
        fetchResult = singleFetch(api, "")    
        return flask.jsonify(error="Tags parameter is required")
    

# Combines all the results from the API requests.
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


# API posts route.
@app.route('/api/posts', methods=['GET'])
def getll():
    collationOfTags = collateAllTagPosts(tech(), culture(), startup(), design(), history(),
                politics(), science(), health())


    # Removes repeated posts from the collated API responses.
    filteredPosts=set()
    result=[element for element in collationOfTags
    if not (tuple(element) in filteredPosts
        or  filteredPosts.add(tuple(element)))]
    value = json.dumps(result, indent=4)
    return str(value)


# Test for each API tag by passing in the API url and it's accompanying tag
def test_request_response():
    # Send a request to the API server and store the response.
    response = requests.get(api, params=techTag)

    # Confirm that the request-response cycle completed successfully.
    assert_true(response.ok)

if __name__ == '__main__':      
    startTime = time.time()
    # Runs the app.
    app.run()