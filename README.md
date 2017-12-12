# HCDE310Project

## CourseHub

### Intro
Allows a user to input a University of Washington - Seattle Campus SLN and will output a webpage with photos of the classroom, link to the classroom on the UW map, and the professor's Rate My Professor Score

Some components of the application include: a program to scrape the UW time schedule, a program that finds the professor's rate my professor score, and a program that finds the corresponding Flickr album. There is also HTML to create a homepage, error page, and response page for UW CourseHub

### Known Bugs
Below are list of known bugs in the application code.

#### get_classes.py
1. Course title and course code are not included in the dictionary
2. Classes that take place in different locations or different times on different days only include the first listed
time or place.

#### flickr_albums.py
1. If there are no photos of the classroom on flickr, the it returns None

#### RMP_API.py
1. Cannot handle searches of both professor name and department
2. Cannot differentiate professors if two professors have the same name and teach at the same school
