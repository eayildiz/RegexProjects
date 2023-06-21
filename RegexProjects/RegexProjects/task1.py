import re

regEx = "([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ )- - \[([0-9][0-9]?\/[A-Za-z]+\/[0-9][0-9][0-9][0-9])"
ipAndDateRE = re.compile(regEx)

def errorFileOpen():
    errorLog = open("error_log.txt", "w")
    if(errorLog is None):
        print("Error log file: error_log.txt could not opened.")
    return errorLog

def fileOpen():
    errorLog = errorFileOpen()
    sourceFile = open("log_task1.txt", "r")
    destinationFile = open("output_task1.txt", "w")

    if(ipAndDateRE is None):
        errorLog.write("Match object ipAndDateRE returned 'None'.\n")
    if(sourceFile is None):
        errorLog.write("Source file: log_task1.txt could not opened.\n")
    if(destinationFile is None):
        errorLog.write("Destination file: output_task1.txt could not opened.\n")
    return errorLog, sourceFile, destinationFile

def readAndWrite(sourceFile, destinationFile, errorLog):
    line = sourceFile.readline()
    nthLine = 1
    while(line != ""):
        ipAndDate = ipAndDateRE.search(line)
        if(ipAndDate is not None):
            ip = ipAndDate.group(1)
            date = ipAndDate.group(2)
            tempTuple = re.subn("/", "-", date)
            date = tempTuple[0]
            destinationFile.write(ip + date + "\n")
        else:
            errorLog.write("Compiled regex could not matched with string:\n' " + line + " ' line " + str(nthLine) + "\nRegex is: " + regEx + "\n\n")
        line = sourceFile.readline()
        nthLine = nthLine + 1

def main():
    errorLog, sourceFile, destinationFile = fileOpen()
    readAndWrite(sourceFile, destinationFile, errorLog)
    
    sourceFile.close()
    destinationFile.close()
    errorLog.close()
    
if __name__ == "__main__":
    main()