PostgreSQL Notes
================

https://www.postgresql.org/docs

create user and delete user

```
sudo -u postgres createuser --interactive username
sudo -u postgres dropuser username
```

create dateabase

```
createdb name
dropdb name
psql -l
```

accessing a databse

```
psql name
> \q  # quit
```
