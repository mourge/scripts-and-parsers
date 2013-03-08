#!/usr/bin/env python

import sys
import argparse

args = None

def readVersionNumberFromFile():
    version = open(args.version)
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

def parseCmdLine():
    parser = argparse.ArgumentParser(description="Convert version numbers in <input> file, creat <output> file")

    parser.add_argument('-i', '--input', default="pom.xml.in", help="Input File")
    parser.add_argument('-o', '--output', default="pom.xml", help="Output File")
    parser.add_argument('-s', '--version', default="KVersion", help="File for processing, default is yesterday.json")
    parser.add_argument('-n', '--number', action='store_true', help="add hardcoded version number")

    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-r', '--randomize', action='store_true', help='Randomize query types')

    return parser.parse_args()

if __name__ == "__main__":
    args = parseCmdLine()

    inputFile = args.input
    outputFile = args.output
    newVersionNumber = None
    if args.number:
        newVersionNumber = "1.0.0" # args.number
    else:
        newVersionNumber = readVersionNumberFromFile()

    readInPomXML()
