from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import confusion_matrix 
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
import os 
from googletrans import Translator 
from django.conf import settings
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
import random

gulumseme = ["😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣"]
uzulme = ["😞", "😔", "😟", "😕", "🙁", "☹️"]
sevgi = ["😍", "🥰 ", "❤️"]

def random_enjoy():
    ind = random.randint(0, 7)
    return gulumseme[ind]
def random_sad():
    ind = random.randint(0, 5)
    return uzulme[ind]
def random_sevgi():
    ind = random.randint(0, 2)
    return sevgi[ind]



# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

@csrf_exempt
def predict(request):
    emotions = ["😶",random_sad(),random_enjoy(),random_sevgi()]
    translator = Translator() 
    message = request.POST.get('msg','')     
    
    file1 = open(os.path.join(settings.BASE_DIR, 'vectorizer.pck'),'rb')
    
    file2 = open(os.path.join(settings.BASE_DIR, 'classifier.pck'),"rb")
    
    vectorizer = pickle.load(file1)
    classifier = pickle.load(file2)

    message = translator.translate(message).text
    result = classifier.predict(vectorizer.transform([message])) 
    print(result[0])
    response = {'emoji' : emotions[result[0]]}
    return JsonResponse(response)