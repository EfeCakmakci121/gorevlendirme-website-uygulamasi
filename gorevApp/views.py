from django.shortcuts import render

def onesignalTest(request):
    return render(request,'player.html')

def gorevlerim(request):
    return render(request, 'gorevlerim.html')

def gorevOlustur(request):
    return render(request, 'gorevolustur.html')