#!/usr/bin/env python3

# Quick hack to make the SQL insert for use in
# https://github.com/vipulnaik/donations/blob/master/sql/donations.sql

import re


DONEE_RENAME = {
    'Board of Trustees of the University of Illinois': 'University of Illinois',
    'Farm Foundation NFP': 'Farm Foundation',
    'Foundation for the National Institute of Health': 'Foundation for the National Institutes of Health',
    'Foundation of the University of Medicine and Dentistry of New Jersey': 'University of Medicine and Dentistry of New Jersey',
    'George Mason University Foundation': 'George Mason University',
    'Henry J. Kaiser Family Foundation': 'Kaiser Family Foundation',
    'Houston Independent School District Foundation': 'Houston Independent School District',
    'ID Insight': 'IDinsight',
    'International Centre for Genetic Engineering & Biotechnology': 'International Centre for Genetic Engineering and Biotechnology',
    'Measures for Justice Institute': 'Measures for Justice',
    'Ohio State University Foundation': 'Ohio State University',
    'Oklahoma State University': 'Oklahoma State University Foundation',
    'Oregon Health and Science University Foundation': 'Oregon Health & Science University',
    'Oxfam-America': 'Oxfam America',
    'President and Fellows of Harvard College': 'Harvard University',
    'President & Fellows of Harvard College': 'Harvard University',
    'Regents of the University of Colorado': 'University of Colorado',
    'Regents of the University of Michigan': 'University of Michigan',
    'Regents of the University of Minnesota': 'University of Minnesota',
    "Research Triangle Institute" : "RTI International",
    'Rutgers University Foundation': 'Rutgers University',
    "Seattle Children's Hospital Foundation": "Seattle Children's Hospital",
    'The Board of Trustees of the University of Illinois': 'University of Illinois',
    'The Henry J. Kaiser Family Foundation': 'Kaiser Family Foundation',
    'The Oakland Public Education Fund': 'Oakland Public Education Fund',
    'The Pennsylvania State University': 'Pennsylvania State University',
    'The Regents of the University of California, Berkeley': 'University of California, Berkeley',
    'The Regents of the University of California, Irvine': 'University of California, Irvine',
    'The Regents of the University of California, Los Angeles': 'University of California, Los Angeles',
    'The Regents of the University of California, San Diego': 'University of California, San Diego',
    'The Regents of the University of California, San Francisco': 'University of California, San Francisco',
    'The Regents of the University of California, Santa Barbara': 'University of California, Santa Barbara',
    'The Regents of the University of Michigan': 'University of Michigan',
    'The Research Foundation of State University of New York': 'Research Foundation of State University of New York',
    'The Trustees of Princeton University': 'Princeton University',
    'The University of Chicago': 'University of Chicago',
    'The University of Tennessee': 'University of Tennessee',
    'The University of Texas at Austin': 'University of Texas at Austin',
    'The University of Texas at Dallas': 'University of Texas at Dallas',
    'Trustees of Boston University': 'Boston University',
    'Trustees of Indiana University': 'Indiana University',
    'Trustees Of Princeton University': 'Princeton University',
    'Trustees of the University of Pennsylvania': 'University of Pennsylvania',
    'University of Arizona Foundation': 'University of Arizona',
    'University of California at San Diego': 'University of California, San Diego',
    'University of California - Berkeley': 'University of California, Berkeley',
    'University of California San Francisco': 'University of California, San Francisco',
    'University of California Santa Barbara': 'University of California, Santa Barbara',
    'University of Colorado Foundation': 'University of Colorado',
    'University of Colorado': 'University of Colorado Foundation',
    'University of Maryland Baltimore Foundation': 'University of Maryland, Baltimore',
    'University of Washington Foundation': 'University of Washington',
    'Ursuline Academy of Dallas Foundation': 'Ursuline Academy of Dallas',
    'Washington State University Foundation': 'Washington State University',
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
    if donee in DONEE_RENAME:
        donee = DONEE_RENAME[donee]
    return donee


print("""insert into donations (donor, donee, amount, donation_date,
    donation_date_precision, donation_date_basis, cause_area, url,
    donor_cause_area_url, notes, affected_countries, affected_states) values""")

with open("grants-with-multiyear.tsv", "r") as f:
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
            cause_area=area,
            donor_cause_area_url=donor_cause_area_url(area),
            notes=notes,
            affected_states=assign_state(recipient)
        ), end='')
    print(";")
