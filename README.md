Run the following commands to update grants.sql:

```bash
curl http://www.arnoldfoundation.org/grants/ > index.html
python3.5 fetch_page.py > grants-with-multiyear.tsv
python3.5 loop.py > grants.sql
```

The following commands are to insert into [donations list website](https://github.com/vipulnaik/donations) and git repository:

```bash
mysql donations -p < grants.sql # Enter password on being prompted
cp grants.sql ../donations/sql/donations/arnold-foundation-grants.sql
cd ../donations
# Then git diff, commit, push, etc.
```
