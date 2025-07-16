from django.shortcuts import render
from django.http import JsonResponse
import json
import numpy as np
import joblib
import os
from django.conf import settings

# Load the pre-trained model
# Ensure the model file is in the 'tasks/models/' directory
model_path = os.path.join(settings.BASE_DIR, 'tasks', 'models', 'house_price_model.pkl')
try:
    model = joblib.load(model_path)
except FileNotFoundError:
    model = None # Handle case where model is not found

def index(request):
    if request.method == 'POST':
        if model is None:
            return JsonResponse({'error': 'Model not found.'}, status=500)

        try:
            data = json.loads(request.body)
            # The order of features must match the order the model was trained on
            features = [
                float(data['area']),
                int(data['bedrooms']),
                int(data['bathrooms']),
                int(data['stories'])
            ]
            
            # Convert to numpy array for the model
            input_data = np.array(features).reshape(1, -1)
            
            # Make prediction
            prediction = model.predict(input_data)
            price = float(prediction[0])
            
            return JsonResponse({'prediction': price})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return render(request, 'house_price/index.html')
