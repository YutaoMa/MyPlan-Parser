#coding=utf-8
from selenium import webdriver
import json
import key

# Initialize
option = webdriver.ChromeOptions()
option.set_headless()
option.add_argument("blink-settings=imagesEnabled=false")
browser = webdriver.Chrome(options=option)
browser.implicitly_wait(30)

# Login
browser.get("https://myplan.uw.edu/")
browser.find_element_by_class_name("btn-login-netid").click()
browser.find_element_by_id("weblogin_netid").send_keys(key.NET_ID)
browser.find_element_by_id("weblogin_password").send_keys(key.NET_PASSWORD)
browser.find_element_by_css_selector("input[type='submit']").click()

# Get majors list
browser.find_element_by_link_text("Find Courses").click()
browser.find_element_by_id("seattle-campus-selection").click()
majors_file = open("data/majors.txt", "w")
majors = browser.find_elements_by_css_selector(".split-column a")
for major in majors:
    majors_file.write(major.text + "\n")

# Function to parse one major
def parse_major(major):
    browser.find_element_by_class_name("icon-menu").click()
    browser.find_element_by_link_text("Find Courses").click()
    browser.find_element_by_partial_link_text("(" + major + ")").click()
    major_name = browser.find_element_by_name("searchQuery").get_attribute("value")
    major_name = major_name.replace(" ", "").replace("&", "")
    keep_parsing = True
    courses_list = []
    while(keep_parsing):
        courses = browser.find_elements_by_css_selector(".search-results li")
        for course in courses:
            course_json = {}
            course_json["course-code"] = course.find_element_by_class_name("course-code").text
            course_json["course-title"] = course.find_element_by_class_name("course-title").text
            course_json["course-credit"] = course.find_element_by_css_selector(".course-credit .hidden-xs").text
            course_json["course-term"] = course.find_element_by_class_name("course-term").text
            course_json["course-sections"] = course.find_element_by_class_name("course-sections-mobile").text
            course_json["course-genedureqs"] = course.find_element_by_class_name("course-genedureqs").text
            courses_list.append(course_json)
        try:
            browser.find_element_by_css_selector(".pagination li:nth-child(5):not(.disabled)").click()
        except:
            keep_parsing = False
    with open("data/" + major_name + ".json", "w") as major_file:
        json.dump(courses_list, major_file)
