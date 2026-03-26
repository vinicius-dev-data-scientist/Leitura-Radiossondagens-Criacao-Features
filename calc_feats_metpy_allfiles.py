import pandas as pd
import numpy as np
import glob
import os

from metpy.calc import (
    bulk_shear,
    wind_components,
    bunkers_storm_motion,
    corfidi_storm_motion,
    galvez_davison_index
)
from metpy.units import units

PASTA_ENTRADA = r'C:\Users\gabriel.pereira\estagio\sondagens_manaus_2026'

arquivos = glob.glob(os.path.join(PASTA_ENTRADA, '*.csv'))

resultados = []


def processar_arquivo(caminho):
    df = pd.read_csv(caminho)

    df = df.dropna(subset=['PRES', 'DRCT', 'SKNT', 'HGHT'])

    p = df['PRES'].values * units.hPa
    h = df['HGHT'].values * units.m
    wdir = df['DRCT'].values * units.degree
    sped = df['SKNT'].values * units.knots

    T = df['TEMP'].values * units.degC
    mixrat = df['MIXR'].values * units('g/kg')

    u, v = wind_components(sped, wdir)

    # bulk shear
    u_shr, v_shr = bulk_shear(p, u, v, height=h, depth=6000 * units.m)
    shr_mag = np.hypot(u_shr, v_shr)

    # bunkers
    rm, lm, mean = bunkers_storm_motion(p, u, v, h)

    # corfidi
    up, down = corfidi_storm_motion(p, u, v)

    # galvez
    galvez = galvez_davison_index(p, T, mixrat, p[0])

    def mag(u, v):
        return np.hypot(u, v)

    data = {
        'shr06_u': u_shr.m,
        'shr06_v': v_shr.m,
        'shr06_mag': shr_mag.m,

        'rm_u': rm[0].m,
        'rm_v': rm[1].m,
        'rm_speed': mag(rm[0], rm[1]).m,

        'mean_u': mean[0].m,
        'mean_v': mean[1].m,
        'mean_speed': mag(mean[0], mean[1]).m,

        'corfidi_up_u': up[0].m,
        'corfidi_up_v': up[1].m,
        'corfidi_up_speed': mag(up[0], up[1]).m,

        'corfidi_down_u': down[0].m,
        'corfidi_down_v': down[1].m,
        'corfidi_down_speed': mag(down[0], down[1]).m,

        'galvez_davison': galvez.m
    }

    return data
    
    
def extrair_data(nome_arquivo):
    base = os.path.basename(nome_arquivo).replace('.csv', '')
    return pd.to_datetime(base, format='%Y%m%d%H')
    
for arq in arquivos:
    try:
        data = processar_arquivo(arq)
        data['datetime'] = extrair_data(arq)
        resultados.append(data)
    except Exception as e:
        print(f'Erro em {arq}: {e}')
        
        
df_final = pd.DataFrame(resultados)

# definir índice temporal
df_final = df_final.set_index('datetime')

# ordenar por tempo
df_final = df_final.sort_index()


df_final.to_csv(r'C:\Users\gabriel.pereira\estagio\novas_feats.csv')

