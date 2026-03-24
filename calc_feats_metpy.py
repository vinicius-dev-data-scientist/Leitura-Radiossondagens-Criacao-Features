import pandas as pd
import numpy as np
import os

from metpy.calc import bulk_shear, wind_components, bunkers_storm_motion, corfidi_storm_motion, mixing_ratio_from_relative_humidity, galvez_davison_index
from metpy.units import units


df = pd.read_csv(r'C:\Users\gabriel.pereira\Downloads\sondagens_manaus_2026\2026010112.csv')

df =  df.dropna(subset=['PRES', 'DRCT', 'SKNT', 'HGHT'])

p = df['PRES'].values * units.hPa
wdir = df['DRCT'].values * units.degree
sped = df['SKNT'].values * units.knots

h = df['HGHT'].values * units.m

T = df['TEMP'].values * units.degC
rh = df['RELH'].values * units.dimensionless
mixrat = mixing_ratio_from_relative_humidity(p, T, rh)

u, v = wind_components(sped, wdir)
#print(f"Cisalhamento oeste-leste: {u}\n Cisalhamento norte-sul: {v}")

shear = bulk_shear(p, u, v) #height=h, depth=6000 * units.m
print(f'Cisalhamento Volumoso: {shear}')

bstorm = bunkers_storm_motion(p, u, v, h)
print(f'\nMovimento de tempestade de bunkers: {bstorm}')

corfidi = corfidi_storm_motion(p, u, v)
print(f'\nMovimento de tempestade de corfidi: {corfidi}')

galvez = galvez_davison_index(p, T, mixrat, p[0])
print(f'\nÍndice de Galvez Davison: {galvez}')

print(type(corfidi))


data = {

    'bulk_shear': [shear],
    'bunkers_storm_motion': [bstorm],
    'corfidi_sorm_motion': [corfidi],
    'galvez_davison_index': [galvez]

}

df_feats = pd.DataFrame(data)

df_feats.to_csv(r'C:\Users\gabriel.pereira\estagio_radiossondagens_calculovariaveis\feats_indexes.csv')
