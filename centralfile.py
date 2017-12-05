import json, jinja2

#JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
#    extensions=['jinja2.ext.autoescape'],
#    autoescape=True)

SLN = input("What is the SLN of your class? ")
with open('data.txt', 'r') as myfile:
    data = myfile.read()
    dict = json.loads(data)

#print(str(dict))
#Get RateMyProfessor
professor = dict[str(SLN)]["instructor"]



#Get Classroom Info
building = dict[str(SLN)]["building"]
roomnum = dict[str(SLN)]["room"]
building_and_num = building + " " + roomnum