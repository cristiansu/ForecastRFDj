from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(ForecastTabla)
class ForecastRFAdmin(admin.ModelAdmin):
    list_display=('usuario', 'Dia', 'Mes', 'Forecast_ACTIVACIONES_POS')
    list_filter=('Mes','usuario')


@admin.register(ForecastTablaManu)
class ForecastRFAdminManu(admin.ModelAdmin):
    list_display=('usuario', 'Dia', 'Mes', 'Forecast_ACTIVACIONES_POS')
    list_filter=('Mes','usuario')