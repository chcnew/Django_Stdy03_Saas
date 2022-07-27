from django.shortcuts import render


def user_login(request):
    return render(request, "informal/login.html")


def user_register(request):
    return render(request, "informal/register.html")
