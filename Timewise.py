import xml.etree.ElementTree as ET
import pandas as pd

tree = ET.parse("Test_datasets\lums-sum17.xml")

root = tree.getroot()
print(root)
NAME = root.attrib['name']
DAYS = int(root.attrib['nrDays'])
SLOTS = int(root.attrib['slotsPerDay'])
WEEKS = int(root.attrib['nrWeeks']) 

class Room:
    def __init__(self, room_id, capacity, unavailable):
        self.room_id = room_id
        self.capacity = capacity
        self.unavailable = unavailable
    def isAvailable(self, day, week, start, length):
        end = start + length
        for entry in self.unavailable:
            if entry[0][day] == '1' and entry[3][week] == '1':
                if start >= entry[1] and start < entry[1] + entry[2]:
                    return False
                elif end > entry[1] and end <= entry[1] + entry[2]:
                    return False
                elif start < entry[1] and end > entry[1] + entry[2]:
                    return False
        return True

newfile = open("timewise-lums-sum17.csv","w")
newfile.write("ID,Cap,Days,Start,Length,Weeks\n")

Rooms = []
for rooms in root.iter('rooms'):
    for room in rooms.iter('room'):
        room_id = room.attrib['id']
        capacity = room.attrib['capacity']
        unavailable = []
        if room.find('unavailable') == None:
            unavailable = []
        else:
            for unava in room.iter('unavailable'):
                unavailable.append([unava.attrib['days'], int(unava.attrib['start']), int(unava.attrib['length']), unava.attrib['weeks']])
                newfile.write(room_id +","+capacity+",'" + unava.attrib['days'] +"," + unava.attrib['start']+","+ unava.attrib['length']+",'" + unava.attrib['weeks']+"\n")
        Rooms.append(Room(room_id, capacity,unavailable))

newfile.close()
for courses in root.iter('courses'):
    for course in courses.iter('course'):
        i = 1
        for config in course.iter('config'):
            if i == 2:
                print(course.attrib)
            i += 1

