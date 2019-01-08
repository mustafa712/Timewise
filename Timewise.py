import xml.etree.ElementTree as ET
#import pandas as pd

tree = ET.parse("Test_datasets\lums-sum17.xml")

root = tree.getroot()
#print(root)
NAME = root.attrib['name']
DAYS = int(root.attrib['nrDays'])
SLOTS = int(root.attrib['slotsPerDay'])
WEEKS = int(root.attrib['nrWeeks'])

class Time:
    '''
    Variables:
        days - string of 0s and 1s of length DAYS
        start - integer representing the start slot
        length - integer representing the the length of the slot
        end - integer representing the end of slot
        weeks - string of 0s and 1s of length WEEKS
    '''
    def __init__(self,days,start,length,weeks):
        self.days = days
        self.start = start
        self.length = length
        self.end = start + length
        self.weeks = weeks
    def __key(self):
        return (self.days,self.start,self.length,self.weeks)
    def __hash__(self):
        return hash(self.__key())
    def __eq__(self,other):
        return isinstance(self, type(other)) and self.__key() == other.__key()

class Room:
    '''
    Variables:
        room_id - Room ID integer
        capacity - Room capacity integer
        unavailable - list of objects of type Time
    Functions:
        isAvailable:
            Inputs:
                day - integer between 0 to DAYS
                week - integer between 0 to WEEKS
                start - integer start slot
                end - integer end slot
            Output:
                Boolean representing whether the room is available between start and end slot on the day of the week
    '''
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
    def __key(self):
        return self.room_id
    def __hash__(self):
        return hash(self.__key())
    def __eq__(self,other):
        return isinstance(self, type(other)) and self.__key() == other.__key()


class Class:
    '''
    Variable:
        course_id - Course ID integer
        config_id - Config ID integer
        subpart_id - Subpart ID integer
        class_id - Class ID integer
        limit - Class limit integer
        room_penalty - list of a 2 element list whose first element is the object of type Room and second element is the penalty associated for the same
        time_penalty - list of a 2 element list whose first element is the object of type Time and second element is the penalty associated for the same
        ValidRoomTime - Valid Rooms and Times combinations of type RoomTime
        Functions:
            getValidRoomTime - returns a list of objects of type RoomTime which are valid for the Class
    '''
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
        self.ValidRoomTime = self.getValidRoomTime()
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
        return room_times
    def __key(self):
        return class_id
    def __hash__(self):
        return hash(self.__key())
    def __eq__(self,other):
        return isinstance(self, type(other)) and self.__key() == other.__key()


class RoomTime:
    '''
    Variables:
        room - object of type Room
        time - object of type Time
        penalty - total penalty of the room time combination
    '''
    def __init__(self,room,time,penalty):
        self.room = room
        self.time = time
        self.penalty = penalty
    def __key(self):
        return (self.room.room_id,self.time.days,self.time.start,self.time.length,self.time.weeks)
    def __hash__(self):
        return hash(self.__key())
    def __eq__(self,other):
        return isinstance(self, type(other)) and self.__key() == other.__key()

#newfile = open("timewise-lums-sum17.csv","w")
#newfile.write("ID,Cap,Days,Start,Length,Weeks\n")

Rooms = {}
for rooms in root.iter('rooms'):
    for room in rooms.iter('room'):
        room_id = int(room.attrib['id'])
        capacity = int(room.attrib['capacity'])
        unavailable = []
        if room.find('unavailable') == None:
            unavailable = []
        else:
            for unava in room.iter('unavailable'):
                unavailable.append(Time(unava.attrib['days'], int(unava.attrib['start']), int(unava.attrib['length']), unava.attrib['weeks']))
                #newfile.write(room_id +","+capacity+",'" + unava.attrib['days'] +"," + unava.attrib['start']+","+ unava.attrib['length']+",'" + unava.attrib['weeks']+"\n")
        Rooms[room_id] = Room(room_id,capacity,unavailable)

#newfile.close()
classes = {}
for courses in root.iter('courses'):
    for course in courses.iter('course'):
        course_id = int(course.attrib['id'])
        for config in course.iter('config'):
            config_id = int(config.attrib['id'])
            for subpart in config.iter('subpart'):
                subpart_id = int(subpart.attrib['id'])
                for clss in subpart.iter('class'):
                    class_id = int(clss.attrib['id'])
                    room_penalty = []
                    time_penalty = []
                    for room in clss.iter('room'):
                        room_penalty.append([Rooms[int(room.attrib['id'])],int(room.attrib['penalty'])])
                    for time in clss.iter('time'):
                        time_penalty.append([Time(time.attrib['days'], int(time.attrib['start']), int(time.attrib['length']), time.attrib['weeks']), int(time.attrib['penalty'])])
                    classes[class_id] = Class(course_id,config_id,subpart_id,class_id, int(clss.attrib['limit']))

def isClashing(time1,time2):
    """
    Input:
        time1(Time): Time object containing days, weeks, start and length data
        time2(Time): Time object containing days, weeks, start and length data
        
    Output:
        Bool: True, if the two times clash at any day of the week
    """
    for weekIndex in range(len(time1.weeks)):
        if time1.weeks[weekIndex] == time2.weeks[weekIndex]:
            for dayIndex in range(len(time1.days)):
                if time1.days[dayIndex] == time2.days[dayIndex]:
                    if time1.start < time2.start:
                        if time1.end > time2.start: return True
                    else:
                        if time2.end > time1.start: return True
    return time1.start == time2.start
