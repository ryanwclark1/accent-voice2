.PHONY: test-setup egg-info test

test-setup: egg-info
	docker build --pull -t accentcommunications/accent-websocketd ..
	docker build --no-cache -t accent-websocketd-test -f Dockerfile ..

egg-info:
	cd .. && python3 setup.py egg_info

test:
	pytest suite
