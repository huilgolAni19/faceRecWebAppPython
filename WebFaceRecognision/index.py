from flask import Flask, render_template, request
import json
import cv2
import numpy as np
import urllib.request as url_req
import ssl

app = Flask(__name__)


# METHOD #1: OpenCV, NumPy, and urllib
def readImageFromUrl(imgUrl):
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
	context = ssl._create_unverified_context()
	with url_req.urlopen(imgUrl, context=context) as url:
   		 s = url.read()
	image = np.asarray(bytearray(s), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	#return the image
	return image

# METHOD #2: Checks Whether the input is just string or Url 
def isUrl(string):
	if "http://" in string:
		return True
	elif "https://" in string:
		return True
	else :
		return False


# METHOD #3: Check for the Faces Presence and 
def getFaceCoordinates(faceImage):
	#load harcascade Classifier
	face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
	greay_image = cv2.cvtColor(faceImage, cv2.COLOR_BGR2GRAY)
	faceDetected = False
	faces = face_cascade.detectMultiScale(greay_image,
	scaleFactor=1.05,
	minNeighbors = 5)		
	coordinates=list()
	for x, y, w, h in faces:
		faceDetected = True
		face_coordinates = {"Start_X":x, "Start_Y": y, "End_X":(x+w), "End_Y": (y+h), "height": h, "width": w}
		coordinates.append(face_coordinates)

	result = {"FacePresence": faceDetected,
		 	"FacesCount": len(faces),
		 	"Coordinates": coordinates}
	return result

# WEB_METHOD #1: for Default url 
@app.route('/')
def home():
	return "Get request called"

# WEB_METHOD #2: Detect Faces And return face coodrinates of the face in the image..
@app.route('/faceDetect', methods=['GET','POST'])
def faceDetect():
	if request.method == 'GET':
	   return "{\"method\": \"GET\", \"response\": \"GET method called Successfully\", \"status\":\"SUCCESS\"}"
	elif request.method == 'POST':
		data = json.loads(request.data)	
		uof = isUrl(data["url"])
		if uof == True:
			img = readImageFromUrl(data["url"])
			response = getFaceCoordinates(img)
		#stringResponse = "Url: {} ImageName: {}".format(data["url"], data["image_name"])
		return str(response)

if __name__ == '__main__':
	app.run(debug = True)