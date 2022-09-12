import pandas as pd
import numpy as np
#from django.core.management.base import BaseCommand
#from RFapp.models import ForecastRF
import joblib
from sklearn.ensemble import RandomForestRegressor
#from sqlalchemy import create_engine
import datetime
from datetime import timedelta
from django.conf import settings
import os

from Forecast.settings import BASE_DIR


def crea_data_pred2(n):

    cols4=['CONTACTOS_TLV',
    'CONTACTOS_WEB',
    'CONTACTOS_IMP',
    'BB_CATEGORIA',
    'DTV_PROGRAMACION',
    'DTV_TOH',
    'MACRO_IPC',
    'MACRO_USD',
    'GT_DEPOR_COPA_ARGENTINA',
    'GT_DEPOR_CHAMPIONS_LEAGUE',
    'GT_DEPOR_REAL_VS_BARZA',
    'GT_DEPOR_RACING_VS_INDEP',
    'GT_DEPOR_MUNDIAL_FUTBOL',
    'GT_DEPOR_ROLAND_GARROS',
    'GT_DEPOR_WIMBLEDON',
    'PRECIO_DIRECTV',
    'DTV__CTA',
    'COMP_TELECENTRO',
    'CBV_TOH',
    'CBV_DEPORTE',
    'TEL_GOOGLETRENDS']

    ruta=os.path.join(BASE_DIR,'RFapp/modeloML','estadisticos_model_ml.csv')
    #estadisticos=pd.read_csv('modeloML/estadisticos_model_ml.csv')
    estadisticos=pd.read_csv(ruta)
    dfr=pd.DataFrame()
    data=[]
    for i,j in zip(cols4,range(2,23)):
        serie=np.random.uniform(low=estadisticos.iloc[3,j], high=estadisticos.iloc[7,j], size=(n))
        dfr[i]=list(serie)
    hoy=datetime.datetime.now().strftime("%Y-%m-%d")
    dfr['Fecha']=pd.date_range(hoy,periods=n, freq='d')
    return dfr

def dataset_ok(n):
    dfr=crea_data_pred2(n)
    dfr['Dia']=dfr.Fecha.dt.day
    dfr['Mes']=dfr.Fecha.dt.month
    dfr=dfr.reindex(columns=[
    'Dia',
    'Mes',
    'CONTACTOS_TLV',
    'CONTACTOS_WEB',
    'CONTACTOS_IMP',
    'BB_CATEGORIA',
    'DTV_PROGRAMACION',
    'DTV_TOH',
    'MACRO_IPC',
    'MACRO_USD',
    'GT_DEPOR_COPA_ARGENTINA',
    'GT_DEPOR_CHAMPIONS_LEAGUE',
    'GT_DEPOR_REAL_VS_BARZA',
    'GT_DEPOR_RACING_VS_INDEP',
    'GT_DEPOR_MUNDIAL_FUTBOL',
    'GT_DEPOR_ROLAND_GARROS',
    'GT_DEPOR_WIMBLEDON',
    'PRECIO_DIRECTV',
    'DTV__CTA',
    'COMP_TELECENTRO',
    'CBV_TOH',
    'CBV_DEPORTE',
    'TEL_GOOGLETRENDS'])
    return dfr

def forecast_result(n):
    #model_ml=joblib.load('modeloML/ml_RF_model.joblib')
    ruta=os.path.join(BASE_DIR,'RFapp/modeloML','ml_RF_model.joblib')
    model_ml=joblib.load(ruta)
    df_train=dataset_ok(n)
    y_pred=model_ml.predict(df_train)
    df_pred=pd.DataFrame({'Forecast_ACTIVACIONES_POS':y_pred})
    df_result=pd.concat([df_train,df_pred], axis=1)
    return df_result


# class Command(BaseCommand):
#     help='Generador datos modelo machine learning RF'

#     def handle(self, n,*args, **kwargs):

#         df=forecast_result(n)
#         engine=create_engine('sqlite:///db.sqlite3')
#         df.to_sql(ForecastRF._meta.db_table, if_exists='append', con=engine, index=False)

# test=Command()
# prueba=test.handle(30)
# print(prueba)
