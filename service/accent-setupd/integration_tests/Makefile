test-setup: egg-info setupd setupd-test deployd webhookd

test:
	pytest -x

egg-info:
	cd .. && python setup.py egg_info

setupd:
	docker build -t accentcommunications/accent-setupd ..

setupd-test: egg-info
	docker build --no-cache -t accent-setupd-test -f Dockerfile-setupd ..

deployd:
	docker build -t accentcommunications/accent-deployd-mock -f docker/accent-deployd-mock/Dockerfile docker/accent-deployd-mock

webhookd:
	docker build -t accentcommunications/accent-webhookd-mock -f docker/accent-webhookd-mock/Dockerfile docker/accent-webhookd-mock

.PHONY: test-setup test egg-info setupd setupd-test deployd webhookd
