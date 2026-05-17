from django.shortcuts import render

# Create your views here.
def revizelerim(request):
    return render(request, 'revizelerim.html')

def revizeGuncelleme(request):
    return render(request, 'revizeGuncelle.html')
