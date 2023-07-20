from django.db import models


class Empresa(models.Model):
    cnpj = models.CharField(max_length=20)
    nome = models.CharField(max_length=255)
    capital_social = models.FloatField()
