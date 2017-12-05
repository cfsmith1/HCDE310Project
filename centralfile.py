import json, jinja2
import RMP_API
<<<<<<< HEAD
import Flickr_Albums
=======
#COURTNEY READ THIS!!: Please change the name of your "Flickr Album" file to remove the space so that we can import it.
# Then we can do "import Flickr_Album" and then basically copy what Zoe did with hers.
>>>>>>> 42fc7642f64ea118b9bc306f40bc9bde9c8c9057

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
print(professor)
score = RMP_API.sendScore(professor)
print(score)




#Get Classroom Info
building = dict[str(SLN)]["building"]
roomnum = dict[str(SLN)]["room"]
building_and_num = building + " " + roomnum
print(building_and_num)