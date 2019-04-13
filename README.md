## New instructions

Get new grants data:

```bash
./scrape.py > grants-YYYY-MM-DD.csv
```

Use CSV file to generate SQL (the older `grants-with-multiyear.tsv` file is required for figuring out the cause areas of grants):

```bash
./proc.py grants-YYYY-MM-DD.csv grants-with-multiyear.tsv > out.sql
```

## Old instructions

Run the following commands to update out.sql:

```bash
curl http://www.arnoldfoundation.org/grants/ > index.html
python3.5 fetch_page.py index.html > grants-with-multiyear.tsv
python3.5 loop.py grants-with-multiyear.tsv > out.sql
```

The following commands are to insert into [donations list website](https://github.com/vipulnaik/donations) and git repository:

```bash
mysql donations -p < out.sql # Enter password on being prompted
cp out.sql ../donations/sql/donations/private-foundations/arnold-foundation-grants.sql
cd ../donations
# Then git diff, commit, push, etc.
```
