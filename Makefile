lint:
	pylint *.py

sample: sample.pdf

%.pdf: %.md
	pandoc --filter=pandoc_run_postgres.py $^ -o $@


tests/output/run_postgres_tag.md: tests/input/run_postgres_tag.md
tests/output/sample.md: sample.md
tests/output/sql_formatting.md: tests/input/sql_formatting.md

tests/output/run_postgres_tag.md tests/output/sample.md tests/output/sql_formatting.md:
	pandoc --filter=pandoc_run_postgres.py $^ -o $@

docker_bash:
	docker run -it -v `pwd`:/pandoc --entrypoint=bash dalibo/pandocker:latest

.PHONY: tests
tests: tests/output/sql_formatting.md tests/output/sample.md tests/output/run_postgres_tag.md
	diff tests/output tests/expected
