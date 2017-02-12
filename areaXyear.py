#!/usr/bin/python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from util import *

df = pd.read_csv('grants.tsv', sep='\t')
areas = df.area.unique()
years = df.year.sort_values().unique()
group = df.groupby(['area', 'year']).amount.sum()

print('{| class="sortable wikitable"')
print("|-")
print("!")
print('! colspan="{}" | Grant amount'.format(len(years) + 1))
print('|-')
print('! Focus areas !! ' + '!!'.join(str(y) for y in years) + '!! Sum')
for area in areas:
    print('|-')
    print('| {}'.format(area))
    for year in years:
        if year in group[area]:
            amount = group[area][year]
        else:
            amount = 0
        print('| style="text-align:right;" | {:,d}'.format(amount))
    area_sums = df.groupby('area').amount.sum()
    print('| style="text-align:right;" | {:,d}'.format(area_sums[area]))

year_sums = df.groupby('year').amount.sum()
print('|-')
print('! Total')
for y in years:
    print('! style="text-align:right;" | {:,d}'.format(year_sums[y]))
print('! style="text-align:right;" | {:,d}'.format(year_sums.sum()))
print('|}')
