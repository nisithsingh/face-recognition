import os.path
import datetime
import re
import urllib
import base64
import json

from django.template import Template
from django.template.loader import get_template
from django.template import Context
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def home(request):
  return render(request, "webcamrecog/home.html")


def train(request):
	return render(request,'webcamrecog/train.html')

@csrf_exempt
def save(request):
	resp = {'error': '0', 'message': 'all was ok'}
	face_name = "Test"
	if request.method == 'POST':
		img = request.body
		f = open(face_name +'.jpg', 'wb')
		f.write(base64.b64decode(img))
		f.close()
		return HttpResponse(json.dumps(resp), mimetype="application/json")
	else:
		return HttpResponse(json.dumps(resp), mimetype="application/json")


