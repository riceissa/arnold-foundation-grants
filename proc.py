#!/usr/bin/env python3

import sys
import csv
import re

import util

# This is just a quick way to normalize some common discrepancies in naming
# donees *within Arnold Foundation's data*. It's used for matching the donee
# names across different Arnold data sets when we backfill the cause areas.
# It's not meant to be used as a normalization function for DLW's data.
def normalized_donee(donee):
    return donee.replace("–", "-").replace("men?s", "men's").replace("’", "'").replace("Lawyers?", "Lawyers'")


# Since the new Arnold grants data does not have cause area info, use the older
# data to figure out the cause area, in cases where we can do this.
GRANTS = []  # List of all grants from the older data
DONEE_TO_AREA = {}  # Track the *most recent* area for each donee
most_recent_year_for_donee = {}  # Track the most recent year seen for each
                                 # donee; this helps us construct DONEE_TO_AREA
with open(sys.argv[2], "r") as f:
    next(f)  # skip header line of tsv
    for line in f:
        area, recipient, year, amount, donation_date_precision, notes = line.strip().split("\t")
        recipient = normalized_donee(recipient)
        assert notes.startswith('Grant period: ')
        term = notes[len('Grant period: '):]
        GRANTS.append({
            'recipient': recipient,
            'term': term,
            'amount': float(amount),
            'area': area
        })

        if recipient in DONEE_TO_AREA:
            # If we have already seen this donee, only over-write the area if
            # we have a more recent year
            if int(year) > most_recent_year_for_donee[recipient]:
                DONEE_TO_AREA[recipient] = area
                most_recent_year_for_donee[recipient] = int(year)
        else:
            DONEE_TO_AREA[recipient] = area
            most_recent_year_for_donee[recipient] = int(year)


def get_area(donee, term, amount):
    """Find the area for a given (donee, term, amount) combination, by first
    looking for an exact match (with amount up to a $2 difference) and then
    looking for a donee/recipient match (using the area of the most recent
    grant as the area)."""
    for grant in GRANTS:
        # For amount, there are some rounding errors on Arnold's part, so
        # subtract the two amounts and consider them equal if they're within $2
        if (normalized_donee(donee) == grant['recipient'] and
                term == grant['term'] and abs(amount - grant['amount']) <= 2):
            # GRANTS.remove(grant)
            return grant['area']

    # If we make it to here, there was no exact match for the grant, so fall
    # back on using just the latest area of the recipient
    if normalized_donee(donee) in DONEE_TO_AREA:
        return DONEE_TO_AREA[normalized_donee(donee)]

    return None


def main():
    with open(sys.argv[1], newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        print("""insert into donations (donor, donee, amount, donation_date, donation_date_precision, donation_date_basis, cause_area, donor_cause_area_url, url, notes, affected_states) values""")
        first = True

        for row in reader:
            amount_list = row["amount"].split()
            if len(amount_list) == 1:
                assert amount_list[0].startswith("$")
                amount = float(amount_list[0].replace("$", "").replace(",", ""))
            else:
                assert len(amount_list) == 3
                assert amount_list[:2] == ["Up", "To"]
                amount = float(amount_list[2].replace("$", "").replace(",", ""))

            match = re.match(r"(\d\d\d\d)( - \d\d\d\d)?$", row["term"])
            year = match.group(1)
            donation_date = year + "-01-01"

            area = get_area(row["recipient"], row["term"], amount)

            print(("    " if first else "    ,") + "(" + ",".join([
                mysql_quote("Arnold Ventures"),  # donor
                mysql_quote(util.donee_clean(row["recipient"])),  # donee
                str(amount),  # amount
                mysql_quote(donation_date),  # donation_date
                mysql_quote("year"),  # donation_date_precision
                mysql_quote("donation log"),  # donation_date_basis
                mysql_quote(util.standardize_cause_area(area)),  # cause_area
                util.donor_cause_area_url(area),  # donor_cause_area_url
                mysql_quote("https://www.arnoldventures.org/grants/"),  # url
                mysql_quote(row["purpose"]),  # notes
                util.assign_state(row["recipient"]),  # affected_states
            ]) + ")")
            first = False
        print(";")
        # for t in GRANTS:
        #     print(t, file=sys.stderr)


def mysql_quote(x):
    """Quote the string x using MySQL quoting rules. If x is the empty string,
    return "NULL". Probably not safe against maliciously formed strings, but
    our input is fixed and from a basically trustable source."""
    if not x:
        return "NULL"
    x = x.replace("\\", "\\\\")
    x = x.replace("'", "''")
    x = x.replace("\n", "\\n")
    return "'{}'".format(x)


if __name__ == "__main__":
    main()
