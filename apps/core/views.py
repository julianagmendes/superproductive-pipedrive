from django.shortcuts import render

def signup_view(request, tenant):
    return render(request, 'core/signup.html')