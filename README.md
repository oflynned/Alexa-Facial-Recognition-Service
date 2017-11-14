# Facial RESTful Service
Service for recognising a face from a group with an interface with Alexa for voice service, and hosted on a Tomcat server

This service consists of multiple parts: a tomcat server, a webcam service, python script for Microsoft API, and an Alexa skill for user interaction.

## Webcam Service
This service is run locally on the computer, and posts a stream of images every 1s to the Tomcat server. It requires the server to be up and running first in order to post images to it.

## Tomcat Webserver
This webserver acts as a conduit for storing images posted, handling connections, allowing the latest images to be retrieves via URL params, and automatically grooms the images older than 30s to be disposed of. The server uses Jython to invoke a Python script in bash from the directory, and using a callback it returns the output to the get request. The server should be hosted on an AWS EC2 instance.

## Microsoft API Python Script
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
Checks an image against the face group and returns the name and confidence if it matches within a tolerance
  
```
$ python ./facialrecognition nuke
```
Purges the group and does everything in the correct order for you. Use this if you don't want to do things manually. For regular use, you'll most likely just use *nuke* and *get*. For example: 
```
$ python nuke
$ python get http://www.glassbyte.com/images/edmond.o.flynn.jpg
```

Please note that URLs must be in the form of ``http://www.example.com/edmond.o.flynn.jpg`` remotely, and the name must correspond to its remote counterpart locally. 

## Alexa Skill
The Alexa skill associated with this allows the user to interact with the the service by invoking it by voice. 
```
"Alexa, open facial recognition"
"Recognise me"
"I am approximately 85% confident that you're Edmond O' Flynn"
```

The Alexa skill relies on the stream of images being sent to the server to be checked. The scripts are invoked with the latest images URL as a parameter for the image comparison against a group.

## How to Run
### Training Your Own Facelist
Get your own Microsoft API key and replace the KEY variable in the facialrecognition.py file with it.  
In the same folder as the python file, create a folder called images. Put all of your training images in here. They will be used for their filenames.  
On a publicly available webhost, upload the same images to there and replace the ``http://www.glassbyte.com/images/`` URL with your own. The images must be uploaded to a webserver so that the Microsoft API can discover them.  
Run ``python ./facialrecognition nuke`` and then when this finishes, check its training with ``python ./facialrecognition check``. Your facelist should now be trained.  

### Tomcat Server Webapp
Run with Eclipse Jee Neon and Java EE. The dependencies should already be included as .jar files. If not, the following .jar files are needed:  
* Jersey 2.23.1 Container Servlet
* Jersey 2.23.1 Common
* Jersey 2.23.1 Server
* Jersey 2.23.1 Client
* Jersey 2.23.1 Media Multipart
* Mimepull 1.9.6
* Jython Standalone 2.5.2

Open the project, right click on the project, export > WAR file.  
Use this file to upload to a Tomcat installation on an AWS EC2 instance. Make sure that the appropriate ports are open.  

### Interacting with the Tomcat Service
The service takes GET and POST requests with parameters to various URLs. 

*GET* ``.../WebServer/rest/image/name/{name}`` Returns in JSON format the result of the {name} parameter passed, corresponding to http://www.glassbyte.com/images/{name}.jpg. Used for debug for finding out the name and confidence of known static images  
*GET* ``.../WebServer/rest/image/name/`` Returns in JSON format the result of the latest image uploaded to the Tomcat service when processed with the Python script, returning the name and the confidence level.  
*GET* ``.../WebServer/rest/image/latestImage`` Returns a jpeg format mime type of the latest image uploaded for viewing.  
*POST* ``.../WebServer/rest/image/upload`` Receives an image that has been posted to the address, and saves the item as the current time in milliseconds which is then used for grooming images later, ie removing images that are more than 30s old.  

### Webcam Setup
Open with Intellij IDEA as it was written using this IDE. Change the destination of where the images will be sent by modifying the *POST_ADDRESS* global variable to whatever you want. 

Depedencies for webcam:
* bridj-0.6.3-20130316.190111-13.jar
* commons-logging-1.2.jar
* dx-1.7.jar
* httpclient-4.5.2.jar
* httpcore-4.4.4.jar
* httpmime-4.5.2.jar
* mimepull-1.9.3.jar
* slf4j-api-1.7.2.jar
* webcam-capture-0.3.10.jar

### Deploying on Amazon Web Service
To deploy the Tomcat webapp, Google installing Tomcat 8, forward and redirect any ports necessary on the instance as AWS defaults to 80 and Tomcat to 8080, SSH into the instance via a terminal and SCP the war file over to the root directory.  
Move the file to wherever the webapps folder of the Tomcat 8 installation is on the server, then cd to bin of the Tomcat installation. Restart Tomcat and install the new webapp by ``$ sudo ./catalina run``.
