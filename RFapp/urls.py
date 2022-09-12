from django.urls import path
from .views import home,tabla,export_excel,simple_upload, tabla_manual, export_excel_manual,graficoA, graficoM, graficoPlotlyA, graficoPlotlyM




urlpatterns = [
    path('', home, name='generador'),
    path('manual', simple_upload, name='generador_manual'),
    path('forecast_list/', tabla, name='forecast_list'),
    path('forecast_list_manu/', tabla_manual, name='forecast_list_manu'),
    path('excel_export/', export_excel, name='excel_export'),
    path('excel_export_manual/', export_excel_manual, name='excel_export_manual'),
    path('grafica_auto/', graficoA, name='grafica_auto'),
    path('grafica_manu/', graficoM, name='grafica_manu'),
    path('grafica_plot_auto/', graficoPlotlyA, name='grafica_plot_auto'),
    path('grafica_plot_manu/', graficoPlotlyM, name='grafica_plot_manu'),

]