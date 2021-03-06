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

from django.urls import path
from rest_framework.authtoken import views
from rest_framework.urlpatterns import format_suffix_patterns

from api.views import (
    AgendaAPIView,
    ConsultaAPIView,
    ConsultaDeleteApiView,
    EspecialidadeAPIView,
    MedicoAPIView,
    UsuarioView,
)

urlpatterns = [
    path("users/", UsuarioView.as_view()),
    path("login/", views.obtain_auth_token),
    path("consultas/", ConsultaAPIView.as_view(), name="consultas_post"),
    path("consultas/<int:pk>/", ConsultaDeleteApiView.as_view(), name="consultas_detalhes"),
    path("medicos/", MedicoAPIView.as_view(), name="get_medicos"),
    path("agendas/", AgendaAPIView.as_view(), name="get_agendas"),
    path("especialidades/", EspecialidadeAPIView.as_view(), name="get_especialidades"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
