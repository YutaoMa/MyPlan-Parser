#coding=utf-8
import requests
import json

# subjects = requests.get("https://myplan.uw.edu/course/api/subjectAreas").json()
# subjects_list = []
# for subject in subjects:
#     if subject['campus'] == 'seattle':
#         subjects_list.append({'code': subject['code']})
# with open("data/course/subjects.json", "w") as file:
#     json.dump(subjects_list, file)

subjects = json.load(open("data/course/subjects.json", "r"))
courses_url = "https://myplan.uw.edu/course/api/courses"

with open('data/course/courses.json', 'w') as courses_file:
    for subject in subjects:
        body = {
            'campus': 'seattle',
            'consumerLevel': 'UNDERGRADUATE',
            'queryString': subject['code'],
            'sectionSearch': 'False'
        }
        r = requests.post(courses_url, json=body)
        courses = r.json()
        for course in courses:
            json.dump({'code': course['code']}, courses_file)
        r.close()

