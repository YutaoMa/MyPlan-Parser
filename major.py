#coding=utf-8
import requests
import json

url = "https://myplan.uw.edu/program/api/campuses/seattle"
r = requests.get(url)
with open("data/major/majors.json", 'w') as file:
    json.dump(r.json(), file)

majors_file = open("data/major/majors.json", 'r')
majors_json = json.load(majors_file)

majors_min_json = []
colleges = majors_json['colleges']
for college in colleges:
    departments = college['departments']
    for department in departments:
        programs = department['programs']
        for program in programs:
            credentials = program['credentials']
            for credential in credentials:
                code = credential['auditCode']
                admission = credential['admissionType']
                name = credential['name'].replace(" with a major ", " ").strip()
                major = credential['credentialCode']['major']
                majors_min_json.append({
                    'name': name,
                    'code': code,
                    'admission': admission,
                    'major': major
                })
with open("data/major/majors_min.json", 'w') as min_file:
    json.dump(majors_min_json, min_file)             
