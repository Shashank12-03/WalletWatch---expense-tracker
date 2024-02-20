from locale import currency
from .models import UserPreference 
from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
import json
import os

def index(request):
    exist = UserPreference.objects.filter(user=request.user).exists()
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

        for k, v in data.items():
            currency_data.append({'name': k, 'value': v})

    user_preference = None
    if exist:
        user_preference = UserPreference.objects.get(user=request.user)

    if request.method == 'GET':
        return render(request, 'preferences/index.html', {'currencies': currency_data, 'user_preferences': user_preference})
    else:
        currency = request.POST['currency']
        if exist:
            user_preference.currency = currency
            user_preference.save()
        else:
            UserPreference.objects.create(user=request.user, currency=currency)

        messages.success(request, 'Changes Saved')
        return render(request, 'preferences/index.html', {'currencies': currency_data, 'user_preferences': user_preference})
    