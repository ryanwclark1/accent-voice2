test-setup: build-ui egg-info

build-ui:
	docker build -t accentcommunications/accent-ui ..
	docker build --no-cache -t accent-ui-test -f Dockerfile ..

egg-info:
	cd .. && python setup.py egg_info

test:
	pytest

.PHONY: test-setup test build-ui egg-info
