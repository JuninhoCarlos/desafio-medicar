"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from api.views import AgendaAPIView, ConsultaAPIView, EspecialidadeAPIView, MedicoAPIView
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/login", views.obtain_auth_token),
    path("api/v1/consultas/", ConsultaAPIView.as_view()),
    path("api/v1/medicos", MedicoAPIView.as_view()),
    path("api/v1/agendas", AgendaAPIView.as_view()),
    path("api/v1/especialidades", EspecialidadeAPIView.as_view()),
]
