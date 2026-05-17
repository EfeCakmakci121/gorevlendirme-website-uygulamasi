from django.shortcuts import render

def raporlarim(request):
    return render(request, 'raporlarim.html')

def raporOlustur(request):
    return render(request, 'raporOlustur.html')

def raporGuncelle(request):
    return render(request, 'raporGuncelle.html')