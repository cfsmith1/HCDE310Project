import json, jinja2, RMP_API, flickr_albums, os, webbrowser, urllib2, webapp2, re

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

#def getSLN():
#    SLN = input("What is the SLN of your class? ")

def getDict():
    with open('data.txt', 'r') as myfile:
        data = myfile.read()
        return json.loads(data)

def getProfessor(SLN, dict):
    professor = dict[str(SLN)]["instructor"]
    print professor
    score = RMP_API.sendScore(professor)
    print score
    return score

#Get Classroom Info
def getClassroom(SLN, dict):
    building = dict[str(SLN)]["building"]
    roomnum = dict[str(SLN)]["room"]
    building_and_num = building + " " + roomnum
    thumbnailsList = flickr_albums.userInputToURLs(building_and_num)
    print thumbnailsList
    return thumbnailsList

class MainHandler(webapp2.RequestHandler):
    def get(self):
        #logging.info("In MainHandler")
        template_values = {}
        template_values['page_title'] = "UW Class Search"
        template = JINJA_ENVIRONMENT.get_template('your_class_form.html')
        self.response.write(template.render(template_values))

def checkInput(input):
    SLNSearch = re.match(r'\d{5}', input, re.M | re.I)
    if SLNSearch:
        return SLNSearch.group().strip()
    else:
        return None

def fixProfName(name):
    namelist = name.split(",")
    newname = "%s %s"%(str(namelist[1]), str(namelist[0]))
    return newname

def getMapURL(building):
    baseurl = "https://www.washington.edu/maps/#!/"
    return "" + baseurl + building

class GreetResponseHandlr(webapp2.RequestHandler):
    def post(self):
        SLN = self.request.get('SLN')
        SLN = checkInput(SLN)

        dict = getDict()

        if SLN and SLN in dict:
            #SLN = self.request.get('SLN')
            #vals['SLN'] = SLN
            building = dict[str(SLN)]["building"]
            roomnum = dict[str(SLN)]["room"]
            building_and_num = building + " " + roomnum
            htmlInfo = {'score': getProfessor(SLN, dict), 'SLN': SLN,
                        'professor': fixProfName(dict[SLN]["instructor"]), 'classroom': building_and_num,
                        'maplink': getMapURL(building), 'building': building}
            thumbnails = getClassroom(SLN, dict)
            #htmlInfo['thumbnails-text'] = str(thumbnails)
            if thumbnails:
                htmlInfo['thumbnails'] = thumbnails
            fname = "your_class_response.html"
            template = JINJA_ENVIRONMENT.get_template(fname)
            self.response.write(template.render(htmlInfo))
            webbrowser.open('your_class_response.html')
        else:
            template = JINJA_ENVIRONMENT.get_template('your_class_error.html')
            htmlInfo = {'page_title': 'ERROR'}
            self.response.write(template.render(htmlInfo))

        #template_values = {}
        #template_values['page_title'] = "Flickr Tag Search"

application = webapp2.WSGIApplication([ \
                                      ('/gresponse', GreetResponseHandlr),
                                      ('/.*', MainHandler)
                                      ],
                                      debug=True)