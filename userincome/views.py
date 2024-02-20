from locale import currency
import re
import json
from urllib import request
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Source,UserIncome 
from django.contrib import messages
from django.core.paginator import Paginator
from userpreferences.models import UserPreference
# Create your views here.


def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(
            amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)
    
    
@login_required(login_url="/Authentication/Login")
def index(request):
    sources = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get("page")
    page_obj = Paginator.get_page(paginator, page_number)
    try:
        user_preference = UserPreference.objects.get(user=request.user)
        currency = user_preference.currency
    except UserPreference.DoesNotExist: 
        currency = "USD"  
    context = {
        "income": income, 
        "page_obj": page_obj,
        'currency':currency,
    }
    
    return render(request, "income/index.html", context)


def add_income(request):
    sources = Source.objects.all()
    context = {"sources": sources, "values": request.POST}
    if request.method == "GET":
        return render(request, "income/add_income.html", context)
    if request.method == "POST":
        amount = request.POST["amount"]
        description = request.POST["description"]
        if not amount or not description:
            messages.error(request, "Amount and description are required")
            return render(request, "income/add_income.html", context)
        date = request.POST["income_date"]
        source = request.POST["source"]
        UserIncome.objects.create(
            owner=request.user,
            amount=amount,
            description=description,
            date=date,
            source=source,
        )
        messages.success(request, "Income saved successfully")
        return redirect("income")
    
    
@login_required(login_url="/Authentication/Login")
def income_edit(request, id):
    income = income.objects.get(pk=id)
    source = Source.objects.all()
    context = {
        "income": income,
        "values": income,
        "source": source,
    }
    if request.method == "GET":
        return render(request, "income/edit-income.html", context)

    if request.method == "POST":
        amount = request.POST["amount"]
        description = request.POST["description"]
        date = request.POST["income_date"]
        category = request.POST["category"]
        if not amount or not description:
            messages.error(request, "Amount or description is required")
            return render(request, "income/edit-income.html", context)

        income.owner = request.user
        income.amount = amount
        income.description = description
        income.date = date
        income.category = category
        income.save()
        messages.success(request, "income saved successfully")
        return redirect("income")


def income_delete(request, id):
    income = income.objects.get(pk=id)
    income.delete()
    messages.success(request, "Income delete successfully")
    return redirect("incomes")