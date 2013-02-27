#!/usr/bin/env python
from __future__ import print_function
from random import choice

import json
import dns.resolver
import socket
import argparse

args = None
types = ['A', 'AAAA', 'MX', 'NS', 'ANY', 'CNAME', 'DNAME', 'DNSKEY', 'DS', 'PTR']

class DamballaParser:
    def findYesterdaysLosses(self, yesterday, today):
        losses = []
        losses.append(item for item in yesterday if item not in today)
        return losses

    def eatFile(self, filename):
        domainList = []
        with open(filename, "r") as file:
            jsonData = json.loads(file.readline())
            for key in jsonData.keys():
                entry = jsonData[key]
                for domain in entry[u'domains']:
                    domainList.append(domain[u'name'])
        return domainList

    def queryForAddressAgainstAVantio(self, address, vantio=None, type='A'):
        resolver = dns.resolver.Resolver()
        if args.randomize:
            type = choice(types)
            if args.verbose:
                print("randomized type choice = %s" % type)

        if vantio:
            resolver.nameservers = [socket.gethostbyname(vantio)]

        try:
            rdata = resolver.query(address, type)
            return dns.rcode.to_text(rdata.response.rcode())
        except Exception:
            return "NXDOMAIN"

def printf(str, *args):
    print(str % args, end='')

def printOutput(today):
    linecounter = 80

    for entry in today:

        rcode = dp.queryForAddressAgainstAVantio(entry, vantio=args.host)
        if rcode != "NXDOMAIN":
            if args.verbose:
                print("%s ON %s" % (rcode, entry))
            else:
                printf('-')
        else:
            printf('.')

        linecounter -= 1
        if linecounter < 0:
            print("")
            linecounter = 80

def makeDnsPerfList(list):
    dnsPerfList = open("dnsperflist", "w")


    type='A'

    for item in today:
        if args.randomize:
            type = choice(types)
            if args.verbose:
                print("randomized type choice = %s" % type)

        dnsPerfList.write("%s %s\n" % (item, type))

def parseCmdLine():
    parser = argparse.ArgumentParser(description="Process JSON feed for dns testing of security feeds")
    parser.add_argument('-t', '--today', default="today.json", help="File for processing, default is today.json")
    parser.add_argument('-y', '--yesterday', default="yesterday.json", help="File for processing, default is yesterday.json")
    parser.add_argument('--host', default="8.8.8.8", help="vantio host to query against")

    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-c', '--continuous', action='store_true')
    parser.add_argument('-r', '--randomize', action='store_true', help='Randomize query types')
    parser.add_argument('-a', '--action', default='query', help=("action to perform (dnsperf, query)"))

    return parser.parse_args()

def yesterdaysLosses(today, yesterday):
    theFile = open("losses", "w")
    theFile.write("%s\n" % (item for item in yesterday if item not in today))

def actionQuery(list):
    if args.continuous:
        while (True):
            printOutput(list)
            print("looping")

    else:
        printOutput(list)


if __name__ == "__main__":
    dp = DamballaParser()

    args = parseCmdLine()
    today = dp.eatFile(args.today)

    if args.action == "cut":
        with open("today.json", "r") as file:
            for line in file:
                print(line[:5000])
        exit()
    elif args.action == "query":
        actionQuery(today)
    elif args.action == "dnsperf":
        makeDnsPerfList(today)
    elif args.action == "losses":
        dp.yesterdaysLosses(today, dp.eatFile(args.yesterday))
