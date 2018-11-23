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
