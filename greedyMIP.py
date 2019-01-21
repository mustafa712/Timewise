# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 18:37:06 2019

@author: Akul Bansal
"""

from Timewise import *
import pulp as solver
import datetime as dt

def greedyRoomTimeAssignment(classDict = getAllClasses()):
    """
    Input:
        classList: List of all class objects       
    Output:
        updated list with room-time object assignment to class objects
    """
    
    #classDict = getAllClasses()
    #for classroom in classList:
        #classDict[classroom.class_id] = classroom
    classIDList = classDict.keys()
    problem = solver.LpProblem("RoomTimeAssignment", solver.LpMinimize)
    
    variableDict = {}
    #Declaring the binary variables
    for classID in classIDList:
        variableDict[classID] = {}
        for ukey in classDict[classID].ValidRoomTime:
            variableDict[classID][ukey] = \
            solver.LpVariable("x"+str(classID)+"_"+ ukey,cat = "Binary")
    
    #Objective Function
    problem += solver.lpSum([variableDict[classID][ukey]*validRoomTime.penalty \
                             for classID in classIDList \
                             for ukey, validRoomTime in classDict[classID].ValidRoomTime.items()])
    
    #Constraint to ensure only one of the available roomtimes is picked
    for classID in classIDList:
        lst = []
        #for ukey, RT in classDict[classID].ValidRoomTime.items():
        #print(RT.room.room_id, RT.time.unique_key, RT.u_key, RT.penalty)
        for ukey in classDict[classID].ValidRoomTime:
            #print(ukey)
            #print(variableDict[classID][ukey])
            lst.append(variableDict[classID][ukey])
        #print(classID,lst)
        problem += solver.lpSum(lst) == 1, "Class_" + str(classID)
            
    #Constraint to avoid clashes between classes
    for classID1 in classIDList:
        for ukey1, validRoomTime1 in classDict[classID1].ValidRoomTime.items():
            for classID2 in classIDList:
                if classID2 != classID1:
                    for ukey2, validRoomTime2 in classDict[classID2].ValidRoomTime.items():
                        if isGlobalClash(validRoomTime1, validRoomTime2):
                            problem += variableDict[classID1][ukey1] + variableDict[classID2][ukey2] <= 1, str(classID1) + "_" + ukey1 +"_" + str(classID2) + "_" + ukey2
                
    problem.writeLP("lums-sum17.lp")
    #Calling the CBC solver
    print("File started")
    newFile = open("output-"+str(dt.datetime.now())+".csv","w")
    problem.solve()
    print(solver.LpStatus[problem.status])
    for classID in classIDList:
        print("variables printing started")
        for ukey, validRoomTime in classDict[classID].ValidRoomTime.items():
            if variableDict[classID][ukey].value() > 0.5: 
                out = str(variableDict[classID][ukey].name) + ","
                out += str(variableDict[classID][ukey].value()) + ","
                out += str(classID)+","
                out += validRoomTime.time.days + ","
                out += str(validRoomTime.time.start) +","
                out += str(validRoomTime.time.weeks) + ","
                out += str(validRoomTime.room.room_id) + "\n"
                newFile.write(out)
    newFile.close()
greedyRoomTimeAssignment()
