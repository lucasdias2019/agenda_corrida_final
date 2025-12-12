from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone # <- IMPORTAÇÃO ESSENCIAL

# O modelo User é fornecido pelo Django (RF05 - Gerenciar Conta)

class ModeloDeCorrida(models.Model):
    """
    RF01: Permite o registro de um modelo de treino reutilizável.
    """
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='modelos_corrida',
        verbose_name='Usuário'
    )
    nome = models.CharField(max_length=100, verbose_name='Nome do Modelo')
    
    # RRN01: A Distância Planejada deve ser um valor positivo e maior que zero.
    distancia_planejada_km = models.FloatField(
        validators=[MinValueValidator(0.1)],
        verbose_name='Distância Planejada (km)'
    )
    
    duracao_estimada_min = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Duração Estimada (min)'
    )
    
    objetivo = models.CharField(
        max_length=200, 
        blank=True, 
        null=True, 
        verbose_name='Objetivo do Treino'
    )

    def __str__(self):
        return f"{self.nome} - {self.distancia_planejada_km} km"

    class Meta:
        verbose_name = "Modelo de Corrida"
        verbose_name_plural = "Modelos de Corrida"


class HistoricoCorrida(models.Model):
    """
    RF04: Representa o registro de uma corrida realizada.
    """
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='historico',
        verbose_name='Usuário'
    )
    
    # RRN02: Ligado a um ModeloDeCorrida para referência.
    modelo_corrida = models.ForeignKey(
        ModeloDeCorrida,
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name='Modelo Associado'
    )
    
    # CORREÇÃO: Usamos models.DateField com default para ser editável no formulário.
    data_realizacao = models.DateField(default=timezone.now, verbose_name='Data da Realização')
    
    tempo_total_min = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='Tempo Total (minutos)'
    )
    
    observacoes = models.TextField(blank=True, verbose_name='Observações')

    def __str__(self):
        return f"Corrida de {self.usuario.username} em {self.data_realizacao}"

    class Meta:
        ordering = ['-data_realizacao']
        verbose_name = "Histórico de Corrida"
        verbose_name_plural = "Histórico de Corridas"