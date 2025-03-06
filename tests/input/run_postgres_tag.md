# pandoc-run-postgres

## Basic Usage

```run-postgres
SeLeCT 1 AS TesT1
```

## Do not show the query

``` {.run-postgres show_query=False}
SeLeCT * from pg_tables LIMIT 2;
```

## Error

```run-postgres

SELLLLLECT 1;
```

## Do not show the result

``` {.run-postgres  show_result=false}
SeLeCT * from pg_tables LIMIT 2;
```

## Write a table

```run-postgres
CREATE TEMPORARY TABLE tmp_121 AS SELECT 1;
```
