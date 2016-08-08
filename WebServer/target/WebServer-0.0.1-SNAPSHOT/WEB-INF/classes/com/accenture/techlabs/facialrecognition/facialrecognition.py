import httplib
import urllib
import base64
import numpy
from PIL import Image
import glob
import pathlib2
import os
import json
import requests, time, numpy as np, operator
from os import listdir
from os.path import isfile, join
import csv
import sys

KEY_1 = "762ac81f753e4514ad8517a6034d7677"
KEY_2 = "bdc4b35b836d4d968a80437c706e4c2f"
HOST_URL = "api.projectoxford.ai"

URL_LEO = "http://www.gannett-cdn.com/-mm-/6a9564a532fa878eefae141946cf6762f7a5d370/c=0-22-1500-2022&r=537&c=0-0-534-712/local/-/media/2016/01/30/USATODAY/USATODAY/635897932182134363-GTY-507668894-79302472.JPG"
URL_ED_CHINA = "https://scontent.xx.fbcdn.net/t31.0-8/11896358_952356464828105_6692768694666984387_o.jpg"
URL_ED_SUIT = "https://scontent.xx.fbcdn.net/t31.0-8/11406518_915664685163950_3210201981848860137_o.jpg"

FACE_LIST_ID = "accenture_face_list_test"
IMAGE_DIR = '../Store/'
IMAGE_PATH = glob.glob(IMAGE_DIR + '/*.jpg')

DIRECTORY = r'/Users/colinpuri/Desktop/Faces/Primary'

PERSON_GROUP_ID = 'accenture_group'
PERSON_GROUP_ID_TEST = 'test_group'

face_id_list = list()
face_id_name_list = list()

headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': KEY_1
}

def getFaceList(group):
    #print('\n\n getFaceList():')
    body = {}
    try:
        conn = httplib.HTTPSConnection(HOST_URL)
        conn.request("GET", "/face/v1.0/persongroups/" + group + "/persons", body, headers)
        response = conn.getresponse()
        data = response.read()
        face_ids = json.loads(data)
        face_ids_name = json.loads(data)

        for face_id in face_ids:
            face_id_list.append("{personId}".format(**face_id))
            face_id_name_list.append("{name}".format(**face_id))

        #for i in range(0, len(face_id_list)):
        #    print face_id_list[i] + "/" + face_id_name_list[i]

        #print(str(len(face_id_list)) + " faces in list")

        conn.close()
    except Exception, e:
        print(e)

def getFaceListWithIndex(index):
    #print('\n\n getFaceListWithIndex(...):')
    try:
        conn = httplib.HTTPSConnection(HOST_URL)
        conn.request("GET", "/face/v1.0/facelists/" + FACE_LIST_ID, "{body}", headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        conn.close()
        return data["persistedFaces"][index]["persistedFaceId"]
    except Exception, e:
        print(e)

def getFaceListPersistentId():
    #print('\n\n getFaceListPersistentId(...):')
    try:
        conn = httplib.HTTPSConnection(HOST_URL)
        conn.request("GET", "/face/v1.0/facelists/" + FACE_LIST_ID, "{body}", headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        conn.close()
        #print data["persistedFaces"]
    except Exception, e:
        print(e)

def getFaceListCount():
    try:
        conn = httplib.HTTPSConnection(HOST_URL)
        conn.request("GET", "/face/v1.0/facelists/" + FACE_LIST_ID, "{body}", headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        conn.close()
        return len(data["persistedFaces"])
    except Exception, e:
        print(e)
        
                         
def addToFaceList(url):
    body = {}
    body['url'] = url
    json_body = json.dumps(body)
    
    try:
        conn = httplib.HTTPSConnection(HOST_URL)
        conn.request("POST", "/face/v1.0/facelists/" + FACE_LIST_ID + "/persistedFaces", json_body, headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        conn.close()
        return 
    except Exception, e:
        print(e)
        
def verifyInFaceList(faceId1, faceId2):
    #print('\n\n verifyInFaceList(...):')
    
    body = {}
    body['faceId1'] = faceId1
    body['faceId2'] = faceId2
    json_body = json.dumps(body)

    #print json_body
    
    try:
        conn = httplib.HTTPSConnection(HOST_URL)
        conn.request("POST", "/face/v1.0/verify", json_body, headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        conn.close()
    except Exception, e:
        print(e)

def detectFace(url):
    #print("\n\ndetectFace(...)")
    
    body = {}
    body['url'] = url
    json_body = json.dumps(body)
    
    params = urllib.urlencode({
        # Request parameters
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'true',
    })

    try:
        conn = httplib.HTTPSConnection(HOST_URL)
        conn.request("POST", "/face/v1.0/detect?%s" % params, json_body, headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        faceId = (data[0]["faceId"])
        conn.close()
        return faceId
        
    except Exception, e:
        print(e)

def trainPersonGroup(group):
    body = {}
    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/persongroups/" + group + "/train", body, headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        conn.close()
    except Exception, e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        

def employeeName(dir, index):
    fileList = list()
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith('.jpg'):
                fileList.append(file)
    return (str(fileList[index]).replace(".jpg", "").replace(".", " ").title().replace("Mcc", "McC"))

def employeeNameSource(dir, index):
    fileList = list()
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith('.jpg'):
                fileList.append(file)
    return (str(fileList[index]))

def employeeName(dir, index):
    fileList = list()
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith('.jpg'):
                fileList.append(file)
    return (str(fileList[index]).replace(".jpg", "").replace(".", " ").title().replace("Mcc", "McC"))

def getFileCountInDir(dir):
    count = 0
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith('.jpg'):
                count += 1
    return count

def addFaceToGroup(name, group):
    body = {}
    body['name'] = name
    json_body = json.dumps(body)

    while(True):
        try:
            response_no = 200
            conn = httplib.HTTPSConnection('api.projectoxford.ai')
            conn.request("POST", "/face/v1.0/persongroups/" + group + "/persons", json_body, headers)
            response = conn.getresponse()
            data = response.read()
            #print(data)
            conn.close()
        except Exception, e:
            print(e)
            response_no = e.errno      
        finally:
            if(response_no != 60):
                break

def addFaceToPerson(groupId, personId, url):
    body = {}
    body['url'] = url
    json_body = json.dumps(body)
    responseMessage = "error"
    
    while(responseMessage != "ok"):
        try:
            conn = httplib.HTTPSConnection('api.projectoxford.ai')
            conn.request("POST", "/face/v1.0/persongroups/" + groupId + "/persons/" + personId + "/persistedFaces", json_body, headers)
            response = conn.getresponse()
            data = response.read()
            responseMessage = json.loads(data)
            if "error" not in  str(responseMessage):
               responseMessage = "ok"
            #print data
            #print responseMessage
            conn.close()
            if "error" in str(responseMessage):
                time.sleep(4)
        except Exception, e:
            print(e)
        
def identifyFace(faceIds, group):
    body = {}
    body['personGroupId'] = group
    body['faceIds'] = faceIds
    body['maxNumOfCandidatesReturned'] = 1
    json_body = json.dumps(body)

    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/identify", json_body, headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        #print data
        returnedPerson = data[0]["candidates"][0]["personId"]
        #print returnedPerson
        return returnedPerson
        conn.close()
    except Exception, e:
        print(e)

users = {}
        
def addToDictionary(id, person):
    users[id] = person

argUrl = sys.argv[1]
	
getFaceList(PERSON_GROUP_ID_TEST)

for i in range(0, len(face_id_list)):
    addToDictionary(face_id_list[i], face_id_name_list[i])

faceListTemp = []
temporaryID = detectFace(argUrl)
faceListTemp.append(temporaryID)

face = identifyFace(faceListTemp, PERSON_GROUP_ID_TEST)
for i in range(0, len(face_id_list)):
    if(face_id_list[i] == face):
        print face_id_name_list[i]

"""
faceListTemp = []
faceListTemp.append(detectFace(URL_ED_CHINA))
print ("Hello " + identifyFace(faceListTemp, PERSON_GROUP_ID) + "!")
"""

"""
#add employee names to people group
print "\n\n"
for i in range(0, getFileCountInDir(DIRECTORY)):
    print "adding person:"
    print employeeName(DIRECTORY, i)
    addFaceToGroup(employeeName(DIRECTORY, i), PERSON_GROUP_ID)
    time.sleep(4)

#add images for training to people in people group
for i in range(0, len(face_id_name_list)):
    print (employeeName(DIRECTORY, i) + " with id " + str(users[employeeName(DIRECTORY, i)]))
    addFaceToPerson(PERSON_GROUP_ID, users[face_id_name_list[i]], "http://www.glassbyte.com/images/" + str(employeeNameSource(DIRECTORY, i)))
"""
