import json
#import urllib.request
#import urllib.error
#import urllib.parse
#import ssl
import urllib2
import urllib
from urlparse import urlparse

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

def safe_URL(url):
    try:
        return url
    except urllib2.URLError as e:
        if hasattr(e, 'reason'):
            print("Reason:", e.reason)
        elif hasattr(e, "code"):
            print("Error Code", e.code)

def rmp_REST(baseurl = 'http://www.ratemyprofessors.com/find/professor/',
    department = "",
    instituition = "University of Washington",
    page = "1",
    query = "*:*",
    queryoption = "TEACHER",
    queryBy = "SchoolId",
    sid = "1530",
    sortBy = "teacherlastname_sort_s asc",
    format = "json",
    params={},
    printurl = False
    ):
    params['department'] = department
    params['institution'] = instituition
    params['page'] = page
    params['format'] = format
    params["query"] = query
    params['queryBy'] = queryBy
    params['sid'] = sid
    params['queryoption'] = queryoption
    params['sortBy'] = sortBy
    params["format"] = format
    if format == "json": params["nojsoncallback"]=True
    data = urllib.urlencode(params)
    #data = data.encode('Big5')
    url = baseurl + "?" + data#urllib.parse.urlencode(params)
    if printurl:
        print(url)
    safeURL = safe_URL(url)

    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req).read()

    #opener = AppURLopener()
    #response = opener.open(safeURL).read()
    resultsPage = json.loads(response)
    return resultsPage

#class AppURLopener(urllib.request.FancyURLopener): #Code From: https://stackoverflow.com/questions/16627227/http-error-403-in-python-3-web-scraping
    #version = "Mozilla/5.0"

def getScore(name, department=""):
#How do we deal with edge cases with people with the same name?
#Also getting the a query AND department search is not working????
    dict = rmp_REST(query=name, department=department)
    if dict["searchResultsTotal"] != 0:
        for professor in dict["professors"]:
            #if professor["overall_rating"] == "N/A":
                #print("Not Enough Reviews to Score")
            return professor["overall_rating"]
    else:
        #print("Professor not found")
        return "N/A"

#Working with the rest of the files.
def sendScore(professor):
    if professor == "TBA":
        return "Sorry a professor has not yet been chosen for this course"
    else:
        professorNoComma = professor.replace(",", " ")
        professorSplit = professorNoComma.split()
        professorSearch= professorSplit[0] + " " + professorSplit[1]
        return getScore(professorSearch)