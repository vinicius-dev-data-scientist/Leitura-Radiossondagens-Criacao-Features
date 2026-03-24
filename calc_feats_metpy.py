import pandas as pd
import numpy as np
import os

from metpy.calc import (
        bulk_shear,
        wind_components,
        bunkers_storm_motion,
        corfidi_storm_motion,
        mixing_ratio_from_relative_humidity,
        galvez_davison_index
)
from metpy.units import units


df = pd.read_csv(r'C:\Users\gabriel.pereira\Downloads\sondagens_manaus_2026\2026010112.csv')

df =  df.dropna(subset=['PRES', 'DRCT', 'SKNT', 'HGHT'])

# variáveis
p = df['PRES'].values * units.hPa
h = df['HGHT'].values * units.m
wdir = df['DRCT'].values * units.degree
sped = df['SKNT'].values * units.knots

T = df['TEMP'].values * units.degC
rh = df['RELH'].values / 100.0

# cálculos

u, v = wind_components(sped, wdir)

mixrat = mixing_ratio_from_relative_humidity(p, T, rh)

# bulk shear (recomendado 6km)
u_shr, v_shr = bulk_shear(p, u, v, height=h, depth=6000 * units.m)
shr_mag = np.hypot(u_shr, v_shr)

# bunkers
rm, lm, mean = bunkers_storm_motion(p, u, v, h)

# corfidi
up, down = corfidi_storm_motion(p, u, v)

# galvez-davison
galvez = galvez_davison_index(p, T, mixrat, p[0])

def mag(u, v):
    return np.hypot(u, v)
    
# construção variáveis

data = {
    #bulk shear
    'shr06_u': u_shr.m,
    'shr06_v': v_shr.m,
    'shr06_mag': shr_mag.m,
    
    #bunkers
    'rm_u': rm[0].m,
    'rm_v': rm[1].m,
    'rm_speed': mag(rm[0], rm[1]).m,
    
    'mean_u': mean[0].m,
    'mean_v': mean[1].m,
    'mean_speed': mag(mean[0], mean[1]).m,
    
    #corfidi
    'corfidi_up_u': up[0].m,
    'corfidi_up_v': up[1].m,
    'corfidi_up_speed': mag(up[0], up[1]).m,
    
    'corfidi_down_u': down[0].m,
    'corfidi_down_v': down[1].m,
    'corfidi_down_speed': mag(down[0], down[1]).m,
    
    #index
    'galvez_davison': galvez.m

}

df_feats = pd.DataFrame([data])

df_feats.to_csv(r'C:\Users\gabriel.pereira\estagio_radiossondagens_calculovariaveis\feats_indexes.csv', index=False)
