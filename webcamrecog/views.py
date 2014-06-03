from django.shortcuts import render

# Create your views here.

def home(request):
  return render(request, "webcamrecog/home.html")


def train(request):
	return render(request,'webcamrecog/train.html')

def save(request):
	return render(request,'webcamrecog/train.html')