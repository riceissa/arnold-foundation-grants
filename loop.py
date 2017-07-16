#!/usr/bin/env python3

# Quick hack to make the SQL insert for use in
# https://github.com/vipulnaik/donations/blob/master/sql/donations.sql

import re


DONEE_RENAME = {
    "Research Triangle Institute" : "RTI International"
}

def assign_state(recipient):
    """
    Try to assign a state to the recipient. If not possible, return "NULL".
    States have alphabetical precedence.
    """
    states = [
        "Alabama", "Alaska", "Arizona",
        "Arkansas", "California", "Colorado",
        "Connecticut", "Delaware", "Florida",
        "Georgia", "Hawaii", "Idaho",
        "Illinois", "Indiana", "Iowa",
        "Kansas", "Kentucky", "Louisiana",
        "Maine", "Maryland", "Massachusetts",
        "Michigan", "Minnesota", "Mississippi",
        "Missouri", "Montana", "Nebraska",
        "Nevada", "New Hampshire", "New Jersey",
        "New Mexico", "New York", "North Carolina",
        "North Dakota", "Ohio", "Oklahoma",
        "Oregon", "Pennsylvania", "Rhode Island",
        "South Carolina", "South Dakota", "Tennessee",
        "Texas", "Utah", "Vermont",
        "Virginia", "Washington", "West Virginia",
        "Wisconsin", "Wyoming",
    ]
    for s in states:
        if s in recipient:
            return "'" + s + "'"
    return "NULL"

def donor_cause_area_url(area):
    if area == "Criminal Justice":
        return "'http://www.arnoldfoundation.org/initiative/criminal-justice/'"
    if area == "Education":
        return "'http://www.arnoldfoundation.org/initiative/education/'"
    if area == "Evidence-Based Policy and Innovation":
        return "'http://www.arnoldfoundation.org/initiative/evidence-based-policy-innovation/'"
    if area == "New Initiatives":
        return "'http://www.arnoldfoundation.org/initiative/venture-development/'"
    if area == "Research Integrity":
        return "'http://www.arnoldfoundation.org/initiative/research-integrity/'"
    if area == "Sustainable Public Finance":
        return "'http://www.arnoldfoundation.org/initiative/sustainable-public-finance/'"
    else:
        return "NULL"

def donee_clean(donee):
    donee = re.sub(r",? inc\.?$", "", donee, flags=re.IGNORECASE)
    return donee

print("""insert into donations (donor, donee, amount, donation_date,
    donation_date_precision, donation_date_basis, cause_area, url,
    donor_cause_area_url, notes, affected_countries, affected_states) values""")

with open("grants-with-multiyear.tsv", "r") as f:
    headerLine = True
    continuing = False
    for line in f:
        if headerLine == True:
            headerLine = False
        else:
            if continuing == True:
                print(",")
            else:
                continuing = True
            area, recipient, year, amount, donation_date_precision, notes = line.strip().split("\t")
            if recipient in DONEE_RENAME:
                recipient = DONEE_RENAME[recipient]
            print("""    ("Laura and John Arnold Foundation","{donee}",{amount},"{donation_date}-01-01","{donation_date_precision}","donation log","{cause_area}","http://www.arnoldfoundation.org/grants/",{donor_cause_area_url},"{notes}","United States",{affected_states})""".format(
                donee=donee_clean(recipient),
                amount=amount,
                donation_date=year,
                donation_date_precision=donation_date_precision,
                cause_area=area,
                donor_cause_area_url=donor_cause_area_url(area),
                notes=notes,
                affected_states=assign_state(recipient)
            ), end='')
    print(";")
