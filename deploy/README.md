# accent-docker

Contains docker compose file to setup Accent Voice project

## Prerequisite

* Install docker and docker compose
* Clone the following repositories
    * accentcommunications/accent-auth-keys
    * accentcommunications/accent-webhookd
    * accentcommunications/accent-config
    * accentcommunications/accent-manage-db
* set environment variable `LOCAL_GIT_REPOS=<path/to/cloned/repositories>`

## Prepare Environment

* `for repo in accent-config accent-webhookd accent-auth-keys accent-manage-db; do git -C "$LOCAL_GIT_REPOS/$repo" pull; done`
* `docker compose pull --ignore-pull-failures`
* `docker compose build --pull`

## Start Environment

* `docker compose up --detach`
* Need to accept custom certificate on `https://localhost:8443`
* default username / password: `root` / `secret`

## Clean Environment

* `docker compose down --volumes`
* `docker compose up --detach`

## Restart Environment  ```````````````````

* `docker compose down`
* `docker compose up --detach`

## Test Environment

* Install `curl` and `jq` commands
* `./verify.sh`

## Troubleshooting

* To get sql prompt: `docker compose exec postgres psql -U asterisk accent`
* To use accent-auth-cli: `docker compose run --entrypoint bash bootstrap`
* To update only one service without restarting everything

  ```
  docker compose stop webhookd
  docker compose rm webhookd
  docker compose up webhookd
  ```

* **Avoid to use `docker compose restart <service>`**. It will only restart container without new
  parameters (mount, config, variable)

* When running softphone on the same host than docker, don't use 127.0.0.1:5060, but use *public* IP
  (i.e. 192.168.x.x:5060)


ENV ASTERISK_APPS = \
    --included app_agent_pool \
    --included app_authenticate \
    --included app_bridgeaddchan \
    --included app_bridgewait \
    --included app_cdr \
    --included app_celgenuserevent \
    --included app_channelredirect \
    --included app_chanspy \
    --included app_confbridge \
    --included app_controlplayback \
    --included app_db \
    --included app_dial \
    --included app_directed_pickup \
    --included app_directory \
    --included app_disa \
    --included app_dumpchan \
    --included app_echo \
    --included app_exec \
    --included app_flash \
    --included app_followme \
    --included app_forkcdr \
    --included app_milliwatt \
    --included app_mixmonitor \
    --included app_originate \
    --included app_page \
    --included app_playback \
    --included app_playtones \
    --included app_privacy \
    --included app_queue \
    --included app_read \
    --included app_readexten \
    --included app_record \
    --included app_sayunixtime \
    --included app_senddtmf \
    --included app_sendtext \
    # --included app_skel \
    --included app_softhangup \
    --included app_speech_utils \
    --included app_stack \
    --included app_stasis \
    --included app_stream_echo \
    --included app_system \
    --included app_talkdetect \
    --included app_transfer \
    --included app_userevent \
    --included app_verbose \
    --included app_voicemail \
    --included app_voicemail_imap \
    --included app_voicemail_odbc \
    --included app_waituntil \
    --included app_while \
    --included app_alarmreceiver \
    --included app_amd \
    --included app_attended_transfer \
    --included app_audiosocket \
    --included app_blind_transfer \
    --included app_chanisavail \
    --included app_dictate \
    --included app_dtmfstore \
    --included app_externalivr \
    --included app_festival \
    # --included app_ivrdemo \
    --included app_jack \
    --included app_meetme \
    --included app_mf \
    --included app_minivm \
    --included app_morsecode \
    --included app_mp3 \
    --included app_osplookup \
    --included app_reload \
    # --included app_saycounted \
    --included app_sf \
    --included app_sms \
    --included app_statsd \
    --included app_test \
    --included app_waitforcond \
    --included app_waitforring \
    --included app_waitforsilence \
    --included app_zapateller \
    --included app_adsiprog \
    --included app_dahdiras \
    # --included app_fax \
    --included app_getcpeid \
    --included app_ices \
    --included app_image \
    # --included app_macro \
    --included app_nbscat \
    --included app_url \



### DNS/TRAEFIK ###
Browser throws ERR_TOO_MANY_REDIRECTS when accessing a service: If you deployed using CloudFlare's DNS servers and set CF to 'Flexible mode' then you will incurr in this error. This is because you have https from the client to the CF proxy, and forced http between the CF proxy and the server (forced by CF). As Traefik was configured with an http-to-https redirection itself, this will cause an infinite loop of redirects. In order to solve this issue, you need to set CF to Full encryption mode, and even without LE (using Traefik's self signed certificate) your website/application is now accessible.

Traefik Basic Auth

# Note: when used in docker-compose.yml all dollar signs in the hash need to be doubled for escaping.
# To create user:password pair, it's possible to use this command:
# echo $(htpasswd -nB user) | sed -e s/\\$/\\$\\$/g