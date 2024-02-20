from locale import currency
import re
import json
from urllib import request
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from userincome.models import UserIncome
import expenses
from userincome.models import UserIncome
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from userpreferences.models import UserPreference
import datetime
import xlwt
import csv
# Create your views here.
def home_page(request):
    if request.user.is_authenticated:
        #today's expense block start
        today=datetime.date.today()    
        total_expense=Expense.objects.filter(owner=request.user)
        today_expense=total_expense.filter(date__gte=today,date__lte=today)
        todays_expense=0
        for item in today_expense:
            todays_expense+=item.amount

        #today's expense block end
        
        #balance remain this month start
        month=datetime.date.today().month
        income_month = UserIncome.objects.filter(owner=request.user,date__month=month)
        expense_this_month=total_expense.filter(date__month=month)
        this_month_expense=0
        this_month_expense=sum([item.amount for item in expense_this_month])
        income_this_month = sum([income.amount for income in income_month])
        if income_this_month > 0:
            balance = income_this_month -this_month_expense 
        else:
            balance = 0
        #balance remain this month end
        
        data={'todays_expense':todays_expense,'this_month_expense':this_month_expense,'balance':balance}
        return render(request,'index.html',data)
    else:
        return render(request,'index.html')


@login_required(login_url="/Authentication/Login")
def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url="/Authentication/Login")
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get("page")
    page_obj = Paginator.get_page(paginator, page_number)

    try:
        user_preference = UserPreference.objects.get(user=request.user)
        currency = user_preference.currency
    except UserPreference.DoesNotExist:
        # Handle the case where UserPreference does not exist for the current user
        # You can set a default currency or handle it based on your requirements
        currency = "USD"  # Replace with your default currency or appropriate handling

    context = {
        "expenses": expenses, 
        "page_obj": page_obj,
        'currency': currency,
    }

    return render(request, "expense/index.html", context)


def add_expenses(request):
    categories = Category.objects.all()
    context = {"categories": categories, "values": request.POST}
    if request.method == "GET":
        return render(request, "expense/add_expenses.html", context)
    if request.method == "POST":
        amount = request.POST["amount"]
        description = request.POST["description"]
        if not amount or not description:
            messages.error(request, "Amount and description are required")
            return render(request, "expense/add_expenses.html", context)
        date = request.POST["expense_date"]
        category = request.POST["category"]
        Expense.objects.create(
            owner=request.user,
            amount=amount,
            description=description,
            date=date,
            category=category,
        )
        messages.success(request, "Expense saved successfully")
        return redirect("expenses")

@login_required(login_url="/Authentication/Login")
def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        "expense": expense,
        "values": expense,
        "categories": categories,
    }
    if request.method == "GET":
        return render(request, "expense/edit-expense.html", context)

    if request.method == "POST":
        amount = request.POST["amount"]
        description = request.POST["description"]
        date = request.POST["expense_date"]
        category = request.POST["category"]
        if not amount or not description:
            messages.error(request, "Amount or description is required")
            return render(request, "expense/edit-expense.html", context)

        expense.owner = request.user
        expense.amount = amount
        expense.description = description
        expense.date = date
        expense.category = category
        expense.save()
        messages.success(request, "Expense saved successfully")
        return redirect("expenses")


def expense_delete(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, "Expense delete successfully")
    return redirect("expenses")


# def expense_category_summary(request):
#     today=datetime.date.today()
#     six_month_ago=today-datetime.timedelta(days=30*6)
#     expenses=Expense.objects.filter(owner=request.user,date__gte=six_month_ago,date__lte=today)
#     finalrep={}
#     def get_category(expense):
#         return expense.category
#     category_list=list(set(map(get_category,expenses)))
    
    
#     def get_expense_category_amount(category):
#         amount=0
#         filtered_by_category=expenses.filter(category=category)
#         for item in filtered_by_category:
#             amount+=item.amount
#         return amount
    
#     for x in expenses:
#         for y in category_list:
#             finalrep[y]=get_expense_category_amount(y)
            
#     return JsonResponse({'expense_category_data':finalrep},safe=False)

#Expense/category
def calculate_expense_category_data(expenses):
    finalrep={}
    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)
        for item in filtered_by_category:
            amount += item.amount
        return amount

    for category in set(expenses.values_list('category', flat=True)):
        finalrep[category] = get_expense_category_amount(category)

    return finalrep


def expense_category_summary(request):
    today = datetime.date.today()
    six_month_ago = today - datetime.timedelta(days=30 * 6)
    expenses = Expense.objects.filter(owner=request.user, date__gte=six_month_ago, date__lte=today)
    finalrep= calculate_expense_category_data(expenses)
    
    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def stats1_view(request):
    today = datetime.date.today()
    six_month_ago = today - datetime.timedelta(days=30 * 6)
    amount=0
    expenses=Expense.objects.filter(owner=request.user,date__gte=six_month_ago, date__lte=today)
    finalrep=calculate_expense_category_data(expenses)
    for expense in expenses:
        amount+=expense.amount
    return render(request,'expense/stats1.html',{'amount':amount,'expense_category_data': finalrep})


#Expense/Month of year
def calculate_expense_month_summary(expenses):
    final_report = {}

    def get_monthly_expense_amount():
        for month in range(1, 13):
            amount = 0
            filtered_by_month = expenses.filter(date__month=month)
            for item in filtered_by_month:
                amount += item.amount
            final_report[month] =amount
            
    get_monthly_expense_amount()
    return final_report


def stats2_view(request):
    monthly_expenses = {}
    yr=0
    if request.method == 'POST':
        year=request.POST['select_year']
        request.session['select_year'] = year 
        print(year)
        if year:
            expenses = Expense.objects.filter(owner=request.user, date__year=year)
            monthly_expenses = calculate_expense_month_summary(expenses)
            yr=year 
            return render(request, 'expense/stats2.html', {'expense_month_data': monthly_expenses,'yr':yr})
    return render(request, 'expense/stats2.html', {'expense_month_data': monthly_expenses,'yr':yr})

def expense_month_summary(request):
    select_year = request.session.get('select_year')
    expenses=Expense.objects.filter(owner=request.user,date__year=select_year)
    monthly_expenses = calculate_expense_month_summary(expenses) 
    return JsonResponse({'expense_month_data': monthly_expenses}, safe=False) 


#category/month
def category_per_month(expenses):
    overall_month={}#this will contain month and another dictionary with category and its expense
    def get_expense_category_amount(expense_by_month,category):
        amount = 0
        filtered_by_category = expense_by_month.filter(category=category)
        for item in filtered_by_category:
            amount += item.amount
        return amount
    
    for month in range(1,13):
        category_over_month={}
        filter_category_by_month=expenses.filter(date__month=month)
        for category in set(filter_category_by_month.values_list('category', flat=True)):
            print(category)
            category_over_month[category]=get_expense_category_amount(filter_category_by_month,category)
        overall_month[month]=category_over_month
    #print(overall_month)
    return overall_month

def stats3_view(request):
    category_month={}
    yr=0
    if request.method=='POST':
        year=request.POST['select_year']
        request.session['select_year']=year
        print(year)
        if year:
            expenses=Expense.objects.filter(owner=request.user,date__year=year)
            category_month=category_per_month(expenses)
            yr=year
            return render(request,'expense/stats3.html',{'category_month':category_month,'yr':yr})
    return render(request,'expense/stats3.html',{'category_month':category_month,'yr':yr})

def category_per_month_summary(request):
    selected_year = request.session.get('select_year')
    expenses=Expense.objects.filter(owner=request.user,date__year=selected_year)
    category_month=category_per_month(expenses)
    print(category_month)
    return JsonResponse({'category_month_summary':category_month},safe=False)


#export the expense
def export_csv(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=Expenses'+ datetime.datetime.now().strftime("%Y-%m-%d") +'.csv'
    
    writer= csv.writer(response)
    writer.writerow(['Amount','Description','Category','Date'])
    expenses=Expense.objects.filter(owner=request.user)
    
    for expense in expenses:
        writer.writerow([expense.amount, expense.description,expense.category,expense.date])
    
    return response


def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + datetime.datetime.now().strftime("%Y-%m-%d") + '.xls'
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    
    columns = ['Amount', 'Description', 'Category', 'Date']
    
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    
    font_style = xlwt.XFStyle()
    
    rows = Expense.objects.filter(owner=request.user).values_list('amount', 'description', 'category', 'date')
    
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    
    wb.save(response)
    return response