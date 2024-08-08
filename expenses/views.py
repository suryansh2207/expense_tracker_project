from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import SignUpForm, ExpenseForm
from django.shortcuts import get_object_or_404
from .models import Expense
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def home(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense-list')
    else:
        form = ExpenseForm()
    
    context = {'form': form}
    return render(request, 'expenses/home.html', context)

@login_required
def expense_list(request):
    expenses = Expense.objects.all()
    context = {'expenses': expenses}
    return render(request, 'expenses/expense_list.html', context)

@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense-list')
    else:
        form = ExpenseForm(instance=expense)
    
    return render(request, 'expenses/edit_expense.html', {'form': form, 'expense': expense})

@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    
    if request.method == 'POST':
        expense.delete()
        return redirect('expense-list')
    
    return render(request, 'expenses/delete_expense.html', {'expense': expense})

@login_required
def analytics(request):
    expenses = Expense.objects.all()
    df = pd.DataFrame(list(expenses.values('date', 'category', 'amount')))

    if df.empty:
        return render(request, 'expenses/analytics.html', {'error': 'No expenses data available.'})

    # Ensure the amount column is numeric
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

    # Parse date column
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Drop rows with NaN values in critical columns
    df = df.dropna(subset=['amount', 'date'])

    # Total Expenses Per Category
    category_plot = df.groupby('category')['amount'].sum().plot(kind='bar', title='Total Expenses Per Category')
    category_fig = get_graph(category_plot)
    
    # Monthly Expenses
    monthly_plot = df.resample('M', on='date')['amount'].sum().plot(kind='line', title='Monthly Expenses')
    monthly_fig = get_graph(monthly_plot)
    
    context = {
        'category_plot': category_fig,
        'monthly_plot': monthly_fig,
    }
    
    return render(request, 'expenses/analytics.html', context)

def get_graph(plot):
    buffer = BytesIO()
    plot.figure.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode('utf-8')

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'



