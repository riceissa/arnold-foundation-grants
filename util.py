#!/usr/bin/python3

from math import log10, floor

def percentage_round(percentage):
    if percentage > 1:
        percentage = round(percentage, 1)
    else:
        percentage = round(percentage, -int(floor(log10(abs(percentage)))))
    return percentage

def wikilink(title):
    return "[[" + title + "]]"

