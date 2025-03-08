test-setup: egg-info webhookd webhookd-test db

test:
	pytest -x

egg-info:
	cd .. && python setup.py egg_info
	cd plugins/sentinel && python setup.py egg_info

webhookd:
	docker build -t accentcommunications/accent-webhookd ..

webhookd-test: webhookd egg-info
	docker build --no-cache -t accent-webhookd-test -f Dockerfile ..

db:
	docker build -f ../contribs/docker/Dockerfile-db -t accentcommunications/accent-webhookd-db:local ..

.PHONY: test-setup test egg-info webhookd webhookd-test db
