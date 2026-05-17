from django.shortcuts import render


def kullaniciLogin(request):
    return render(request, 'login.html')

def kullaniciRegister(request):
    return render(request, 'register.html')
