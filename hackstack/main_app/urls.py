import django
from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('disease-api/<int:age>/<int:gender>/<int:height>/<int:weight>/<int:ap_hi>/<int:ap_low>/<int:glucose>/<int:cholestrol>/<int:smoker>/<int:alcoholic>/<int:physicalact>/', views.apirequesthandler, name='ApiRequestHandler'),
]

