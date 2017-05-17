Run the following commands

curl http://www.arnoldfoundation.org/grants/ > index.html
python3.5 fetch_page.py > grants-with-multiyear.tsv
python3.5 loop.py > grants.sql
