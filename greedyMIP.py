# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 18:37:06 2019

@author: Akul Bansal
"""

from Timewise import *
import pulp as solver
import datetime as dt

def greedyRoomTimeAssignment(classList):
    """
    Input:
        classList: List of all class objects       
    Output:
        updated list with room-time object assignment to class objects
    """
    
    classDict = {}
    for classroom in classList:
        classDict[classroom.class_id] = classroom
    classIDList = classDict.keys()
    problem = solver.LpProblem("RoomTimeAssignment", solver.LpMinimize)
    
    variableDict = {}
    #Declaring the binary variables
    for classID in classIDList:
        variableDict[classID] = {}
        for validRoomTime in classDict[classID].getValidRoomTime():
            variableDict[classID][validRoomTime] = \
            solver.LpVariable("x"+classID+"_"+ str(validRoomTime),cat = "Binary")
    
    #Objective Function
    problem += solver.lpSum([variableDict[classID][validRoomTime]*validRoomTime.penalty \
                             for classID in classIDList \
                             for validRoomTime in classDict[classID].getValidRoomTime()])
    
    #Constraint to ensure only one of the available roomtimes is picked
    for classID in classIDList:
        problem += solver.lpSum([variableDict[classID][validRoomTime] for validRoomtTime in classDict[classID].getValidRoomTime()]) == 1
            
    
    
    #Constraint to avoid clashes between classes
    for classID1 in classIDList:
        for validRoomTime1 in classDict[classID1].getValidRoomTime():
            for classID2 in classIDList:
                for validRoomTime2 in classDict[classID2].getValidRoomTime():
                    if isGlobalClash(validRoomTime1, validRoomTime2):
                        problem += variableDict[classID1][validRoomTime1] + variableDict[classID2][validRoomTime2] <= 1
                
    #Calling the CBC solver
    newFile = open("output-"+str(dt.datetime.now())+".csv","w")
    problem.solve()
    for classID in classIDList:
        for validRoomTime in classDict[classID].getValidRoomTime():
            if variableDict[classID][validRoomTime].value() > 0.5:
                out = str(classID)+","
                out += validRoomTime.time.days + ","
                out += str(validRoomTime.time.start) +","
                out += str(validRoomTime.time.weeks) + ","
                out += str(validRoomTime.room.roomID)
                newFile.write(out)
    newFile.close()
            
            
    

