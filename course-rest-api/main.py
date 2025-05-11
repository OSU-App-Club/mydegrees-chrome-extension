import requests
import re
from fastapi import FastAPI
from bs4 import BeautifulSoup

app = FastAPI()

# since most of the colleges use the same type of formatted pages, we can just use the get_course_data
# function on any of the urls in the college_urls list and we should be able to get all the information
# into one big ol json table something like: 'OIT': ['CS 261' : 'CS 271'], see lines 24-27 for explaination 
# on data format

college_urls = ["https://admissions.oregonstate.edu/course-articulations-oregon-inst-technology"]

def get_course_data(url: str) -> dict[str,str]:
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'html.parser')

    # the courses are stored in the HTML pre tag so fetching that here
    txt = soup.pre
   
    # list of some invalid courses that we won't worry about
    invalid_courses = ["LDT", "LDU", "UDT", "UDU"]
    
    # for easy json conversion an example of how this will look is:
    # 'CS 261' : 'CS 271', where the first value is an OSU course
    # and the second value is the equivalent OSU course.
    coursedict: dict[str, str] = {}
   
    # gets executed if the pre tag was parsed correctly
    if txt is not None and txt.string is not None:
        m = txt.string.splitlines(True)
        prevCourse = ""
        for item in m:
            if item.strip() == "":
                continue

            skip = False
            # regex for getting everything into a nice group to extract
            p = r"^(.{0,4})(.{6}).{37}(.{0,4}).{1}(.{0,4})"
            result = re.search(p, item)
            if result is not None:
                equivCourseSubj = result.group(1).strip()
                equivCourseNum = result.group(2).strip()
                osuCourseSubj = result.group(3).strip()
                osuCourseNum = result.group(4).strip()
                for invalid in invalid_courses:
                    if osuCourseNum == invalid:
                        skip = True

                # handling the AND cases
                if not skip and equivCourseSubj == "" and equivCourseNum == "" and osuCourseSubj != "" and osuCourseNum != "" and prevCourse != "":
                    osuCourse = result.group(3).strip() + " " + result.group(4).strip()
                    coursedict[osuCourse] = prevCourse

                if not skip and equivCourseSubj != "" and equivCourseNum != "" and osuCourseSubj != "" and osuCourseNum != "" and len(osuCourseNum) >= 3:
                    equivCourse = result.group(1).strip() + " " + result.group(2).strip()
                    prevCourse = equivCourse
                    osuCourse = result.group(3).strip() + " " + result.group(4).strip()
                    coursedict[osuCourse] = equivCourse
        
    return coursedict

for college in college_urls:
    print(get_course_data(college))
# dummy place holder for now will work on this at some point
@app.get("/")
def read_root():
    return {"Hello": "World"}
