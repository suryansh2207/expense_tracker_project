from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('', views.CustomLoginView.as_view(), name='login'),
    path('home/', views.home, name='home'),
    path('expenses/', views.expense_list, name='expense-list'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.CustomLoginView.as_view(), name='logout'),
    path('analytics/', views.analytics, name='analytics'),  # Analytics view
    path('edit/<int:expense_id>/', views.edit_expense, name='edit-expense'),
    path('delete/<int:expense_id>/', views.delete_expense, name='delete-expense'),
    path('add/', views.home, name='add-expense'),


    
]
