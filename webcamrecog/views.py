import os
import datetime
import re
import urllib
import base64
import json
import ast
import string
import random
import cv2, sys, numpy, os

from django.template import Template
from django.template.loader import get_template
from django.template import Context
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

face_count = 1
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def home(request):
  return render(request, "webcamrecog/home.html")

def train(request):
	return render(request,'webcamrecog/train.html')

def compare(request):
	return render(request,'webcamrecog/compare.html')

@csrf_exempt
def save(request):
	face_count = 1
	resp = {'error': '0', 'message': 'All was ok'}
	image_dir = 'face_attr'
	if request.method == 'POST':
		val = ast.literal_eval(request.body)
		username = val['person']
		img = val['image']
		path = os.path.join(BASE_DIR, image_dir, username)
		if not os.path.isdir(path):
			os.mkdir(path)
		path, dirs, files = os.walk(path).next()
		face_count = len(files) + 1
		img_path = os.path.join(path,str(face_count)) +'.jpg'
		print img_path
		f = open(img_path, 'wb')
		f.write(base64.b64decode(img))
		f.close()
		convertFullImgToTrainImage(path,img_path)
		return HttpResponse(json.dumps(resp), content_type="application/json")
	else:
		return HttpResponse(json.dumps(resp), content_type="application/json")

@csrf_exempt
def recog(request):
	resp = {}
	BASE_DIR = os.path.dirname(os.path.dirname(__file__))
	image_dir = 'tmp/'
	if request.method == 'POST':
		img = request.body
		path = os.path.join(BASE_DIR, image_dir)
		if not os.path.isdir(path):
			os.mkdir(path)
		img_path = (path + id_generator() + '.jpg')
		f = open(img_path, 'wb')
		f.write(base64.b64decode(img))
		f.close()
		rects, img = detect(img_path)
		box(rects, img, img_path)
		with open(img_path, "rb") as image_file:
		    img_content = base64.b64encode(image_file.read())
		image_file.close()
		resp.update({'image': img_content })
		return HttpResponse(json.dumps(resp), content_type="application/javasript")
	else:
		return HttpResponse(json.dumps(resp), content_type="application/json")

@csrf_exempt
def detect(path):
	fn_haar = 'facerecog/static/haarcascade_frontalface_alt.xml'
	img = cv2.imread(path)
	cascade = cv2.CascadeClassifier(fn_haar)
	rects = cascade.detectMultiScale(img, 1.005, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))

	if len(rects) == 0:
		return [], img
	rects[:, 2:] += rects[:, :2]
	return rects, img

@csrf_exempt
def box(rects, img, img_path):
	for x1, y1, x2, y2 in rects:
		cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)
	cv2.imwrite(img_path, img);


