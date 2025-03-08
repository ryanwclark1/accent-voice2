egg-info:
	(cd .. && python setup.py egg_info)

test-setup: egg-info test-image

test-image:
	docker build -t accentcommunications/accent-purge-db ..
	docker build --no-cache -t accent-purge-db-test -f Dockerfile ..

test:
	docker-compose run sync
	docker-compose run purgedb
	# Let time to container to stop
	sleep 2
	docker-compose kill
	docker-compose rm -f

.PHONY: test test-image test-setup egg-info
