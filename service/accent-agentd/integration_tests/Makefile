MANAGE_DB_DIR ?= ../../accent-manage-db/
POSTGRES_DOCKER=$(MANAGE_DB_DIR)/contribs/docker/accent-confd-db-test/Dockerfile

test-setup: egg-info agentd agentd-test

test:
	pytest -x

egg-info:
	cd .. && python setup.py egg_info

agentd:
	docker build -t accentcommunications/accent-agentd ..

agentd-test: egg-info
	docker build --no-cache -t accent-agentd-test -f Dockerfile-agentd ..

db:
	docker build --no-cache -t accentcommunications/accent-confd-db-test -f $(POSTGRES_DOCKER) $(MANAGE_DB_DIR)

.PHONY: test-setup test egg-info agentd agentd-test db
