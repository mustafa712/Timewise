import xml.etree.ElementTree as ET
import pandas as pd

tree = ET.parse("Early_datasets/agh-fis-spr17.xml")

root = tree.getroot()
print(root)
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
import numpy as np
stu_common_courses = np.zeros((n,n))#matrix storing number of common courses for pairs of students
for i in dictionary.keys():
    for y in dictionary[i]:
        j=int(y)-1           #index goes for 0 to 1640 for a matrix of size 1641
        for n in dictionary[i]:
            k=int(n)-1
            if(j==k):
                stu_common_courses[j][k]=0
            else:
                stu_common_courses[j][k]=stu_common_courses[j][k]+1
print(stu_common_courses)







        
##        for course in course.iter('course'):
##            print(course.attrib['id'])

##intiialise a matrix A(nxn) n = no of students
##iterate over all courses:
##    c.parent = nulol
##for student_id in students:
##    iterate over courses c:
##        if (c.parent = null):
##            c.parent.append(student_id)
##        else:
##            for t in c.parent:
##                A[t][student_id]= A[t][student_id]+1

                
