from unittest import result
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import TestReport

# Create your views here.

import numpy as np
import pandas as pd # to make dataframes
from sklearn.model_selection import train_test_split # splitting data into test-train sections
from sklearn.tree import DecisionTreeClassifier   # the actual Decision Maker
from sklearn.preprocessing import StandardScaler    
from sklearn import metrics # to calculate Accuracy of the Model

df = pd.read_csv('main_app/csvfiles/cardio_train.csv', sep=';') # importing dataset to a dataframe
df = df.drop('id', axis=1)
df['age'] = df['age'] / 365.25

X = df.drop(columns=['cardio'],axis=1)
Y = df['cardio']
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size = .15, random_state=42)

st_x= StandardScaler()  
x_train= st_x.fit_transform(x_train)    
x_test= st_x.transform(x_test)    

classifier= DecisionTreeClassifier(criterion='entropy', random_state=0)  
classifier.fit(x_train, y_train)  
acc = metrics.accuracy_score(y_test, classifier.predict(x_test))

def home(request):
    if request.GET :
        dict = request.GET
        try:
            entry = TestReport()
            entry.name = dict['name']
            entry.email = dict['email']
            entry.phone_num = dict['phone']
            entry.age = dict['age']
            entry.gender = dict['gender']
            entry.height = dict['height']
            entry.weight = dict['weight']
            entry.ap_hi = dict['ap_hi']
            entry.ap_low = dict['ap_low']
            entry.save()
            
            result = classifier.predict([[entry.age, entry.gender, entry.height, entry.weight, entry.ap_hi, entry.ap_low, dict['glucose'], dict['cholestrol'], 0,0,0]])

            testEntries = TestReport.objects.filter(phone_num=dict['phone'])

            context = {
                'cardio' : result[0],
                'entries' : testEntries
            }

            return render(request, 'table.html', context)
        except:
            return HttpResponse(404)
    else :
        return render(request, 'index.html')

def apirequesthandler(request, age, gender,height, weight, ap_hi, ap_low, glucose, cholestrol, smoker, alcoholic, physicalact):
    try:
        result = classifier.predict([[age, gender, height, weight, ap_hi, ap_low, glucose, cholestrol, smoker, alcoholic, physicalact]])
        context = {
            'result' : int(result[0]),
            'accuracy': round(float(acc) * 100, 2)
        }
        return JsonResponse(context)
    except: 
        return HttpResponse(404)
