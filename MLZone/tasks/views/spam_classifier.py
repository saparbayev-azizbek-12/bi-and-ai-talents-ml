import os
import json
import joblib
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse

model_path = os.path.join(settings.BASE_DIR, 'models', 'spam_classifier', 'spam_classifier_model.joblib')
vectorizer_path = os.path.join(settings.BASE_DIR, 'models', 'spam_classifier', 'count_vectorizer.joblib')
try:
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
except FileNotFoundError:
    model = None
    vectorizer = None

def index(request):
    context = {}
    if request.method == 'POST':
        if model is None or vectorizer is None:
            # This case should ideally be handled more gracefully
            # For now, just re-render with an error message in context if needed
            context['error'] = 'Model not loaded. Please contact an administrator.'
            return render(request, 'spam_classifier/index.html', context)

        message = request.POST.get('message', '')
        context['user_input'] = message

        if message:
            try:
                message_vector = vectorizer.transform([message])
                prediction_result = model.predict(message_vector)
                
                # Assuming 1 is Spam and 0 is Not Spam
                is_spam = prediction_result[0]
                context['prediction'] = 'Spam' if is_spam == 1 else 'Not Spam'

            except Exception as e:
                # Handle potential errors during prediction
                context['error'] = f"An error occurred: {str(e)}"

    return render(request, 'spam_classifier/index.html', context)