
all: setup start_dev_db build_api_docker start_api_docker

start: all

destroy: destroy_dev_db destroy_api_docker

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

build_api_docker:
	./scripts/api/docker_build.sh


start_api_docker:
	./scripts/api/docker_run.sh

destroy_api_docker:
	./scripts/api/docker_kill.sh


run_server:
	export FLASK_APP="api:create_app()"
	export FLASK_RUN_PORT=5100
	echo $(FLASK_APP)
	venv/bin/flask run


deploy:
	./scripts/deploy.sh


test:
	./scripts/run_tests
