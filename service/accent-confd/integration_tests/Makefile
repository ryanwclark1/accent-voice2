PROVD_DIR ?= ${LOCAL_GIT_REPOS}/accent-provd/

ifeq ($(MANAGE_DB_DIR),)
	UPDATE_DB_TARGET=update-db-pull
else
	UPDATE_DB_TARGET=update-db-build
	POSTGRES_DOCKER=$(MANAGE_DB_DIR)/contribs/docker/accent-confd-db-test/Dockerfile
endif

test-setup: egg-info build-confd update-db

build-confd:
	docker build -t accentcommunications/accent-confd ..
	docker build --no-cache -t accent-confd-test -f Dockerfile ..

update-db: $(UPDATE_DB_TARGET)

update-db-pull:
	docker pull accentcommunications/accent-confd-db-test
	docker tag accentcommunications/accent-confd-db-test:latest accentcommunications/accent-confd-db-test:local

update-db-build:
	docker build --pull --no-cache -t accentcommunications/accent-confd-db-test:local -f $(POSTGRES_DOCKER) $(MANAGE_DB_DIR)

build-provd:
	docker build -t accentcommunications/accent-provd $(PROVD_DIR)

test:
	pytest -x

egg-info:
	cd .. && python setup.py egg_info

.PHONY: test-setup test egg-info update-db update-db-build update-db-pull build-provd build-confd
