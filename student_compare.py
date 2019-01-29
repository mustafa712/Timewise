import xml.etree.ElementTree as ET
#import pandas as pd
import numpy as np

tree = ET.parse("Early_datasets/muni-fsps-spr17.xml")

root = tree.getroot()
#print(root)
def common_courses():
    n=0
    for students in root.iter('students'):
        for student in students.iter('student'):
            n=n+1
            
    dictionary = dict() #dictionary to store id of students per course
    for students in root.iter('students'):
        for student in students.iter('student'):
            student_id = student.attrib['id']
            for course in student.iter('course'):
                course_id = course.attrib['id']
                if course_id in dictionary.keys():
                    dictionary[course_id].append(student_id)
                else:
                    dictionary[course_id]=[student_id]

    stu_common_courses = np.zeros((n,n))#matrix storing number of common courses for pairs of students
    for i in dictionary.keys():
        for y in dictionary[i]:
            j=int(y)-1           #index goes for 0 to 1640 for a matrix of size 1641
            for n in dictionary[i]:
                k=int(n)-1
                if(j==k):
                    stu_common_courses[j][k]=0
                else:
                    stu_common_courses[j][k]=stu_common_courses[j][k]+len(dictionary[i])
    return stu_common_courses, dictionary
print(len(common_courses()[1]['67']))

def Student_sectioning():
    edge_weights, course_student_map = common_courses()
    for courses in root.iter('courses'):
        for course in courses.iter('course'):
            course_id = course.attrib['id']
            for config in course.iter('config'):
                configCapDict[config] = 0
                for subpart in config.iter('subpart'):
                    for clas in subpart.iter('class'):
                        configCapDict[config] += clas.attrib['limit']
#            config_count = sum(1 for _ in course.iter('config'))
#            if config_count > 1:
#                configCapDict = {}
#                config_students = solve_IP(course_student_map[course_id])


