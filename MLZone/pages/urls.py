from django.urls import path
from .views import home

app_name = 'pages'

urlpatterns = [
    path('', home.index, name='home'),
]
