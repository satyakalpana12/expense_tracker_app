from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Transaction

def register_user(request):
    if request.method == 'POST':
        User.objects.create_user(request.POST['username'], password=request.POST['password'])
        return redirect('login')
    return render(request, 'tracker/register.html')

def login_user(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'tracker/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

# def dashboard(request):
#     transactions = Transaction.objects.filter(user=request.user)
#     income = sum(t.amount for t in transactions if t.type == "income")
#     expense = sum(t.amount for t in transactions if t.type == "expense")
#     balance = income - expense
#     return render(request, 'tracker/dashboard.html', {'transactions': transactions,'income': income,'expense': expense,'balance': balance})

def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user)

    income = sum(t.amount for t in transactions if t.type == "income")
    expense = sum(t.amount for t in transactions if t.type == "expense")
    balance = income - expense

    # Category-wise expense calculation
    category_data = {}
    for t in transactions:
        if t.type == "expense":
            category_data[t.category] = category_data.get(t.category, 0) + t.amount

    # ✅ Convert dict keys & values to lists for chart
    labels = list(category_data.keys())
    data = list(category_data.values())

    return render(request, 'tracker/dashboard.html', {
        'transactions': transactions,
        'income': income,
        'expense': expense,
        'balance': balance,
        'labels': labels,
        'data': data
    })

def add_transaction(request):
    if request.method == 'POST':
        Transaction.objects.create(
            user=request.user,
            amount=request.POST['amount'],
            category=request.POST['category'],
            date=request.POST['date'],
            type=request.POST['type'],
            note=request.POST['note'],
        )
        return redirect('dashboard')
    return render(request, 'tracker/add_transaction.html')
