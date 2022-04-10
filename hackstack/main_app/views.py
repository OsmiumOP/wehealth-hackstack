from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import TestReport

# Create your views here.

import numpy as np
import pandas as pd # to make dataframes
from sklearn.model_selection import train_test_split # splitting data into test-train sections
from sklearn.tree import DecisionTreeClassifier   # the actual Decision Maker
from sklearn.preprocessing import StandardScaler    

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
            
            xd = classifier.predict([[entry.age, entry.gender, entry.height, entry.weight, entry.ap_hi, entry.ap_low, dict['glucose'], dict['cholestrol'], 0,0,0]])
            print(xd)
            return HttpResponse(404)
        except:
            return HttpResponse(404)
    else :
        return render(request, 'index.html')

def apirequesthandler(request):
    try:
        # YET TO BE CONSTRUCTED
        return HttpResponse(404)
    except:
        return HttpResponse(404)
