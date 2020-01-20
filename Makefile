

setup:
	rm -rf venv
	python3 -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt
	venv/bin/pip install -r requirements-dev.txt

start_dev_db:
	./scripts/dev_db/docker_run_mssql.sh
	./scripts/dev_db/initialise_db.sh

db_shell:
	./scripts/dev_db/db_shell.sh

destroy_dev_db:
	./scripts/dev_db/kill_db.sh

run_server:
	export FLASK_APP="api:create_app()"
	export FLASK_RUN_PORT=5100
	venv/bin/flask run

test:
	./scripts/run_tests
