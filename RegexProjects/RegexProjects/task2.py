import sys
import re

class Person:
    def __init__(self, id, access_time):
        self.id = id
        self.access_time = access_time
        self.number_of_requests = 1

def monthNumber(month):
    switch = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12
    }
    return switch.get(month, 0)

def accessTime(date):
    tempList = re.split("[\W+]", date)
    day = int(tempList[0])
    try:
        month = int(tempList[1])
    except:
        month = int(monthNumber(tempList[1]))
    year = int(tempList[2])
    hour = int(tempList[3])
    minute = int(tempList[4])
    second = int(tempList[5])
    return int(day * 86400 + month * 2628288 + (year - 1970) * 31536000 + hour * 3600 + minute * 60 + second)

error_log2 = open("error_log2.txt", "w")
if(error_log2 is None):
    print("error_log2.txt file could not be opened.")
if(len(sys.argv) != 4):
    error_log2.write("# of parameters do not match with program's requirements.\n Expected input is:\n\tpython task2.py <date> <duration> <resource>\n")
targetDuration = int(sys.argv[2])
targetResource = sys.argv[3]
startDate = accessTime(sys.argv[1])
accessLimit = startDate + targetDuration

#Regex part
getRequest_re_template = "GET (.*) HTTP"
info_re_template = "([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+) - - \[([0-9]+\/[A-Za-z]+\/[0-9][0-9][0-9][0-9]:[0-9][0-9]:[0-9][0-9]:[0-9][0-9])"
getRequestsRE = re.compile(getRequest_re_template)
infoRE = re.compile(info_re_template)

#Files
sourceFile = open("log_task2.txt", 'r')
destinationFile = open("output_task2.txt", 'w')
if(sourceFile is None):
    error_log2.write("Source file: log_task2.txt could not opened.")
if(destinationFile is None):
    error_log2.write("Destination file: output_task2.txt could not opened.")

#Reading file and forming dictionary
people = {}

currentLine = sourceFile.readline()
ith_line =  1
while(currentLine != ""):
    getRequest = getRequestsRE.search(currentLine)
    if(getRequest is not None):
        product = getRequest.group(1)
        info = infoRE.search(currentLine)
        if((product == targetResource) and (info is not None)):
            id = info.group(1)
            currentAccessTime = accessTime(info.group(2))
            if(currentAccessTime < accessLimit and currentAccessTime >= startDate):
                if(id in people):
                    setattr(people[id], "number_of_requests", getattr(people[id], "number_of_requests") + 1)
                else:
                    people[id] = Person(id, currentAccessTime)
        else:
            if(info is None):
                error_log2.write("Regular expression", info_re_template, "did not match with ", ith_line, "line\n", currentLine)
    currentLine = sourceFile.readline()
    ith_line +=1

sortedPeople = {key: val for key, val in sorted(people.items(), key = lambda ele: ele[1].number_of_requests, reverse = True)}

for k,v in sortedPeople.items():
    destinationFile.write(k + " " + str(v.number_of_requests) + " " + str(v.access_time) + "\n")