#!/usr/bin/env python3

# Quick hack to make the SQL insert for use in
# https://github.com/vipulnaik/donations/blob/master/sql/donations.sql

import sys

from util import *

print("""insert into donations (donor, donee, amount, donation_date,
    donation_date_precision, donation_date_basis, cause_area, url,
    donor_cause_area_url, notes, affected_countries, affected_states) values""")


with open(sys.argv[1], "r") as f:
    next(f)  # skip header line of tsv
    continuing = False
    for line in f:
        if continuing:
            print(",")
        else:
            continuing = True
        area, recipient, year, amount, donation_date_precision, notes = line.strip().split("\t")
        print("""    ("Laura and John Arnold Foundation","{donee}",{amount},"{donation_date}-01-01","{donation_date_precision}","donation log","{cause_area}","http://www.arnoldfoundation.org/grants/",{donor_cause_area_url},"{notes}","United States",{affected_states})""".format(
            donee=donee_clean(recipient),
            amount=amount,
            donation_date=year,
            donation_date_precision=donation_date_precision,
            cause_area=standardize_cause_area(area),
            donor_cause_area_url=donor_cause_area_url(area),
            notes=notes,
            affected_states=assign_state(recipient)
        ), end='')
    print(";")
