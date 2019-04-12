#!/usr/bin/env python3

import sys
import csv
import re

def main():
    with open(sys.argv[1], newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        print("""insert into donations (donor, donee, amount, donation_date, donation_date_precision, donation_date_basis, cause_area, url, notes) values""")
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
            donation_date = match.group(1) + "-01-01"

            print(("    " if first else "    ,") + "(" + ",".join([
                mysql_quote("Arnold Ventures"),  # donor
                mysql_quote(row["recipient"]),  # donee
                str(amount),  # amount
                mysql_quote(donation_date),  # donation_date
                mysql_quote("year"),  # donation_date_precision
                mysql_quote("donation log"),  # donation_date_basis
                mysql_quote(""),  # cause_area
                mysql_quote("https://www.arnoldventures.org/grants/"),  # url
                mysql_quote(row["purpose"]),  # notes
            ]) + ")")
            first = False
        print(";")


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
