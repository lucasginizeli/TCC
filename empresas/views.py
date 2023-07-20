from rest_framework import generics

from empresas.models import Empresa
from empresas.serializers import EmpresaSerializer
from django.http import JsonResponse


# Create your views here.
class EmpresaListCreateAPIView(generics.ListCreateAPIView):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer


class EmpresaRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer


def hit_no_database(request):
    return JsonResponse({"No database": "ok"})
