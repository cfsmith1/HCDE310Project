import urllib.request, urllib.error, urllib.parse, json, flickr_key, webbrowser

## safeGet from the lecture code ##
def safeGet(url):
     try:
         return urllib.request.urlopen(url)
     except urllib.error.URLError as e:
         if hasattr(e, "code"):
             print("The server couldn't fulfill the request.")
             print("Error code: ", e.code)
         elif hasattr(e, 'reason'):
             print("We failed to reach a server")
             print("Reason: ", e.reason)
         return None

## requests the information of all the albums of a specific users flickr account ##
def flickrRESTListOfUserPhotos(baseurl = 'https://api.flickr.com/services/rest',
                  method = 'flickr.photosets.getList',
                  api_key = flickr_key.flickrKey,
                  format = 'json',
                  params = {},
                  printurl = False
                  ):
       params['method'] = method
       params['api_key'] = api_key
       params['format'] = format
       if format == "json":
           params['nojsoncallback'] = True
       url = baseurl + "?" + urllib.parse.urlencode(params)
       if printurl:
           print(url)
       return safeGet(url)

resultUserPhotos = flickrRESTListOfUserPhotos(params={'user_id': "52503205@N07"}, printurl=True)
responceUserPhotos = json.loads(resultUserPhotos.read())

## Prints out a list of each album within a spefic users profile and the id code that goes along with that album ##
def printListOfAllIDs():
    print("--------List of ID codes for each classroom-----------")
    photoSetIDList = []
    photoSetIDListIndex = 0
    for classroom in responceUserPhotos['photosets']['photoset']:
        photoSetIDList.append(classroom['id'])
        print(str(classroom['title']['_content'])+":"+str(photoSetIDList[photoSetIDListIndex]))
        photoSetIDListIndex += 1

printListOfAllIDs()

## Takes in user input for the ID of the classroom albums they wish to see then opens said albums in a webbrowser ##
listOfClasses = input("Enter a comma seprated list clasrooms ID code as listed above without any spaces: ").split(",")
for photoalbum in listOfClasses:
     webbrowser.open('http:/www.flickr.com/photos/52503205@N07/albums/'+photoalbum)
