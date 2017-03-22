#!/usr/bin/python3

from bs4 import BeautifulSoup
import operator

TRACK_MULTIYEAR = True

def main():
    with open("index.html", "r") as f:
        soup = BeautifulSoup(f, "html.parser")
    grants = []
    # Collect the grant areas to match up with the tables
    areas = (area.string for area in soup.find_all("h4", class_="grant"))
    for table in soup.find_all("table"):
        area = next(areas)
        for row in table.find_all("tr"):
            g = {}
            recipient = row.find("td", class_="recipient")
            if recipient:
                g['recipient'] = recipient.string
                year_raw = row.find("td", class_="term").string
                if TRACK_MULTIYEAR:
                    if "-" in year_raw:
                        # Presence of hyphen indicates the grant spans multiple
                        # years
                        g['multiyear'] = "multi-year"
                    else:
                        g['multiyear'] = "year"
                # We'll just use the starting year for the "year" column
                g['year'] = year_raw.split()[0]
                amount = row.find("td", class_="amount").string \
                        .replace(',', '').replace('$', '')
                if amount.startswith("up to "):
                    g['amount'] = amount[len("up to "):]
                else:
                    g['amount'] = amount
                g['area'] = area
                grants.append(g)
    print("area\trecipient\tyear\tamount")
    if TRACK_MULTIYEAR:
        for g in sorted(grants,
                key=operator.itemgetter("area", "recipient", "year", "amount", "multiyear")):
            line = "\t".join([
                g['area'],
                g['recipient'],
                g['year'],
                g['amount'],
                g['multiyear'],
            ])
            print(line)
    else:
        for g in sorted(grants,
                key=operator.itemgetter("area", "recipient", "year", "amount")):
            line = "\t".join([
                g['area'],
                g['recipient'],
                g['year'],
                g['amount'],
            ])
            print(line)

if __name__ == "__main__":
    main()
