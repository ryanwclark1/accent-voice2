test-setup: egg-info build-dird build-db-image build-ws-mock-image

build-dird:
	docker build -t accentcommunications/accent-dird ..
	docker build --no-cache -t accent-dird-test -f docker/accent-dird-test.Dockerfile ..

build-db-image:
	docker build --pull -f ../contribs/docker/accent-dird-db.Dockerfile -t accentcommunications/accent-dird-db:local ..

build-ws-mock-image:
	docker build -f docker/accent-dird-ws-mock.Dockerfile -t accentcommunications/accent-dird-ws-mock:local .

egg-info:
	cd .. && python3 setup.py egg_info
	cd docker/broken-plugins && python3 setup.py egg_info

test:
	pytest

.PHONY: test-setup build-dird build-db-image egg-info test
