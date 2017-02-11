#!/usr/bin/python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from util import *

df = pd.read_csv('grants.tsv', sep='\t')
years = df.year.sort_values().unique()
total = df.amount.sum()
print('{| class="sortable wikitable"')
print('! Year !! Amount !! Recipients !! Percentage of total amount')
for year in years:
    print('|-')
    rs = ", ".join(wikilink(x)
            for x in df[df.year == year].recipient.unique().tolist())
    amt = df.groupby('year')['amount'].sum()[year]
    p = amt / total * 100
    print('| {} || {:,d} || {} || {}'.format(year, amt, rs, percentage_round(p)))
print('|-')
print("! Total amount granted || {:,d} || || 100%".format(total))

# print(df.groupby('year')['amount'].sum())
print('|}')
