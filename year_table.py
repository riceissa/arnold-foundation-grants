#!/usr/bin/python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from util import *

num_outside_collapse = 10

df = pd.read_csv('grants.tsv', sep='\t')
years = df.year.sort_values().unique()
total = df.amount.sum()
print('{| class="sortable wikitable"')
print('! Year !! Amount !! Recipients !! Percentage of total amount')
for year in years:
    print('|-')
    rs = df[df.year == year].groupby('recipient').sum().sort_values(by='amount',
            ascending=False).index
    amt = df.groupby('year')['amount'].sum()[year]
    p = amt / total * 100
    print('| {}'.format(year))
    print('| {:,d}'.format(amt))
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
print("! Total amount granted || {:,d} || || 100%".format(total))
print('|}')
