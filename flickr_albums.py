import json #urllib.request, urllib.error, urllib.parse, json
import urllib2
import urllib
from urlparse import urlparse

# safeGet from the lecture code
def safeGet(url):
    try:
        req = urllib2.Request(url)
        return urllib2.urlopen(req)
    except urllib2.URLError as e:
        if hasattr(e, "code"):
            print("The server couldn't fulfill the request.")
            print("Error code: ", e.code)
        elif hasattr(e, 'reason'):
            print("We failed to reach a server")
            print("Reason: ", e.reason)
        return None

# from lecture code
def flickrREST(baseurl='https://api.flickr.com/services/rest/',
               method='flickr.photos.search',
               api_key='c9ec635aa4c47910e4c47a07291cd4db',
               format='json',
               params={},
               ):
    params['method'] = method
    params['api_key'] = api_key
    params['format'] = format
    if format == "json": params["nojsoncallback"] = True
    #url = baseurl + "?" + urllib.parse.urlencode(params)
    data = urllib.urlencode(params)
    url = baseurl + "?" + data
    return safeGet(url)

# requests the information of all the albums of a specific users flickr account
def flickrRESTListOfUserPhotos(baseurl='https://api.flickr.com/services/rest',
                               method='flickr.photosets.getList',
                               api_key='c9ec635aa4c47910e4c47a07291cd4db',
                               format='json',
                               params={},
                               ):
    params['method'] = method
    params['api_key'] = api_key
    params['format'] = format
    if format == "json": params['nojsoncallback'] = True
    #url = baseurl + "?" + urllib.parse.urlencode(params)
    data = urllib.urlencode(params)
    url = baseurl + "?" + data
    return safeGet(url)

# calls above method for the user of intrest
resultUserPhotos = flickrRESTListOfUserPhotos(params={'user_id': "52503205@N07"})
responceUserPhotos = json.loads(resultUserPhotos.read())

# requests the information of all the photos in an album of a specific users flickr account
def flickrRESTListOfPhotosInAlbum(baseurl='https://api.flickr.com/services/rest',
                                  method='flickr.photosets.getPhotos',
                                  api_key='c9ec635aa4c47910e4c47a07291cd4db',
                                  format='json',
                                  params={},
                                  ):
    params['method'] = method
    params['api_key'] = api_key
    params['format'] = format
    if format == "json":
        params['nojsoncallback'] = True
    #url = baseurl + "?" + urllib.parse.urlencode(params)
    data = urllib.urlencode(params)
    url = baseurl + "?" + data
    return safeGet(url)

# creates a dictionary of each album within a spefic users profile and the id code that goes along with that album
def classroomAndItsID():
    photoSetIDDict = {}
    for classroom in responceUserPhotos['photosets']['photoset']:
        photoSetIDDict[classroom['title']['_content']] = classroom['id']
    return photoSetIDDict

# converts an album to a list of each photo
# creates a dictornay with photo album ID as key and list of photo ID's as value
def photoAlbumtoIndividual(photoalbum):
    DictofPhotosIDInClassroomAlbum = {}
    resultPhotosInAlbum = flickrRESTListOfPhotosInAlbum(params={'user_id': "52503205@N07", 'photoset_id': photoalbum})
    responcePhotosInAlbum = json.loads(resultPhotosInAlbum.read())
    listofPhotoIDs = []
    for eachPhoto in responcePhotosInAlbum['photoset']['photo']:
        listofPhotoIDs.append(eachPhoto['id'])
    DictofPhotosIDInClassroomAlbum[photoalbum] = listofPhotoIDs
    return DictofPhotosIDInClassroomAlbum

# creates a list of the thumbnail URLS for each photo within an album
def IDstoURLS(photoalbumID):
    DictofPhotosIDInClassroomAlbum = photoAlbumtoIndividual(photoalbumID)
    listOfThumbnailURLs = []
    for individualID in DictofPhotosIDInClassroomAlbum[photoalbumID]:
        thumbnailInfo = \
        json.loads(flickrREST(method='flickr.photos.getInfo', params={'photo_id': individualID}).read())['photo']
        thumbnailURL = 'https://farm' + str(thumbnailInfo['farm']) + '.staticflickr.com/' + str(thumbnailInfo['server']) + '/' + str(individualID) + '_' + str(thumbnailInfo['secret']) + '_q.jpg'
        listOfThumbnailURLs.append(thumbnailURL)
    return listOfThumbnailURLs

# takes in user input for the classroom they wish to see and calls other methods to create a dictorary where the
# classroom maps to thumbnail URLs for each photo of the classroom interior
def userInputToURLs(inputFromCentral):
    photoSetIDDict = classroomAndItsID()
    if inputFromCentral in photoSetIDDict:
        photoalbumID = photoSetIDDict[inputFromCentral]
        URLS = IDstoURLS(photoalbumID)
        return URLS
    else:
        return []