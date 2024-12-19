from django.urls import path
from . import views

app_name = 'basepage'

urlpatterns = [
    path('', views.home, name='home')
]
