import json, jinja2, RMP_API, flickr_albums, os

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

SLN = input("What is the SLN of your class? ")
with open('data.txt', 'r') as myfile:
    data = myfile.read()
    dict = json.loads(data)

#Get RateMyProfessor
professor = dict[str(SLN)]["instructor"]
print(professor)
score = RMP_API.sendScore(professor)
print(score)

#Get Classroom Info
building = dict[str(SLN)]["building"]
roomnum = dict[str(SLN)]["room"]
building_and_num = building + " " + roomnum
print(building_and_num)
thumbnailsList = flickr_albums.userInputToURLs(building_and_num)
print(thumbnailsList)



htmlInfo = {'score': score, 'thumbnails': thumbnailsList, 'SLN': SLN, 'professor': dict[SLN]["instructor"]}
fname = "your-class.html"
f = open(fname, 'w')

#template_values = {}
#template_values['page_title'] = "Flickr Tag Search"

template = JINJA_ENVIRONMENT.get_template('ClassesTemplate.html')

#response.write(template.render(template_values))

f.write(template.render(htmlInfo))
f.close()
webbrowser.open('ClassesTemplate.html')
