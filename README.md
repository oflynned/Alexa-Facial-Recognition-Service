# Facial RESTful Service
Service for recognising a face from a group with an interface with Alexa for voice service, and hosted on a Tomcat server

This service consists of multiple parts: a tomcat server, a webcam service, python script for Microsoft API, and an Alexa skill for user interaction.

##Webcam Service
This service is run locally on the computer, and posts a stream of images every 1s to the Tomcat server. It requires the server to be up and running first in order to post images to it.

##Tomcat Webserver
This webserver acts as a conduit for storing images posted, handling connections, allowing the latest images to be retrieves via URL params, and automatically grooms the images older than 30s to be disposed of. The server uses Jython to invoke a Python script in bash from the directory, and using a callback it returns the output to the get request. The server should be hosted on an AWS EC2 instance.

##Microsoft API Python Script
There is one script associated with this project. It is invoked by the webserver for checking a face against a group and also returns a confidence interval. The group must first be trained. A few important notes, as I did not have hosting for the project where images were publicly accessible, I used my own webserver. The images for training should be in a folder locally and remotely. For locally, it just polls the names, sanitises them, and creates a person name with the given entry's name. The remote folder should contain the same files and filenames, this is so that the images can be used in training for Microsoft API.

There are a few options for arguments in command line with ``python <cmd> <optional endpoint>``

```
$ python ./facialrecognition.py create
```
Creates a new facelist enabling images to be added to it for comparisons

```
$ python ./facialrecognition.py add
```
Adds faces to a facelist with names of people from a folder of images in the format <forename.surname.jpg>

```
$ python ./facialrecognition.py train
```
Trains a group when images have been added to individual faces
  
```
$ python ./facialrecognition.py check
```
Checks current training of the group once training has been called

```  
$ python ./facialrecognition.py get <url>
```
Checks an image against the face group and returns the name if it matches within a tolerance
  
```
$ python ./facialrecognition nuke
```
Purges the group and does everything in the correct order for you. Use this if you don't want to do things manually. For regular use, you'll most likely just use <nuke> and <get>. For example: 
```
$ python nuke
$ python get http://www.example.com/edmond.o.flynn.jpg
$ python get http://www.example.com/john.smith.jpg
```

##Alexa Skill
The Alexa skill associated with this allows the user to interact with the the service by invoking it by voice. 
```
"Alexa, open facial recognition"
"Recognise me"
"I am approximately 85% confident that you're Edmond O' Flynn"
```

The Alexa skill relies on the stream of images being sent to the server to be checked. The scripts are invoked with the latest images URL as a parameter for the image comparison against a group.
