import os
import datetime
import re
import urllib
import base64
import json
import ast
import string
import random

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
	BASE_DIR = os.path.dirname(os.path.dirname(__file__))
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

		return HttpResponse(json.dumps(resp), content_type="application/json")
	else:
		return HttpResponse(json.dumps(resp), content_type="application/json")

@csrf_exempt
def recog(request):
	resp = {'error': '0', 'message': 'All was ok'}
	BASE_DIR = os.path.dirname(os.path.dirname(__file__))
	image_dir = 'temp/'
	if request.method == 'POST':
		img = request.body
		path = os.path.join(BASE_DIR, image_dir)
		if not os.path.isdir(path):
			os.mkdir(path)
		img_path = (path + id_generator() + '.jpg')
		f = open(img_path, 'wb')
		f.write(base64.b64decode(img))
		f.close()
		return HttpResponse(json.dumps(resp), content_type="application/json")
	else:
		return HttpResponse(json.dumps(resp), content_type="application/json")


