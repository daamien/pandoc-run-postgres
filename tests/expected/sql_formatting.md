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

``` sql
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
