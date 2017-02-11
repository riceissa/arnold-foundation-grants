#!/usr/bin/python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import log10, floor

def percentage_round(percentage):
    if percentage > 1:
        percentage = round(percentage)
    else:
        percentage = round(percentage, -int(floor(log10(abs(percentage)))))
    return percentage

df = pd.read_csv('grants.tsv', sep='\t')
areas = df.area.unique()
total = df.amount.sum()
print('{| class="sortable wikitable"')
print('! Focus area !! Amount !! Recipients !! Percentage of total amount')
for area in areas:
    print('|-')
    rs = ", ".join(df[df.area == area].recipient.unique().tolist())
    amt = df.groupby('area')['amount'].sum()[area]
    p = amt / total * 100
    print('| {} || {:,d} || {} || {}'.format(area, amt, rs, percentage_round(p)))
print('|-')
print("! Total amount granted || {:,d} || || 100%".format(total))

# print(df.groupby('year')['amount'].sum())
print('|}')
