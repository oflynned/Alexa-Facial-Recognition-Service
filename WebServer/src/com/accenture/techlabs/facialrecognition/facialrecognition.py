"""
Author Edmond O' Flynn
"""

import httplib
import json
import os
import sys
import time
import urllib
import math

KEY_1 = "667f399a4e4046c0b37ddef39b4bf2fa"
HOST_URL = "api.projectoxford.ai"

DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "/images/"
PERSON_GROUP_ID = 'accenture_group'

face_id_list = list()
face_id_name_list = list()
users = {}

header = {
    'Ocp-Apim-Subscription-Key': KEY_1
}
header_octet = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': KEY_1
}


def get_face_list(group):
    body = {}
    try:
        conn = httplib.HTTPSConnection(HOST_URL)
        conn.request("GET", "/face/v1.0/persongroups/" + group + "/persons", body, header)
        response = conn.getresponse()
        data = response.read()
        face_ids = json.loads(data)

        for face_id in face_ids:
            face_id_list.append("{personId}".format(**face_id))
            face_id_name_list.append("{name}".format(**face_id))

        for j in range(0, len(face_id_list)):
            # sys.stdout.write(face_id_list[j] + "/" + face_id_name_list[j] + "\n")
            # sys.stdout.flush()
            add_to_dictionary(face_id_list[j], face_id_name_list[j])

        # sys.stdout.write("\n" + str(len(face_id_list)) + " faces in list" + "\n")
        # sys.stdout.flush()
        conn.close()
    except Exception, e:
        print e


def detect_face(url):
    body = {'url': url}
    json_body = json.dumps(body)
    params = urllib.urlencode({
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'true',
    })

    try:
        conn = httplib.HTTPSConnection(HOST_URL)
        conn.request("POST", "/face/v1.0/detect?%s" % params, json_body, header)
        response = conn.getresponse()
        data = json.loads(response.read())
        face_id = (data[0]["faceId"])
        conn.close()
        return face_id

    except Exception, e:
        print e

def detect_face_image(image):
    body = image
    params = urllib.urlencode({
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'true',
    })

    try:
        conn = httplib.HTTPSConnection(HOST_URL)
        conn.request("POST", "/face/v1.0/detect?%s" % params, body, header_octet)
        response = conn.getresponse()
        data = json.loads(response.read())
        face_id = (data[0]["faceId"])
        conn.close()
        return face_id

    except Exception, e:
        print e

def employee_name_source(directory, index):
    file_list = list()
    for root, dirs, files in os.walk(directory):
        for element in files:
            if element.endswith('.jpg'):
                file_list.append(element)
    return str(file_list[index])


def employee_name(directory, index):
    return employee_name_source(directory, index).replace(".jpg", "").replace(".", " ").title() \
        .replace("Mcc", "McC").replace("Mcm", "McM").replace("Mca", "McA")


def employee_file_name(name):
    return name.replace(" ", ".").lower()


def get_file_count_in_dir(directory):
    count = 0
    for root, dirs, files in os.walk(directory):
        for element in files:
            if element.endswith('.jpg'):
                count += 1
    return count


def add_face_to_group(name, group):
    body = {'name': name}
    json_body = json.dumps(body)

    while True:
        try:
            response_no = 200
            conn = httplib.HTTPSConnection(HOST_URL)
            conn.request("POST", "/face/v1.0/persongroups/" + group + "/persons", json_body, header)
            response = conn.getresponse()
            data = response.read()
            sys.stdout.write(str(data) + "\n")
            sys.stdout.flush()
            conn.close()
        except Exception, e:
            print e
            response_no = e.errno
        finally:
            if response_no != 60:
                break


def add_face_to_person(person_id, image):
    response_message = "error"
    sys.stdout.flush()

    # print person_id

    while response_message != "ok":
        try:
            conn = httplib.HTTPSConnection(HOST_URL)
            conn.request("POST",
                         "/face/v1.0/persongroups/" + PERSON_GROUP_ID + "/persons/" + person_id + "/persistedFaces",
                         image, header_octet)
            response = conn.getresponse()
            data = response.read()
            response_message = json.loads(data)
            if "error" not in str(response_message):
                response_message = "ok"
                conn.close()
            if "error" in str(response_message):
                time.sleep(4)
        except Exception, e:
            print e


def identify_face(face_ids):
    # print face_ids
    body = {'personGroupId': PERSON_GROUP_ID, 'faceIds': face_ids, 'maxNumOfCandidatesReturned': 1}
    json_body = json.dumps(body)
    try:
        conn = httplib.HTTPSConnection(HOST_URL)
        conn.request("POST", "/face/v1.0/identify", json_body, header)
        response = conn.getresponse()
        data = json.loads(response.read())
        # print data
        returned_person = data[0]["candidates"][0]["personId"]
        confidence = int(math.ceil(data[0]["candidates"][0]["confidence"] * 100))
        conn.close()
        names = "{\"name\":\"" + users[returned_person] + "\",\"confidence\":\"" + str(confidence) + "\"}"
        print names

    except Exception, e:
        print e


def print_invalid():
    print("Not a valid argument for the given command" +
          "\n\n" +
          "Enter commands in this fashion:" +
          "\n" +
          "python <cmd> <optional endpoint>" +
          "\n\n" +
          "Options for <cmd> are:\n" +
          "<create> \t-> Creates a new facelist enabling images to be added to it for comparisons\n" +
          "<add> \t\t-> Adds faces to a facelist with names of people from a folder of images in the format <forename.surname.jpg>\n" +
          "<train> \t-> Trains a group when images have been added to individual faces\n" +
          "<check> \t-> Checks current training of the group once training has been called\n" +
          "<get> <url> \t-> Checks an image against the face group and returns the name if it matches within a tolerance\n" +
          "<nuke> \t\t-> Purges the group and does everything in the correct order for you. Use this if you don't want to do things manually.\n\n" +
          "For regular use, you'll most likely just use <nuke> and <get>.\n\n" +
          "eg\tpython nuke\n\tpython get http://www.example.com/edmond.o.flynn.jpg\n\tpython get http://www.example/com/john.smith.jpg\n\n" +
          "Make sure the folder of images is named appropriately as ./images/ where the script is located, and that all names use a dot for a space")


def add_to_dictionary(user_id, person):
    users[user_id] = person


def purge_group():
    params = {}
    body = {}
    try:
        conn = httplib.HTTPSConnection(HOST_URL)
        conn.request("DELETE", "/face/v1.0/persongroups/" + PERSON_GROUP_ID + "?%s" % params, body, header)
        respond(purge_group.__name__, conn)
        sys.stdout.write("\neverything has been nuked lol\n")
        sys.stdout.flush()
    except Exception, e:
        print e


def create_group():
    params = {}
    body = {
        "name": PERSON_GROUP_ID,
        "userData": PERSON_GROUP_ID
    }

    try:
        conn = httplib.HTTPSConnection(HOST_URL)
        conn.request("PUT", "/face/v1.0/persongroups/" + PERSON_GROUP_ID + "?%s" % params, json.dumps(body), header)
        respond(create_group.__name__, conn)
    except Exception, e:
        print e


def check_training():
    sys.stdout.write("\n\nchecking training" + "\n")
    params = {}
    body = {}
    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("GET", "/face/v1.0/persongroups/" + PERSON_GROUP_ID + "/training?%s" % params, body, header)
        response = conn.getresponse()
        data = response.read()
        sys.stdout.write(str(data))
        sys.stdout.flush()
        conn.close()
    except Exception, e:
        print e


def respond(method_name, conn):
    response = conn.getresponse()
    data = response.read()
    if not data:
        if method_name == purge_group.__name__:
            sys.stdout.write(PERSON_GROUP_ID + " successfully purged\n")
        elif method_name == create_group.__name__:
            sys.stdout.write(PERSON_GROUP_ID + " successfully created\n")
    else:
        sys.stdout.write("'" + data + "'" + "\n")

    sys.stdout.flush()
    conn.close()


def add_to_group():
    sys.stdout.write("\n\nadding to group:\n")
    for i in range(0, get_file_count_in_dir(DIRECTORY)):
        sys.stdout.write("\nadding person:" + "\n")
        sys.stdout.write(employee_name(DIRECTORY, i) + "\n")
        sys.stdout.flush()
        add_face_to_group(employee_name(DIRECTORY, i), PERSON_GROUP_ID)
        time.sleep(4)
    sys.stdout.write("completed generating faces" + "\n")
    sys.stdout.flush()


def train_group():
    get_face_list(PERSON_GROUP_ID)
    sys.stdout.write("training group with range " + str(len(face_id_name_list)) + "\n")
    sys.stdout.flush()
    users = dict(zip(face_id_list, face_id_name_list))

    for index, user in enumerate(users):
        person_image = open(DIRECTORY + employee_file_name(users[user]) + ".jpg", 'rb').read()
        sys.stdout.write(user + " " + str(users[user]) + "\n\n")
        sys.stdout.flush()
        add_face_to_person(user, person_image)

    params = {}
    body = {}

    try:
        conn = httplib.HTTPSConnection(HOST_URL)
        conn.request("POST", "/face/v1.0/persongroups/" + PERSON_GROUP_ID + "/train?%s" % params, body, header)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception, e:
        print e


def get_image_name():
    try:
        person_image = open(sys.argv[2], 'rb').read()
        arg_url = sys.argv[2]
        sys.stdout.flush()
        get_face_list(PERSON_GROUP_ID)
        for i in range(0, len(face_id_list)):
            add_to_dictionary(face_id_list[i], face_id_name_list[i])
        face_list_temp = []
        temporary_id = detect_face_image(person_image)
        face_list_temp.append(temporary_id)
        identify_face(face_list_temp)
    except IndexError:
        print_invalid()


argFunction = sys.argv[1]

if not argFunction:
    print_invalid()
else:
    if argFunction == "create":
        purge_group()
        create_group()
    elif argFunction == "add":
        add_to_group()
    elif argFunction == "train":
        train_group()
    elif argFunction == "check":
        check_training()
    elif argFunction == "get":
        get_image_name()
    elif argFunction == "nuke":
        purge_group()
        create_group()
        add_to_group()
        train_group()
        check_training()
    else:
        print_invalid()
