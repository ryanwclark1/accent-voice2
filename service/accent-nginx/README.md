accent-nginx
==========

# Logs

The default Accent log format add additional information about
response time and status.

```
log_format main
    '$remote_addr - $remote_user [$time_local] "$request" '
    '$status $body_bytes_sent "$http_referer" "$http_user_agent" "$sent_http_x_powered_by" '
    '$request_length $msec $request_time $upstream_addr '
    '$upstream_response_length $upstream_response_time $upstream_status';
```

| Placeholder               | Description                                                       |
|---------------------------|-------------------------------------------------------------------|
| $remote_addr              | the source IP address of the client                               |
| $remote_user              | user name supplied with the Basic authentication                  |
| $time_local               | local time in the Common Log Format                               |
| $request                  | full original request line                                        |
| $status                   | response status                                                   |
| $body_bytes_sent          | number of body bytes sent to a client                             |
| $http_referer             | value of the Referer header                                       |
| $http_user_agent          | value of User-Agent header                                        |
| $sent_http_x_powered_by   | service name                                                      |
| $request_length           | request length (including request line, header, and request body) |
| $mesc                     | time in seconds with a milliseconds at the time of the log write  |
| $request_time             | request processing time in seconds with a milliseconds resolution |
| $upstream_addr            | the IP address and port of the upstream server                    |
| $upstream_response_length | the length of the response obtained from the upstream server      |
| $upstream_response_time   | time spent on receiving the response from the upstream server     |
| $upstream_status          | status code of the response obtained from the upstream server     |

## GoAccess log format

Logs can be analyzed with [GoAccess](https://goaccess.io) using the following
time, date and log format :

```
time-format %H:%M:%S

date-format %d/%b/%Y

log-format %h %^ %e [%d:%t %^] "%r" %s %b "%R" "%u" "%^" %^ %^ %^ %v %^ %T %^
```

Live report command line example :

```
goaccess --real-time-html --date-format '%d/%b/%Y' --time-format '%H:%M:%S' \
  --log-format '%h %^ %e [%d:%t %^] "%r" %s %b "%R" "%u" "%^" %^ %^ %^ %v %^ %T %^' \
  /var/log/nginx/accent.access.log
```
