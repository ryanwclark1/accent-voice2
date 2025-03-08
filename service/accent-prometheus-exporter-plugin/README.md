# accent-prometheus-exporter-plugin

Adds `/metrics` to the accent-auth service as well as Asterisk and Nginx

## Installation

```sh
accent-plugind-cli -c "install git https://github.com/ryanwclark1/accent-prometheus-exporter-plugin"
```

## Metrics endpoints

* asterisk `/api/asterisk/metrics`
* nginx `/api/nginx/metrics`
* rabbitmq `/api/rabbitmq/metrics`
* accent-auth `/api/auth/0.1/metrics`
* accent-calld `/api/calld/1.0/metrics`
* accent-chatd `/api/chatd/1.0/metrics`
* accent-dird `/api/dird/0.1/metrics`
* accent-sysconfd `/api/sysconfd/metrics`
