MANAGE_DB_DIR ?= ../../accent-manage-db/
CEL_POSTGRES_DOCKER=$(MANAGE_DB_DIR)/contribs/docker/accent-confd-db-test/Dockerfile

test-setup: egg-info call-logd purge-db db

egg-info:
	cd .. && python setup.py egg_info

test:
	pytest

purge-db:
	docker build --no-cache -t accent-purge-db-test -f docker/Dockerfile-purge-db-test ..

call-logd:
	docker build -t accentcommunications/accent-call-logd ..
	docker build --no-cache -t accent-call-logd-test -f docker/Dockerfile-call-logd-test ..

cel-db:
	docker build --no-cache -t accentcommunications/accent-confd-db-test -f $(CEL_POSTGRES_DOCKER) $(MANAGE_DB_DIR)

db:
	docker build -f ../contribs/docker/Dockerfile-db -t accentcommunications/accent-call-logd-db ..

.PHONY: test-setup test call-logd purge-db cel-db db
