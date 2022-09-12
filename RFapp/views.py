from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
import datetime
from datetime import timedelta
from .funcionesRF import *
from .recursos import ManualResource
from RFapp.models import ForecastTabla, ForecastTablaManu
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
import xlwt
from django.db.models import Q
from tablib import Dataset
import string
import random
import time
import plotly.graph_objects as go
from django.contrib.auth.decorators import login_required
# funcion crea código

def codigo(n):
    number_of_strings = n
    length_of_string = 7
    return (''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length_of_string)))


#generador de forecast automático
login_required(login_url='/')
def home(request):

    if request.method == 'POST':
        try:
            n = int(request.POST.get('peridodo'))
            current_user=get_object_or_404(User, pk=request.user.pk)
            cod_a=codigo(1)
            hoy=datetime.datetime.now()
            if (n!='') and (n>0) and (n<=180):
                data=forecast_result(n)
                for i in range(n):
                    ForecastTabla.objects.create(
                        usuario=current_user,
                        tipo='Auto',
                        codigo=cod_a,
                        Fecha=(hoy+datetime.timedelta(i)).strftime("%Y-%m-%d"),
                        Dia=data['Dia'][i], 
                        Mes=data['Mes'][i],
                        CONTACTOS_TLV=data['CONTACTOS_TLV'][i],
                        CONTACTOS_WEB=data['CONTACTOS_WEB'][i],
                        CONTACTOS_IMP=data['CONTACTOS_IMP'][i],
                        BB_CATEGORIA=data['BB_CATEGORIA'][i],
                        DTV_PROGRAMACION=data['DTV_PROGRAMACION'][i],
                        DTV_TOH=data['DTV_TOH'][i],
                        MACRO_IPC=data['MACRO_IPC'][i],
                        MACRO_USD=data['MACRO_USD'][i],
                        GT_DEPOR_COPA_ARGENTINA=data['GT_DEPOR_COPA_ARGENTINA'][i],
                        GT_DEPOR_CHAMPIONS_LEAGUE=data['GT_DEPOR_CHAMPIONS_LEAGUE'][i],
                        GT_DEPOR_REAL_VS_BARZA=data['GT_DEPOR_REAL_VS_BARZA'][i],
                        GT_DEPOR_RACING_VS_INDEP=data['GT_DEPOR_RACING_VS_INDEP'][i],
                        GT_DEPOR_MUNDIAL_FUTBOL=data['GT_DEPOR_MUNDIAL_FUTBOL'][i],
                        GT_DEPOR_ROLAND_GARROS=data['GT_DEPOR_ROLAND_GARROS'][i],
                        GT_DEPOR_WIMBLEDON=data['GT_DEPOR_WIMBLEDON'][i],
                        PRECIO_DIRECTV=data['PRECIO_DIRECTV'][i],
                        DTV_CTA=data['DTV__CTA'][i],
                        COMP_TELECENTRO=data['COMP_TELECENTRO'][i],
                        CBV_TOH=data['CBV_TOH'][i],
                        CBV_DEPORTE=data['CBV_DEPORTE'][i],
                        TEL_GOOGLETRENDS=data['TEL_GOOGLETRENDS'][i],
                        Forecast_ACTIVACIONES_POS=data['Forecast_ACTIVACIONES_POS'][i]
                        )
                messages.success(request, 'Forecast generado Ok')
                return redirect('forecast_list')
            context={'title':'Generador-Forecast-Auto'}
            messages.success(request, 'Error. Debe ingresar sólo números entre 1 y 180')
            return render(request, 'generador.html', context)
        except ValueError:
            messages.error(request, 'Error. Debe ingresar un número entre 1 y 180')
            context={'title':'Generador-Forecast-Auto', 'mensajeError':'Debe ingresar valor numérico entre 1 y 180'}
            return render(request, 'generador.html', context)
    else:
        context={'title':'Generador-Forecast-Auto'}
        return render(request, 'generador.html', context)

#tabla lista de forecast automáticos realizados 
login_required(login_url='/')       
def tabla(request):
    datosxuser=ForecastTabla.objects.filter(usuario=request.user)
    
    if request.user.is_superuser:
        datos=ForecastTabla.objects.all()

        context={
            'title':'Forecast',
            'datos':datos
        }
        return render(request, 'forecast_list.html', context)

    else:
        datos=ForecastTabla.objects.filter(usuario=request.user)

        context={
            'title':'Forecast',
            'datos':datos
        }
        return render(request, 'forecast_list.html', context)

#exporta a excel forecast realizados en el día
login_required(login_url='/')
def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Forecast_ACTIVACIONES_POS'+str(datetime.datetime.now())+'.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Forecast_ACTIVACIONES_POS')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold=True

    columns = ['Fecha_Create','Usuario', 'Codigo','Fecha','Dia', 'Mes', 'CONTACTOS_TLV', 'CONTACTOS_WEB', 'CONTACTOS_IMP','BB_CATEGORIA','DTV_PROGRAMACION','DTV_TOH','MACRO_IPC','MACRO_USD','GT_DEPOR_COPA_ARGENTINA','GT_DEPOR_CHAMPIONS_LEAGUE','GT_DEPOR_REAL_VS_BARZA','GT_DEPOR_RACING_VS_INDEP','GT_DEPOR_MUNDIAL_FUTBOL','GT_DEPOR_ROLAND_GARROS','GT_DEPOR_WIMBLEDON','PRECIO_DIRECTV','DTV_CTA','COMP_TELECENTRO','CBV_TOH','CBV_DEPORTE','TEL_GOOGLETRENDS','Forecast_ACTIVACIONES_POS']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    hoy=datetime.datetime.now()
    criterio1=Q(usuario=request.user)
    #criterio2=Q(Date_Create=hoy.strftime("%Y-%m-%d"))
    fecha=ForecastTabla.objects.all().order_by('-Date_Create').first()
    criterio2=Q(Date_Create=fecha.Date_Create)
    rows = ForecastTabla.objects.filter(criterio1 & criterio2).values_list('Date_Create','usuario', 'codigo','Fecha','Dia', 'Mes', 'CONTACTOS_TLV', 'CONTACTOS_WEB', 'CONTACTOS_IMP','BB_CATEGORIA','DTV_PROGRAMACION','DTV_TOH','MACRO_IPC','MACRO_USD','GT_DEPOR_COPA_ARGENTINA','GT_DEPOR_CHAMPIONS_LEAGUE','GT_DEPOR_REAL_VS_BARZA','GT_DEPOR_RACING_VS_INDEP','GT_DEPOR_MUNDIAL_FUTBOL','GT_DEPOR_ROLAND_GARROS','GT_DEPOR_WIMBLEDON','PRECIO_DIRECTV','DTV_CTA','COMP_TELECENTRO','CBV_TOH','CBV_DEPORTE','TEL_GOOGLETRENDS','Forecast_ACTIVACIONES_POS')

    for row in rows:
        row_num +=1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response

#exporta a excel forecast manual realizados en el día
login_required(login_url='/')
def export_excel_manual(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Forecast_ACTIVACIONES_POS'+str(datetime.datetime.now())+'.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Forecast_ACTIVACIONES_POS')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold=True

    columns = ['Fecha_Create','Usuario', 'Codigo','Fecha','Dia', 'Mes', 'CONTACTOS_TLV', 'CONTACTOS_WEB', 'CONTACTOS_IMP','BB_CATEGORIA','DTV_PROGRAMACION','DTV_TOH','MACRO_IPC','MACRO_USD','GT_DEPOR_COPA_ARGENTINA','GT_DEPOR_CHAMPIONS_LEAGUE','GT_DEPOR_REAL_VS_BARZA','GT_DEPOR_RACING_VS_INDEP','GT_DEPOR_MUNDIAL_FUTBOL','GT_DEPOR_ROLAND_GARROS','GT_DEPOR_WIMBLEDON','PRECIO_DIRECTV','DTV_CTA','COMP_TELECENTRO','CBV_TOH','CBV_DEPORTE','TEL_GOOGLETRENDS','Forecast_ACTIVACIONES_POS']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    hoy=datetime.datetime.now()
    criterio1=Q(usuario=request.user)
    #criterio2=Q(Date_Create=hoy.strftime("%Y-%m-%d"))
    fecha=ForecastTabla.objects.all().order_by('-Date_Create').first()
    criterio2=Q(Date_Create=fecha.Date_Create)
    rows = ForecastTablaManu.objects.filter(criterio1 & criterio2).values_list('Date_Create','usuario', 'codigo','Fecha','Dia', 'Mes', 'CONTACTOS_TLV', 'CONTACTOS_WEB', 'CONTACTOS_IMP','BB_CATEGORIA','DTV_PROGRAMACION','DTV_TOH','MACRO_IPC','MACRO_USD','GT_DEPOR_COPA_ARGENTINA','GT_DEPOR_CHAMPIONS_LEAGUE','GT_DEPOR_REAL_VS_BARZA','GT_DEPOR_RACING_VS_INDEP','GT_DEPOR_MUNDIAL_FUTBOL','GT_DEPOR_ROLAND_GARROS','GT_DEPOR_WIMBLEDON','PRECIO_DIRECTV','DTV_CTA','COMP_TELECENTRO','CBV_TOH','CBV_DEPORTE','TEL_GOOGLETRENDS','Forecast_ACTIVACIONES_POS')

    for row in rows:
        row_num +=1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response

#función genera forecast manual en base al modelo ML importado
login_required(login_url='/')
def forecast_result_Manu(n, df_train):
    ruta=os.path.join(BASE_DIR,'RFapp/modeloML','ml_RF_model.joblib')
    model_ml=joblib.load(ruta)
    y_pred=model_ml.predict(df_train)
    df_pred=pd.DataFrame({'Forecast_ACTIVACIONES_POS':y_pred})
    df_result=pd.concat([df_train,df_pred], axis=1)
    return df_result

#generador de forecast manual
login_required(login_url='/')
def simple_upload(request):
        if request.method == 'POST':
            try:
                if request.FILES:
                    current_user=get_object_or_404(User, pk=request.user.pk)
                    cod_m=codigo(1)
                    archivo_resource = ManualResource()
                    dataset = Dataset()
                    new_archivo = request.FILES['myfile']
                    
                    if '.xlsx' in str(new_archivo):
                    
                        try: 
                            imported_data = dataset.load(new_archivo.read(),format='xlsx')  
                            n=len(imported_data)
                            Dia=[]
                            Mes=[]
                            CONTACTOS_TLV=[]
                            CONTACTOS_WEB=[]
                            CONTACTOS_IMP=[]
                            BB_CATEGORIA=[]
                            DTV_PROGRAMACION=[]
                            DTV_TOH=[]
                            MACRO_IPC=[]
                            MACRO_USD=[]
                            GT_DEPOR_COPA_ARGENTINA=[]
                            GT_DEPOR_CHAMPIONS_LEAGUE=[]
                            GT_DEPOR_REAL_VS_BARZA=[]
                            GT_DEPOR_RACING_VS_INDEP=[]
                            GT_DEPOR_MUNDIAL_FUTBOL=[]
                            GT_DEPOR_ROLAND_GARROS=[]
                            GT_DEPOR_WIMBLEDON=[]
                            PRECIO_DIRECTV=[]
                            DTV__CTA=[]
                            COMP_TELECENTRO=[]
                            CBV_TOH=[]
                            CBV_DEPORTE=[]
                            TEL_GOOGLETRENDS=[]
                            for d in imported_data:
                                Dia.append(d[0])
                                Mes.append(d[1])
                                CONTACTOS_TLV.append(d[2])
                                CONTACTOS_WEB.append(d[3])
                                CONTACTOS_IMP.append(d[4])
                                BB_CATEGORIA.append(d[5])
                                DTV_PROGRAMACION.append(d[6])
                                DTV_TOH.append(d[7])
                                MACRO_IPC.append(d[8])
                                MACRO_USD.append(d[9])
                                GT_DEPOR_COPA_ARGENTINA.append(d[10])
                                GT_DEPOR_CHAMPIONS_LEAGUE.append(d[11])
                                GT_DEPOR_REAL_VS_BARZA.append(d[12])
                                GT_DEPOR_RACING_VS_INDEP.append(d[13])
                                GT_DEPOR_MUNDIAL_FUTBOL.append(d[14])
                                GT_DEPOR_ROLAND_GARROS.append(d[15])
                                GT_DEPOR_WIMBLEDON.append(d[16])
                                PRECIO_DIRECTV.append(d[17])
                                DTV__CTA.append(d[18])
                                COMP_TELECENTRO.append(d[19])
                                CBV_TOH.append(d[20])
                                CBV_DEPORTE.append(d[21])
                                TEL_GOOGLETRENDS.append(d[22])

                            df_import=pd.DataFrame({
                                'Dia':Dia,
                                'Mes':Mes,
                                'CONTACTOS_TLV':CONTACTOS_TLV,
                                'CONTACTOS_WEB':CONTACTOS_WEB,
                                'CONTACTOS_IMP':CONTACTOS_IMP,
                                'BB_CATEGORIA':BB_CATEGORIA,
                                'DTV_PROGRAMACION':DTV_PROGRAMACION,
                                'DTV_TOH':DTV_TOH,
                                'MACRO_IPC':MACRO_IPC,
                                'MACRO_USD':MACRO_USD,
                                'GT_DEPOR_COPA_ARGENTINA':GT_DEPOR_COPA_ARGENTINA,
                                'GT_DEPOR_CHAMPIONS_LEAGUE':GT_DEPOR_CHAMPIONS_LEAGUE,
                                'GT_DEPOR_REAL_VS_BARZA':GT_DEPOR_REAL_VS_BARZA,
                                'GT_DEPOR_RACING_VS_INDEP':GT_DEPOR_RACING_VS_INDEP,
                                'GT_DEPOR_MUNDIAL_FUTBOL':GT_DEPOR_MUNDIAL_FUTBOL,
                                'GT_DEPOR_ROLAND_GARROS':GT_DEPOR_ROLAND_GARROS,
                                'GT_DEPOR_WIMBLEDON':GT_DEPOR_WIMBLEDON,
                                'PRECIO_DIRECTV':PRECIO_DIRECTV,
                                'DTV__CTA':DTV__CTA,
                                'COMP_TELECENTRO':COMP_TELECENTRO,
                                'CBV_TOH':CBV_TOH,
                                'CBV_DEPORTE':CBV_DEPORTE,
                                'TEL_GOOGLETRENDS':TEL_GOOGLETRENDS
                            })
                            data=forecast_result_Manu(n,df_import)
                            for i in range(n):
                                ForecastTablaManu.objects.create(
                                    usuario=current_user,
                                    tipo='Manu',
                                    codigo=cod_m,
                                    Dia=data['Dia'][i], 
                                    Mes=data['Mes'][i],
                                    CONTACTOS_TLV=data['CONTACTOS_TLV'][i],
                                    CONTACTOS_WEB=data['CONTACTOS_WEB'][i],
                                    CONTACTOS_IMP=data['CONTACTOS_IMP'][i],
                                    BB_CATEGORIA=data['BB_CATEGORIA'][i],
                                    DTV_PROGRAMACION=data['DTV_PROGRAMACION'][i],
                                    DTV_TOH=data['DTV_TOH'][i],
                                    MACRO_IPC=data['MACRO_IPC'][i],
                                    MACRO_USD=data['MACRO_USD'][i],
                                    GT_DEPOR_COPA_ARGENTINA=data['GT_DEPOR_COPA_ARGENTINA'][i],
                                    GT_DEPOR_CHAMPIONS_LEAGUE=data['GT_DEPOR_CHAMPIONS_LEAGUE'][i],
                                    GT_DEPOR_REAL_VS_BARZA=data['GT_DEPOR_REAL_VS_BARZA'][i],
                                    GT_DEPOR_RACING_VS_INDEP=data['GT_DEPOR_RACING_VS_INDEP'][i],
                                    GT_DEPOR_MUNDIAL_FUTBOL=data['GT_DEPOR_MUNDIAL_FUTBOL'][i],
                                    GT_DEPOR_ROLAND_GARROS=data['GT_DEPOR_ROLAND_GARROS'][i],
                                    GT_DEPOR_WIMBLEDON=data['GT_DEPOR_WIMBLEDON'][i],
                                    PRECIO_DIRECTV=data['PRECIO_DIRECTV'][i],
                                    DTV_CTA=data['DTV__CTA'][i],
                                    COMP_TELECENTRO=data['COMP_TELECENTRO'][i],
                                    CBV_TOH=data['CBV_TOH'][i],
                                    CBV_DEPORTE=data['CBV_DEPORTE'][i],
                                    TEL_GOOGLETRENDS=data['TEL_GOOGLETRENDS'][i],
                                    Forecast_ACTIVACIONES_POS=data['Forecast_ACTIVACIONES_POS'][i]                    
                                    ) 
                            messages.success(request, 'Forecast generado Ok') 
                            return redirect('forecast_list_manu')
                        except ValueError:
                            messages.warning(request, 'Archivo no cumple formato') 
                            context={'title':'Generador-Forecast-Manual'} 
                            return render(request, 'generador_manu.html', context)
                    messages.warning(request, 'Archivo no cumple formato, debe ser Excel xlsx') 
                    context={'title':'Generador-Forecast-Manual'} 
                    return render(request, 'generador_manu.html', context)
                messages.warning(request, 'No ha subido archivo')
                context={'title':'Generador-Forecast-Manual'} 
                return render(request, 'generador_manu.html', context)

            except ValueError:
                messages.warning(request, 'Error. Archivo no cumple formato')
                context={'title':'Generador-Forecast-Manual'} 
                return render(request, 'generador_manu.html', context)
        
        context={'title':'Generador-Forecast-Manual', 'mensaje':'Error formato'} 
        return render(request, 'generador_manu.html', context)
    
#tabla con lista de forecast manual generados
login_required(login_url='/')
def tabla_manual(request):
    datosxuser=ForecastTablaManu.objects.filter(usuario=request.user)
    
    if request.user.is_superuser:
        datos=ForecastTablaManu.objects.all()

        context={
            'title':'Forecast-Manual',
            'datos':datos
        }
        return render(request, 'forecast_list_manu.html', context)

    else:
        datos=ForecastTablaManu.objects.filter(usuario=request.user)

        context={
            'title':'Forecast-Manual',
            'datos':datos
        }
        return render(request, 'forecast_list_manu.html', context)


#gráfica de forecast automático
def graficoA(request):
    dataIni=ForecastTabla.objects.all().filter(usuario=request.user)
    if dataIni:
        try:
            criterio1=Q(usuario=request.user)
            cod=ForecastTabla.objects.all().filter(criterio1).order_by('-id').first()
            codi=cod.codigo
            print(codi)
            criterio2=Q(codigo=codi)
            data=ForecastTabla.objects.filter(criterio2)
            
            fechas=[]
            for f in data:
                fech=f.Fecha
                fechas.append(fech.strftime("%Y-%m-%d"))

            valores=[]
            for v in data:
                valores.append(v.Forecast_ACTIVACIONES_POS)

            context={
                'fechas':fechas[:180],
                'valores':valores[:180],
            }

            return render(request, 'grafico_auto.html', context)
        
        except ValueError:
            messages.warning(request, 'Hubo un error')
            context={'mensaje': 'Error'}
            return render(request, 'grafico_auto.html', context)

    messages.warning(request, 'Error. No hay datos') 
    context={'mensaje': 'Error'}
    return render(request, 'grafico_auto.html', context)     


#gráfica de forecast manual
def graficoM(request):
    dataIni=ForecastTablaManu.objects.all().filter(usuario=request.user)
    if dataIni:
        try:
            criterio1=Q(usuario=request.user)
            cod=ForecastTablaManu.objects.all().filter(criterio1).order_by('-id').first()
            codi=cod.codigo
            print(codi)
            criterio2=Q(codigo=codi)
            data=ForecastTablaManu.objects.filter(criterio2)

            fechas=[]
            for f in data:
                fech=f.Fecha
                fechas.append(fech)

            valores=[]
            for v in data:
                valores.append(v.Forecast_ACTIVACIONES_POS)

            context={
                'fechas':fechas[:180],
                'valores':valores[:180],
            }

            return render(request, 'grafico_manu.html', context)
        
        except ValueError:
            messages.warning(request, 'Hubo un error')
            context={'mensaje': 'Error'}
            return render(request, 'grafico_manu.html', context)

    messages.warning(request, 'Error. No hay datos') 
    context={'mensaje': 'Error'}
    return render(request, 'grafico_manu.html', context)    

#grafica plotly ventas-precio-compCompetencia---->automático
def graficoPlotlyA(request):
    dataIni=ForecastTabla.objects.all().filter(usuario=request.user)
    if dataIni:
        criterio1=Q(usuario=request.user)
        cod=ForecastTabla.objects.all().filter(criterio1).order_by('-id').first()
        codi=cod.codigo
        print(codi)
        criterio2=Q(codigo=codi)

        data=ForecastTabla.objects.filter(criterio2)
        x=[f.Fecha for f in data]
        y=[v.Forecast_ACTIVACIONES_POS for v in data]
        y1=[p.PRECIO_DIRECTV for p in data]
        y2=[c.COMP_TELECENTRO for c in data]


        # Create traces---graficos lineas
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y,
                            mode='lines+markers',
                            name='Forecast_ACTIVACIONES_POS',
                            line=dict(color='red', width=2)))
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=x, y=y1,
                            mode='lines+markers',
                            name='PRECIO_DIRECTV',
                            line=dict(color='royalblue', width=2)))
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=x, y=y2,
                            mode='lines+markers', name='COMP_TELECENTRO',
                            line=dict(color='orange', width=2)))
        
        #graficos de cajas boxplot
        fig3 = go.Figure()
        fig3.add_trace(go.Box(y=y, name='Forecast_ACTIVACIONES_POS',line=dict(color='red', width=2)))

        fig4 = go.Figure()
        fig4.add_trace(go.Box(y=y1, name='PRECIO_DIRECTV',line=dict(color='royalblue', width=2)))

        fig5 = go.Figure()
        fig5.add_trace(go.Box(y=y2, name='COMP_TELECENTRO',line=dict(color='orange', width=2)))

        #fig.show()
        ventas=fig.to_html()
        ventasBp=fig3.to_html()
        precioDtv=fig1.to_html()
        precioDtvBp=fig4.to_html()
        comCompetencia=fig2.to_html()
        comCompetenciaBp=fig5.to_html()
        context={'ventas':ventas, 'precioDtv':precioDtv, 'comCompetencia':comCompetencia, 'ventasBp':ventasBp, 'precioDtvBp':precioDtvBp, 'comCompetenciaBp':comCompetenciaBp}
        return render(request, 'grafico_plotly_auto.html', context=context)
    messages.warning(request, 'Error. No hay datos') 
    context={'mensaje': 'Error'}
    return render(request, 'grafico_plotly_auto.html', context)

#grafica plotly ventas-precio-compCompetencia---->automático
def graficoPlotlyM(request):
    dataIni=ForecastTablaManu.objects.all().filter(usuario=request.user).count()
    if (dataIni)>0:
        try:
            criterio1=Q(usuario=request.user)
            cod=ForecastTablaManu.objects.all().filter(criterio1).order_by('-id').first()
            codi=cod.codigo
            print(codi)
            criterio2=Q(codigo=codi)

            data=ForecastTablaManu.objects.filter(criterio2)
            x=[f.Fecha for f in data]
            y=[v.Forecast_ACTIVACIONES_POS for v in data]
            y1=[p.PRECIO_DIRECTV for p in data]
            y2=[c.COMP_TELECENTRO for c in data]


            # Create traces---graficos lineas
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y,
                                mode='lines+markers',
                                name='Forecast_ACTIVACIONES_POS',
                                line=dict(color='red', width=2)))
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(x=x, y=y1,
                                mode='lines+markers',
                                name='PRECIO_DIRECTV',
                                line=dict(color='royalblue', width=2)))
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=x, y=y2,
                                mode='lines+markers', name='COMP_TELECENTRO',
                                line=dict(color='orange', width=2)))
            
            #graficos de cajas boxplot
            fig3 = go.Figure()
            fig3.add_trace(go.Box(y=y, name='Forecast_ACTIVACIONES_POS',line=dict(color='red', width=2)))

            fig4 = go.Figure()
            fig4.add_trace(go.Box(y=y1, name='PRECIO_DIRECTV',line=dict(color='royalblue', width=2)))

            fig5 = go.Figure()
            fig5.add_trace(go.Box(y=y2, name='COMP_TELECENTRO',line=dict(color='orange', width=2)))

            #fig.show()
            ventas=fig.to_html()
            ventasBp=fig3.to_html()
            precioDtv=fig1.to_html()
            precioDtvBp=fig4.to_html()
            comCompetencia=fig2.to_html()
            comCompetenciaBp=fig5.to_html()
            context={'ventas':ventas, 'precioDtv':precioDtv, 'comCompetencia':comCompetencia,'ventasBp':ventasBp, 'precioDtvBp':precioDtvBp, 'comCompetenciaBp':comCompetenciaBp}
            return render(request, 'grafico_plotly_manu.html', context=context)
        except ValueError:
            messages.warning(request, 'Hubo un error')
            context={'mensaje': 'Error'}
            return render(request, 'grafico_plotly_manu.html', context)
    messages.warning(request, 'Error. No hay datos') 
    context={'mensaje': 'Error'}
    return render(request, 'grafico_plotly_manu.html', context)