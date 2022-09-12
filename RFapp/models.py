from audioop import maxpp
from django.db import models
from django.contrib.auth.models import User
import pandas as pd
import datetime
from datetime import timedelta
import string
import random

# Create your models here.

class ForecastTabla(models.Model):
    Date_Create=models.DateField(auto_now_add=True)
    usuario=models.CharField(max_length=10, null=True, blank=True)
    tipo=models.CharField(max_length=10, null=True, blank=True)
    codigo=models.CharField(max_length=7)
    Fecha=models.DateField()
    Dia=models.IntegerField()
    Mes=models.IntegerField()
    CONTACTOS_TLV=models.FloatField()
    CONTACTOS_WEB=models.FloatField()
    CONTACTOS_IMP=models.FloatField()
    BB_CATEGORIA=models.FloatField()
    DTV_PROGRAMACION=models.FloatField()
    DTV_TOH=models.FloatField()
    MACRO_IPC=models.FloatField()
    MACRO_USD=models.FloatField()
    GT_DEPOR_COPA_ARGENTINA=models.FloatField()
    GT_DEPOR_CHAMPIONS_LEAGUE=models.FloatField()
    GT_DEPOR_REAL_VS_BARZA=models.FloatField()
    GT_DEPOR_RACING_VS_INDEP=models.FloatField()
    GT_DEPOR_MUNDIAL_FUTBOL=models.FloatField()
    GT_DEPOR_ROLAND_GARROS=models.FloatField()
    GT_DEPOR_WIMBLEDON=models.FloatField()
    PRECIO_DIRECTV=models.FloatField()
    DTV_CTA=models.FloatField()
    COMP_TELECENTRO=models.FloatField()
    CBV_TOH=models.FloatField()
    CBV_DEPORTE=models.FloatField()
    TEL_GOOGLETRENDS=models.FloatField()
    Forecast_ACTIVACIONES_POS=models.FloatField()

    # def save(self, *args, **kwargs):
    #     global codigoA
    #     self.codigo=codigoA
    #     return super().save(*args, **kwargs)

    class Meta:
        ordering=['Date_Create']

    def __str__(self):
        return self.usuario

class ForecastTablaManu(models.Model):
    Date_Create=models.DateField(auto_now_add=True)
    usuario=models.CharField(max_length=10, null=True, blank=True)
    tipo=models.CharField(max_length=10)
    codigo=models.CharField(max_length=7)
    Fecha=models.CharField(max_length=15, null=True, blank=True)
    Dia=models.IntegerField()
    Mes=models.IntegerField()
    CONTACTOS_TLV=models.FloatField()
    CONTACTOS_WEB=models.FloatField()
    CONTACTOS_IMP=models.FloatField()
    BB_CATEGORIA=models.FloatField()
    DTV_PROGRAMACION=models.FloatField()
    DTV_TOH=models.FloatField()
    MACRO_IPC=models.FloatField()
    MACRO_USD=models.FloatField()
    GT_DEPOR_COPA_ARGENTINA=models.FloatField()
    GT_DEPOR_CHAMPIONS_LEAGUE=models.FloatField()
    GT_DEPOR_REAL_VS_BARZA=models.FloatField()
    GT_DEPOR_RACING_VS_INDEP=models.FloatField()
    GT_DEPOR_MUNDIAL_FUTBOL=models.FloatField()
    GT_DEPOR_ROLAND_GARROS=models.FloatField()
    GT_DEPOR_WIMBLEDON=models.FloatField()
    PRECIO_DIRECTV=models.FloatField()
    DTV_CTA=models.FloatField()
    COMP_TELECENTRO=models.FloatField()
    CBV_TOH=models.FloatField()
    CBV_DEPORTE=models.FloatField()
    TEL_GOOGLETRENDS=models.FloatField()
    Forecast_ACTIVACIONES_POS=models.FloatField()

    def save(self, *args, **kwargs):
        agno=datetime.datetime.now().year
        # global codigoM
        self.Fecha=f'{self.Dia}-{self.Mes}-{agno}'
        # self.codigo=codigoM
        return super().save(*args, **kwargs)
    
    class Meta:
        ordering=['Date_Create']

    def __str__(self):
        return self.usuario


