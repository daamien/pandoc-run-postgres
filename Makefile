lint:
	pylint *.py

sample: sample.pdf

%.pdf: %.md
	pandoc --filter=pandoc_run_postgres.py $^ -o $@

docker_bash:
	docker run -it -v `pwd`:/pandoc --entrypoint=bash dalibo/pandocker:latest
