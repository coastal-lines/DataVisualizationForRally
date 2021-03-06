import pickle
import re
import requests
from pyral import Rally, rallyWorkset
import matplotlib.pyplot as plt
from matplotlib import pylab
import seaborn as sns
from pylab import *
from matplotlib.ticker import MaxNLocator
import mplcursors
import pandas as pd
from Project.RallyCommonObject import RallyCommonObject
from Project.UserCredential import UserCredential
from Project.RallyInstance import RallyInstance
from Project.RallyFolder import RallyFolder
from Project.RallyWorkspace import RallyWorkspace
from Visualization.UserDataObjects.BarClass import BarClass
from Visualization.TestsAndFoldersActions import TestsAndFoldersActions
from Visualization.DataFrameActions import DataFrameActions

class TestCase():
    def __init__(self, rootFolderName, formattedID, name, preConditions, productArea, productSubarea, method, testFolder, inputs, expecteds):
        self.rootFolderName = rootFolderName
        self.formattedID = formattedID
        self.name = name
        self.preConditions = preConditions
        self.project = project
        self.productArea = productArea
        self.productSubarea = productSubarea
        self.method = method
        self.testFolder = testFolder
        self.inputs = inputs
        self.expecteds = expecteds

userTestCasesFromFile = None
with open(r'C:\Temp2\New folder\DataVisualizationAndStatisticsForRally\Draft\listTestCases2.data', 'rb') as file:
    userTestCasesFromFile = pickle.load(file)

#query = '(Name !contains "Flash")'
query = '((Name !contains "Flash") AND (Name contains "Images"))'

result = re.findall('\((.*?)\)', query)
selectedUserTestCases = []

userTestCasesFromFileCopy = userTestCasesFromFile.copy()

#!!!Возможно нужно добавить break для оптимизации
def removeTestCasesFromList(what, text):
    for tc in userTestCasesFromFile:
        if what == "Name":
            for tc in userTestCasesFromFileCopy:
                if text in tc.name:
                    index = userTestCasesFromFileCopy.index(tc)
                    userTestCasesFromFileCopy.pop(index)
        elif what == "PreCondition":
            for tc in userTestCasesFromFileCopy:
                if text in tc.preConditions:
                    index = userTestCasesFromFileCopy.index(tc)
                    userTestCasesFromFileCopy.pop(index)
        elif what == "Project":
            for tc in userTestCasesFromFileCopy:
                if text in tc.project:
                    index = userTestCasesFromFileCopy.index(tc)
                    userTestCasesFromFileCopy.pop(index)
        elif what == "ProductArea":
            for tc in userTestCasesFromFileCopy:
                if text in tc.productArea:
                    index = userTestCasesFromFileCopy.index(tc)
                    userTestCasesFromFileCopy.pop(index)
        elif what == "ProductSubarea":
            for tc in userTestCasesFromFileCopy:
                if text in tc.productSubarea:
                    index = userTestCasesFromFileCopy.index(tc)
                    userTestCasesFromFileCopy.pop(index)
        elif what == "Method":
            for tc in userTestCasesFromFileCopy:
                if text in tc.method:
                    index = userTestCasesFromFileCopy.index(tc)
                    userTestCasesFromFileCopy.pop(index)
        elif what == "TestFolder":
            for tc in userTestCasesFromFileCopy:
                if text in tc.testFolder:
                    index = userTestCasesFromFileCopy.index(tc)
                    userTestCasesFromFileCopy.pop(index)
        elif what == "Inputs":
            for tc in userTestCasesFromFileCopy:
                for input in tc.inputs:
                    if text in input:
                        index = userTestCasesFromFileCopy.index(tc)
                        userTestCasesFromFileCopy.pop(index)
        elif what == "ExpectedResults":
            for tc in userTestCasesFromFileCopy:
                for expected in tc.expecteds:
                    if text in expected:
                        index = userTestCasesFromFileCopy.index(tc)
                        userTestCasesFromFileCopy.pop(index)


#pre-removing test cases
for query in result:
    what = query.replace('(', '').replace(')', '').split()[0]
    action =  query.split()[1]
    text = query.split()[2].replace('"', '')

    if(action == "!contains" or action == "!="):
        removeTestCasesFromList(what, text)

#common loop for searching custom test cases
for query in result:
    what = query.replace('(', '').replace(')', '').split()[0]
    action =  query.split()[1]
    text = query.split()[2].replace('"', '')

    if what == "Name":
        if "contains" in action or "=" in action:
            for tc in userTestCasesFromFile:
                if text in tc.name:
                    selectedUserTestCases.append(tc)
    elif what == "PreCondition":
        if "contains" in action or "=" in action:
            for tc in userTestCasesFromFile:
                if text in tc.preConditions:
                    selectedUserTestCases.append(tc)
    elif what == "Project":
        if "contains" in action or "=" in action:
            for tc in userTestCasesFromFile:
                if text in tc.project:
                    selectedUserTestCases.append(tc)
    elif what == "ProductArea":
        if "contains" in action or "=" in action:
            for tc in userTestCasesFromFile:
                if text in tc.productArea:
                    selectedUserTestCases.append(tc)
    elif what == "ProductSubarea":
        if "contains" in action or "=" in action:
            for tc in userTestCasesFromFile:
                if text in tc.productSubarea:
                    selectedUserTestCases.append(tc)
    elif what == "Method":
        if "contains" in action or "=" in action:
            for tc in userTestCasesFromFile:
                if text in tc.method:
                    selectedUserTestCases.append(tc)
    elif what == "TestFolder":
        if "contains" in action or "=" in action:
            for tc in userTestCasesFromFile:
                if text in tc.testFolder:
                    selectedUserTestCases.append(tc)
    elif what == "Inputs":
        if "contains" in action or "=" in action:
            for tc in userTestCasesFromFile:
                for input in tc.inputs:
                    if text in input:
                        selectedUserTestCases.append(tc)
                    break
    elif what == "ExpectedResults":
        if "contains" in action or "=" in action:
            for tc in userTestCasesFromFile:
                for expected in tc.expecteds:
                    if text in expected:
                        selectedUserTestCases.append(tc)
                    break

#перед подготовкой bars нужно собрать инфу про найденные кейсы
#находим номера кейсов
#далее находим parent
#далее алгоритм как для остальных запросов

#get response with User's query
#self.testCasesFromUserQuery = self.rally.get('TestCase', fetch = True, projectScopeDown = True, query = query)

#get root test folders according the main root folder
rootFolder = RallyFolder(self.rally ,'FormattedID = "' + rootFolderFormattedID + '"').testFolder
listRootSubfolders = rootFolder.Children

bars = TestsAndFoldersActions().getCustomUserRequest(self.testCasesFromUserQuery, listRootSubfolders)
tidyDataForCustomUserQuery = DataFrameActions.PrepareDataFrame(bars)