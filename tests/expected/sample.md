# pandoc-run-postgres

## Basic Usage

``` {.sql run-postgres="True"}
SeLeCT 1 AS TesT1
```

  test1
  -------
  1

## Run with specific conninfo params

``` {.sql run-postgres="True" user="ghost"}
SELECT "This will fail because the user does not exist"
```

::: {class="warning"}
run-postgres: connection failed: connection to server at "172.18.0.3",
port 65432 failed: FATAL: password authentication failed for user
"ghost"
:::

## Do not run a query

``` sql
SELECT 'THIS IS NOT EXECUTED';
```

## Do not show the query

  schemaname   tablename   tableowner   tablespace   hasindexes   hasrules   hastriggers   rowsecurity
  ------------ ----------- ------------ ------------ ------------ ---------- ------------- -------------
  pg_catalog   pg_type     postgres     None         True         False      False         False

## Error

``` {.sql run-postgres="True"}

SELLLLLECT 1;
```

::: {class="warning"}
run-postgres: syntax error at or near "SELLLLLECT" LINE 1: SELLLLLECT 1;
\^
:::

## Do not show the result

``` {.sql run-postgres="True" show_result="false"}
SeLeCT * from pg_tables WHERE tablename='pg_type';
```

## Write a table

``` {.sql run-postgres="True"}
CREATE TEMPORARY TABLE tmp_121 AS SELECT 1;
```

## Write a function

``` {.sql run-postgres="True"}
CREATE OR REPLACE FUNCTION remove_content_and_ip(message JSONB)
RETURNS JSONB
VOLATILE
LANGUAGE SQL
AS $func$
SELECT
  jsonb_set(message, '{meta, email}', '{}')
  - ARRAY['content'];
$func$;
```

``` {.sql run-postgres="True"}
SELECT
  remove_content_and_ip(
    jsonb_build_object(
      'content','plop',
      'meta',jsonb_build_object('email','foo@bar.com')
    )
  );
```

  remove_content_and_ip
  -----------------------------
  {\'meta\': {\'email\': {}}}
