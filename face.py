from time import time
import base64
import requests
import cv2
import numpy as np
import os
import json

time_prev = time()
change = 0

video_capture = cv2.VideoCapture(0)

subscription_key = 'c155c1d6247145a08c5d987762889567'
assert subscription_key

face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect/'

headers = { 
	'Content-Type': 'application/octet-stream',
	'Ocp-Apim-Subscription-Key': subscription_key }
    
params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'emotion',
}


while(True):
	ret, frame = video_capture.read()
	time_now = time()
	change += time_now - time_prev
	time_prev = time_now

	cv2.imshow('images/frame.png',frame)
	if change > 5:
		cv2.imwrite('images/frame.png', frame)
	
		fileDir = os.path.dirname(os.path.realpath('__file__'))
		filename = os.path.join(fileDir, 'images/frame.png')

		data = open(filename, 'rb').read()

		with open(filename, "rb") as imageFile:
			imageString = base64.b64encode(imageFile.read())

		response = requests.post(face_api_url, params=params, headers=headers, data=data)
		responseText = (json.loads(response.text))[0]['faceAttributes']['emotion']
		print(responseText)
		max = 0.0
		maxEmotion = "neutral"
		for emotion in responseText:
			if responseText[emotion] > max:
				max = responseText[emotion]
				maxEmotion = emotion
		print(maxEmotion)
		change = 0
		
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break




