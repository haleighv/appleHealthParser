import sys
import os
import re
import xml.etree.ElementTree as ET

TYPE_PREFIX = "HKQuantityTypeIdentifier"
TAG_RECORD = "Record"

def fileFind(extension):
    files = [f for f in os.listdir(".") if re.match(r'.*'+extension, f)]
    return files

def parseXML(healthDataFile, keys):
    print("**Writing parsed records**")
    tree = ET.parse(healthDataFile)
    root = tree.getroot()
    with open("output.csv", "w") as outputFile:
        for child in root:
            #print(child.tag, child.attrib)
            if child.tag == TAG_RECORD:
                typeStr = child.get('type')
                dateStr = child.get("creationDate")
                valueStr = child.get("value")
                for key in keys:
                    if key == typeStr:
                        #print("%s,%s,%s"%(typeStr.replace(TYPE_PREFIX, ""), dateStr, valueStr))
                        outputFile.write("%s,%s,%s\n"%(typeStr.replace(TYPE_PREFIX, ""), dateStr, valueStr))

def scanXML(healthDataFile):
    print("**Checking health data records**")
    tree = ET.parse(healthDataFile)
    root = tree.getroot()
    recordTypes = []
    for child in root:
        if child.tag == TAG_RECORD:
            typeStr = child.get('type')
            recordTypes.append(typeStr) if typeStr not in recordTypes else None
    keys = []
    print("**Select records of interest**")
    for recordType in recordTypes:
        userInput = ''
        while (userInput != 'y') and (userInput != 'n'):
            userInput = raw_input("   Would you like to include '%s' records? [y/n]: "%recordType.replace(TYPE_PREFIX, ""))
        if userInput == 'y':
            keys.append(recordType)
    return keys

def main():
    healthDataFile = fileFind(".xml")[0]
    keys = scanXML(healthDataFile)
    parseXML(healthDataFile, keys)
    print("**DONE**")
if __name__ == "__main__":
    main()
