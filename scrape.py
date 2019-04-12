#!/usr/bin/env python3

import csv
import sys
import requests
from bs4 import BeautifulSoup

import pdb

def main():
    fieldnames = ["recipient", "purpose", "term", "amount"]
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()

    url_pat = "https://www.arnoldventures.org/grants/p{}?"
    has_next = True
    page_num = 1

    while has_next:
        url = url_pat.format(page_num)
        print("Downloading " + url, file=sys.stderr)
        response = requests.get(url,
                                headers={'User-Agent': 'Mozilla/5.0 '
                                         '(X11; Linux x86_64) AppleWebKit/537.36 '
                                         '(KHTML, like Gecko) '
                                         'Chrome/63.0.3239.132 Safari/537.36'})
        soup = BeautifulSoup(response.content, "lxml")
        tbody = soup.find("tbody", {"class": "grant-list__body"})
        for row in tbody.find_all("tr"):
            recipient, purpose, term, amount = list(map(lambda x: x.text.strip(),
                                                        row.find_all("td")))
            writer.writerow({
                "recipient": recipient,
                "purpose": purpose,
                "term": term,
                "amount": amount,
            })

        # This is a hacky way to detect the absence of a next page but the idea
        # is as follows: in all pages except the first and the last, there are
        # two pagination links, called "Prev" and "Next". So how do we find out
        # if we are on the last page? We first make sure we aren't on the first
        # page (page_num > 1) and then check if there is just one pagination
        # link.
        if page_num > 1 and len(soup.find("nav", {"class": "pagination"}).find_all("a")) == 1:
            has_next = False
        page_num += 1



if __name__ == "__main__":
    main()
