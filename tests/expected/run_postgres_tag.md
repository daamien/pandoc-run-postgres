# pandoc-run-postgres

## Basic Usage

``` sql
SeLeCT 1 AS TesT1
```

  test1
  -------
  1

## Do not show the query

  schemaname   tablename      tableowner   tablespace   hasindexes   hasrules   hastriggers   rowsecurity
  ------------ -------------- ------------ ------------ ------------ ---------- ------------- -------------
  pg_catalog   pg_statistic   postgres     None         True         False      False         False
  pg_catalog   pg_type        postgres     None         True         False      False         False

## Error

``` sql

SELLLLLECT 1;
```

::: {class="warning"}
run-postgres: syntax error at or near "SELLLLLECT" LINE 1: SELLLLLECT 1;
\^
:::

## Do not show the result

``` {.sql show_result="false"}
SeLeCT * from pg_tables LIMIT 2;
```

## Write a table

``` sql
CREATE TEMPORARY TABLE tmp_121 AS SELECT 1;
```
