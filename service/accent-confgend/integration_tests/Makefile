ifeq ($(MANAGE_DB_DIR),)
	UPDATE_DB_TARGET=update-db-pull
else
	UPDATE_DB_TARGET=update-db-build
	POSTGRES_DOCKER=$(MANAGE_DB_DIR)/contribs/docker/accent-confd-db-test/Dockerfile
endif

test-setup: test-image egg-info update-db

test-image:
	docker build -t accentcommunications/accent-confgend ..
	docker build --no-cache -t accentcommunications/accent-confgend-tests -f docker/Dockerfile-confgend ..

update-db: $(UPDATE_DB_TARGET)

update-db-pull:
	docker pull accentcommunications/accent-confd-db-test
	docker tag accentcommunications/accent-confd-db-test:latest accentcommunications/accent-confd-db-test:local

update-db-build:
	docker build --no-cache -t accentcommunications/accent-confd-db-test:local -f $(POSTGRES_DOCKER) $(MANAGE_DB_DIR)

egg-info:
	cd .. && python3 setup.py egg_info

test:
	pytest

.PHONY: test-setup test test-image egg-info update-db update-db-pull update-db-build
