import os
import datetime
import re
import urllib
import base64
import json
import ast

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
omniUser = ''

def home(request):
  return render(request, "webcamrecog/home.html")


def train(request):
	return render(request,'webcamrecog/train.html')

@csrf_exempt
def save(request):
	global face_count
	global omniUser
	resp = {'error': '0', 'message': 'All was ok'}
	BASE_DIR = os.path.dirname(os.path.dirname(__file__))
	image_dir = 'face_attr'
	if request.method == 'POST':
		val = ast.literal_eval(request.body)
		if (face_count == 1):
			omniUser = val['person']
		username = val['person']
		if not (omniUser == username):
			face_count = 1
			omniUser = val['person']
		img = val['image']
		path = os.path.join(BASE_DIR, image_dir, username)
		if not os.path.isdir(path):
			os.mkdir(path)
		print path
		f = open(os.path.join(path,str(face_count)) +'.jpg', 'wb')
		f.write(base64.b64decode(img))
		f.close()
		face_count += 1
		return HttpResponse(json.dumps(resp), content_type="application/json")
	else:
		return HttpResponse(json.dumps(resp), content_type="application/json")


