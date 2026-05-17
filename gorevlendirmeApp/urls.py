"""
URL configuration for gorevlendirmeApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
from django.contrib import admin
from django.urls import path,include,re_path
from gorevApp.views import onesignalTest
from strawberry.django.views import GraphQLView
from .schemas.mutation import schema
from django.views.static import serve
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path("graphql/", GraphQLView.as_view(schema=schema,graphiql=True)),
    path('gorev/', include('gorevApp.urls')),
    path('giris/', include('userApp.urls')),
    path('revize/', include('revizeApp.urls')),
    path('rapor/', include('raporApp.urls')),
    re_path(r'^OneSignalSDKWorker.js$', serve, {
    'document_root': BASE_DIR,
    'path': 'OneSignalSDKWorker.js',
    }),
]
