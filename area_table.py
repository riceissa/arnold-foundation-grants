#!/usr/bin/python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from util import *

df = pd.read_csv('grants.tsv', sep='\t')
areas = df.area.unique()
total = df.amount.sum()
print('{| class="sortable wikitable"')
print('! Focus area !! Amount !! Recipients !! Percentage of total amount')
for area in areas:
    print('|-')
    rs = ", ".join(wikilink(x)
            for x in df[df.area == area].recipient.unique().tolist())
    amt = df.groupby('area')['amount'].sum()[area]
    p = amt / total * 100
    print('| {} || {:,d} || {} || {}'.format(area, amt, rs, percentage_round(p)))
print('|-')
print("! Total amount granted || {:,d} || || 100%".format(total))
print('|}')
