import xml.etree.ElementTree as ET
import pandas as pd

tree = ET.parse("Test_datasets\lums-sum17.xml")

root = tree.getroot()
print(root)
NAME = root.attrib['name']
DAYS = int(root.attrib['nrDays'])
SLOTS = int(root.attrib['slotsPerDay'])
WEEKS = int(root.attrib['nrWeeks'])

class Time:
    def __init__(self,days,start,length,weeks):
        self.days = days
        self.start = start
        self.length = length
        self.end = start + length
        self.weeks = weeks

class Room:
    def __init__(self, room_id, capacity, unavailable):
        self.room_id = room_id
        self.capacity = capacity
        self.unavailable = unavailable
    def isAvailable(self, day, week, start, end):
        #end = start + length
        for time in self.unavailable:
            if time.days[day] == '1' and time.weeks[week] == '1':
                if start >= time.start and start < time.end:
                    return False
                elif end > time.start and end <= time.end:
                    return False
                elif start < time.start and end > time.end:
                    return False
        return True

class Class:
    def __init__(self, course_id, config_id, subpart_id, class_id, limit, room_penalty, time_penalty):
        self.course_id = course_id
        self.config_id = config_id
        self.subpart_id = subpart_id
        self.class_id = class_id
        self.limit = limit
        #self.rooms = rooms
        #self.times = times
        self.room_penalty = room_penalty
        self.time_penalty = time_penalty
        #self.RoomTime = RoomTime
    def getValidRoomTime(self):
        room_times = []
        for room in self.room_penalty:
            for time in self.time_penalty:
                #valid = True
                for week in range(WEEKS):
                    if time[0].weeks[week] == '1':
                        for day in range(DAYS):
                            if time[0].days[day] == '1':
                                if not room[0].isAvailable(day,week,time.start,time.end):
                                    #valid = False
                                    break
                        else:
                            continue
                        break
                else:
                    room_times.append(RoomTime(room[0],time[0],room[1]+time[1]))


class RoomTime:
    def __init__(self,room,time,penalty):
        self.room = room
        self.time = time
        self.penalty = penalty
        
newfile = open("timewise-lums-sum17.csv","w")
#newfile.write("ID,Cap,Days,Start,Length,Weeks\n")

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
                unavailable.append(Time([unava.attrib['days'], int(unava.attrib['start']), int(unava.attrib['length']), unava.attrib['weeks']]))
                #newfile.write(room_id +","+capacity+",'" + unava.attrib['days'] +"," + unava.attrib['start']+","+ unava.attrib['length']+",'" + unava.attrib['weeks']+"\n")
        Rooms.append(Room(room_id,capacity,unavailable))

newfile.close()
for courses in root.iter('courses'):
    for course in courses.iter('course'):
        i = 1
        for config in course.iter('config'):
            if i == 2:
                print(course.attrib)
            i += 1

