from django.contrib import admin
from django.urls import path

from empresas import views
from empresas.views import (
    EmpresaListCreateAPIView, EmpresaRetrieveUpdateDestroy
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('empresa/', EmpresaListCreateAPIView.as_view(), name='listagem_empresa'),
    path('empresa/<int:pk>/', EmpresaRetrieveUpdateDestroy.as_view(), name='detalhes_empresa'),
    path('hit-no-database/', views.hit_no_database, name='hit-no-database')
]
