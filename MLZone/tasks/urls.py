from django.urls import path
from .views import house_price, digit_recognition, spam_classifier

app_name = 'tasks'

urlpatterns = [
    path('house-price/', house_price.index, name='house_price'),
    path('digit-recognition/', digit_recognition.index, name='digit_recognition'),
    path('spam-classifier/', spam_classifier.index, name='spam_classifier'),
]
