#!/bin/python

f = open("/tmp/g", "r")
for line in f.readlines():
    d = line.strip().split("|")
    date = d[0]
    m = {"iciciupi" : 0, "hdfcupi" : 0, "yesupi" : 0, "indusupi": 0}
    for srPair in d[1:-1]:
        #print(srPair)
        kv = srPair.split("@")
        m[kv[0]] = kv[1]
    print(date, "|", m["iciciupi"], "|", m["yesupi"], "|", m["indusupi"], "|", m["hdfcupi"])

f.close()
