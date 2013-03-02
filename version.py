import sys

def readVersionNumber():
    version = open("KVersion")
    versionDict = {}
    for line in version:
        key, value = line.split(" = ")
        versionDict[key] = value.split()[0]
    return "%s.%s.%s" % (versionDict['MAJOR'], versionDict['MINOR'], versionDict['FEATURE'])

def readInPomXML():
    pomdotin = open(inputFile)
    pomdotout = ""
    for line in pomdotin:

        if "@VERSION@" in line:
            beginning, end = line.split("@VERSION@")
            line = beginning + newVersionNumber + end
        pomdotout += line

    pom = open(outputFile, "w")
    pom.write(pomdotout)


if __name__ == "__main__":
    inputFile = sys.argv[1]
    outputFile = inputFile.split(".in")[0]
    newVersionNumber = readVersionNumber()
    readInPomXML()
