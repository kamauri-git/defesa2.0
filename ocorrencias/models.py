from django.db import models

class Ocorrencia(models.Model):
    numero = models.IntegerField()
    sigrc = models.IntegerField()
    tipo = models.CharField(max_length=100, blank=True, null=True)
    motivo = models.CharField(max_length=255)  # A coluna foi renomeada de descricao para motivo
    data = models.DateField()
    endereco = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    distrito = models.CharField(max_length=255)
    area_risco = models.IntegerField(null=True, blank=True)  # Permitir valor nulo

    def __str__(self):
        return f'Ocorrência {self.numero}'
