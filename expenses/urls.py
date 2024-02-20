from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',views.home_page,name="home"),
    path('expenses',views.index,name="expenses"),
    path('add_expenses',views.add_expenses,name='add_expenses'),
    path('edit-expense/<int:id>',views.expense_edit,name='expense-edit'),
    path('expense-delete/<int:id>',views.expense_delete,name='expense_delete'),
    path('search-expenses', csrf_exempt(views.search_expenses),name="search_expenses"),
    path('expense_category_summary',views.expense_category_summary,name='expense_category_summary'),
    path('expense_month_summary', views.expense_month_summary, name='expense_month_summary'),
    path('category_per_month_summary',views.category_per_month_summary,name='category_per_month_summary'),
    path('stats1',views.stats1_view,name='stats1'),
    path('stats2',views.stats2_view,name='stats2'),
    path('stats3',views.stats3_view,name='stats3'),
    path('export-csv',views.export_csv,name='export-csv'),
    path('export-excel',views.export_excel,name='export-excel')
]
