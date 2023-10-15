#!/bin/python
import sys, json
from collections import Counter

if not len(sys.argv) == 3:
    print("Invalid syntax. Please provide two json files to compare.")
    sys.exit(0)

with open(sys.argv[1], "r") as f:
    json1 = json.load(f)
with open(sys.argv[2], "r") as f:
    json2 = json.load(f)

def isobject(e):
    return isinstance(e, dict)

def isarray(e):
    return hasattr(e, '__len__') and (not isinstance(e, str))

def compareObjects(json1, json2, path):
    if not isobject(json1) or not isobject(json2):
        print("Incompatible types at '" + path + "'.")
        return False
    #print("object: " + path)
    incompatible = False
    for key in json1:
        if not key in json2:
            incompatible = True
            print("Second json file misses key '" + key + "' + at path '" + path + "'.")
    for key in json2:
        if not key in json1:
            incompatible = True
            print("First json file misses key '" + key + "' + at path '" + path + "'.")
    if incompatible:
        return False
    else:
        result = True
        path = "" if path == "/" else path
        for key in json1:
            if not compare(json1[key], json2[key], path + "/" + key):
                result = False
                print("Values differ at path '" + path + "/" + key + "'")
        return result

def compareArrays(json1, json2, path):
    if not isarray(json1) or not isarray(json2):
        print("Incompatible types at '" + path + "'.")
        return False
    #print("array: " + path + " " + str(json1.__len__()) )
    if len(json1) == 0 and len(json2) == 0:
        return True
    contentType = 0
    if isobject(json1[0]):
        contentType = 1
    elif isarray(json1[0]):
        contentType = 2
    for element in json1:
        if not isobject(element) and contentType == 1:
            print("Mixing different types in arrays is not supporter!")
            sys.exit(0)
        elif (not isarray(element) or (isobject(element) and "id" in element)) and contentType == 2:
            print("Mixing different types in arrays is not supporter!")
            sys.exit(0)
        elif (isobject(element) or isarray(element))and contentType == 0:
            print("Mixing different types in arrays is not supporter!")
            sys.exit(0)
    if contentType == 1:
        pseudoObject1 = {}
        pseudoObject2 = {}
        key = list(json1[0].keys())[0]
        for element in json1:
            pseudoObject1[element[key]] = element
        for element in json2:
            pseudoObject2[element[key]] = element
        return compare(pseudoObject1, pseudoObject2, path)
    else:
        return Counter(json1) == Counter(json2)

def compare(json1, json2, path):
    if isobject(json1) or isobject(json2):
        return compareObjects(json1, json2, path)
    elif isarray(json1) or isarray(json2):
        return compareArrays(json1, json2, path)
    else:
        return json1 == json2

if compare(json1, json2, "/"):
    print("Both files contain the same content.")
else:
    print("The content represented by both files differs.")