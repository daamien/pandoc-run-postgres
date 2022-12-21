# pandoc-run-postgres

Execute SQL queries inside a markdown document

## Example

1. Write a SQL query in a code block

~~~ markdown
    ``` run-postgres
    SELECT oid, 'hello ' || rolname || '!' AS greetings from pg_roles
      Limit 2;
    ```
~~~

2. Call pandoc

```
export PGHOST=localhost
export PGDATABASE=foo
export PGUSER=bob
export PGPASSWORD=xxxxxxxx
pandoc --filter pandoc-run-postgres hello.md -o result.md
```

3. The output will contain the SQL query inside a SQL codeblock and
   the result in a table:


~~~ markdown

  ```sql
  SELECT oid,
         'hello ' || rolname || '!' AS greetings
  FROM pg_roles
  LIMIT 2;

  ```

    oid    greetings
    ------ -----------------------------
    33731  hello bob!
    33748  hello alice!
~~~



## Install

```
pip install pandoc-run-postgres
```

## Configuration

See examples in `sample.md`.


## Similar projects

* [pandoc-filter-runsql] for MySQL
* Jupyter's [ipython-sql]


[ipython-sql]: https://github.com/catherinedevlin/ipython-sql
[pandoc-filter-runsql]: https://github.com/barskern/pandoc-filter-runsql
