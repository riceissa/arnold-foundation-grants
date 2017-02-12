#!/usr/bin/python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from util import *

num_outside_collapse = 10

df = pd.read_csv('grants.tsv', sep='\t')
areas = df.area.unique()
total = df.amount.sum()
print('{| class="sortable wikitable"')
print('! Focus area !! Amount !! Recipients !! Percentage of total amount')
for area in areas:
    print('|-')
    rs = df[df.area == area].groupby('recipient').sum().sort_values(by='amount',
            ascending=False).index
    amt = df.groupby('area')['amount'].sum()[area]
    p = amt / total * 100
    print('| {}'.format(area))
    print('| style="text-align: right;" | {:,d}'.format(amt))
    if len(rs) > 10:
        top = rs[:num_outside_collapse]
        rest = rs[num_outside_collapse:]
        print('| {}'.format(", ".join(wikilink(x) for x in top))
                + "{{collapse|"
                + ", ".join(wikilink(x) for x in rest)
                + "|More recipients}}"
        )
    else:
        print('| {}'.format(", ".join(wikilink(x) for x in rs)))
    print('| {}'.format(percentage_round(p)))
print('|-')
print("! Total amount granted")
print('! style="text-align: right;" | {:,d}'.format(total))
print("!")
print('! style="text-align: right;" | 100.0')
print('|}')
