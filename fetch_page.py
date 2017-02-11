#!/usr/bin/python3

from bs4 import BeautifulSoup

def main():
    with open("index.html", "r") as f:
        soup = BeautifulSoup(f, "html.parser")
    grants = []
    # Collect the grant areas to match up with the tables
    areas = (area for area in soup.find_all("h4", class_="grant"))
    for table in soup.find_all("table"):
        for row in first.find_all("tr"):
            g = {}
            recipient = row.find("td", class_="recipient")
            if recipient:
                g['recipient'] = recipient.string
                g['year'] = row.find("td", class_="term").string.split()[0]
                g['amount'] = row.find("td", class_="amount").string.replace(',', '').replace('$', '')
                g['area'] = area
                print(g)

if __name__ == "__main__":
    main()
