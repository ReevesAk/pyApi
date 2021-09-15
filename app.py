import time
import flask
import json
import os
from zipfile import ZipFile
import requests
from requests import PreparedRequest
import requests_cache
from nose.tools import assert_true

# Server side cache to API requests.
# This is used to avoid making too many API requests calls.
requests_cache.install_cache("hatchwayApiCache", backend='SQLite', expire_after=-1)


# API url.
apiUrl = "https://api.hatchways.io/assessment/blog/posts"

# Query tag parameters for api requests.
paramsTags = {"tags" : [{'tag':'tech'}, {'tag' : 'culture'}, {'tag': 'history'}, {'tag': 'design'}, {'tag': 'custom'}, 
{'tag': 'politics'}, {'tag': 'startup'}, {'tag': 'science'}]}


# Initialize flask for API server.
app = flask.Flask(__name__)
app.config["DEBUG"] = True


# Convert code to zip file.
with ZipFile('api.zip', 'w') as zipf:
    zipf.write(os.path.join('/home/akwa/projects/pyApi','/home/akwa/projects/pyApi/app.py'), arcname='/home/akwa/projects/pyApi/app.py')


# API ping route. 
@app.route('/api/ping', methods=['GET'])
def pingApi():
    resp = flask.jsonify(success=True)
    return resp
   

# API posts route.
@app.route('/api/posts', methods=['GET'])
def getAllPostsFromTags():
    collateAllTags = []
    for tag in paramsTags.values():
        for index in tag:
            try:
                req =PreparedRequest()
                req.prepare_url(apiUrl, index)
            finally:
                filteredPosts=set()
                response = requests.get(req.url)
                jsonData = json.loads(response.text)
                collateAllTags.append(jsonData)

                # Removes repeated posts from the collated API responses.
                result=[element for element in collateAllTags
                if not (tuple(element) in filteredPosts
                or  filteredPosts.add(tuple(element)))]
                value = json.dumps(result)
                return value


# Test for api/posts route.
def test_request_response():
    # Send a request to the API server and store the response.
     for tag in paramsTags.values():
        for index in tag:
                req =PreparedRequest()
                req.prepare_url(apiUrl, index)
                response = requests.get(req.url)

                # Confirm that the request-response cycle completed successfully.
                assert_true(response.ok)


# Test for api ping route.
def test_ping_response():
    try:
        resp = flask.jsonify(success=True)
        return resp
    except Exception as err:
        return err    


if __name__ == '__main__':      
    startTime = time.time()
    # Runs the app.
    app.run()