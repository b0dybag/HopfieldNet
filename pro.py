# -*- coding: utf-8 -*-

import csv
import network
import numpy
import binascii

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

def toString(someArray):
    tempString = ' '.join(str(tmp) for tmp in someArray)
    return tempString

def toBinary(someString):
    tempData = ' '.join(format(ord(x), 'b') for x in someString)
    return tempData

def fromBin(lol):
    for k in range(len(lol)):
        if lol[k]==-1: lol[k]="0"
        if lol[k]==1: lol[k]="1"
    lol = toString(lol)
    #print(lol)
    lol = lol.replace("0.0", "0")
    lol = lol.replace("1.0", "1")
    lol = lol.replace(" ", "")
    #print(lol)
    lol = list(lol)
    a=0
    tmp = lol[a]
    while tmp!="1":
        lol[a]=""
        a=a+1
        tmp = lol[a]
    lol = "".join(lol)
    #print(lol)
    n=6
    lol = [lol[i:i+n] for i in range(0, len(lol), n)]
    str1 = ""
    for j in range(len(lol)):
        n = text_from_bits(lol[j])
        str1=str1+n
    return str1

with open('data.csv', newline='') as csvfile:
    fulldata = list(csv.reader(csvfile, delimiter=';'))
i=0
head = fulldata.pop(0)
brokendata = []
gooddata = []
for col in fulldata:
    for sim in col:
        if sim == '-200':#--------------------------- BROKEN DATA IDENTIFICATOR
            brokendata.append(col)
            break   
    if (len(brokendata) == 0) or (col != brokendata[len(brokendata)-1]):
        if toString(col): #print("not mpty col:", col)
            gooddata.append(col)

def toMinusOne(goodDataSample):
    tempstr = toString(goodDataSample)
    tmp = toBinary(tempstr)
    tmp = tmp.replace(" ", "")  #max len 408
    if len(tmp)>599: print("WARNING")
    tmp = "".join("0" for i in range(600-len(tmp)))+tmp
    bi = list(tmp)
    for j in range(len(bi)):
        if bi[j]=="0": bi[j]=-1
        if bi[j]=="1": bi[j]=1
    return bi

model = network.HopfieldNetwork()

gooddata=[gooddata[0], gooddata[1], gooddata[2], gooddata[3]]
print(gooddata[0])
print(gooddata[1])
print(gooddata[2])
print(gooddata[3])

bingooddata = [toMinusOne(d) for d in gooddata]
cmon = numpy.array(bingooddata)

#print("----")
#print(fromBin(cmon[3]))
#print("----")

model.train_weights(cmon)
print("done!")

brokendata=[brokendata[0], brokendata[1], brokendata[2], brokendata[3]]
#, brokendata[4], brokendata[5], brokendata[6], brokendata[7], brokendata[8], brokendata[9], brokendata[10]
print(brokendata[0])
print(brokendata[1])
print(brokendata[2])
print(brokendata[3])

ex = [toMinusOne(t) for t in brokendata]
ex = numpy.array(ex)

#print("----")
#print(fromBin(ex[3]))
#print("----")

#print(ex[0])
predicted = model.predict(ex, threshold=0, asyn=True)


for i in range(len(predicted)):
    print(fromBin(predicted[i]))
