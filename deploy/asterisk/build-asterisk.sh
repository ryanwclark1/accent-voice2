#!/usr/bin/env bash

PROGNAME=$(basename $0)

if test -z ${ASTERISK_VERSION}; then
  echo "${PROGNAME}: ASTERISK_VERSION required" >&2
  exit 1
fi

if test -z ${GITHUB_TOKEN}; then
  echo "${PROGNAME}: GITHUB_TOKEN required" >&2
  exit 1
fi

set -ueo pipefail

USER='asterisk'

adduser --quiet --system --group --no-create-home \
  --home /var/lib/asterisk \
  --gecos "Asterisk PBX daemon" \
  $USER

for group in dialout audio; do
  if groups $USER | grep -w -q -v $group; then
    adduser --quiet $USER $group
  fi
done

echo "Asterisk User Created and Permissions Set"


DEBIAN_FRONTEND=noninteractive \
apt-get update -qq && \
apt-get install --yes -qq --no-install-recommends \
  apt-utils \
  bzip2 \
  ca-certificates \
  curl \
  g++ \
  gcc \
  libasound2-dev \
  libc6-dev \
  libcodec2-dev \
  libcurl4-openssl-dev \
  libedit-dev \
  libgmime-3.0-dev \
  libiksemel-dev \
  libiksemel3 \
  liblua5.4-dev \
  libogg-dev \
  libpopt-dev \
  libpq-dev \
  libresample1-dev \
  libspandsp-dev \
  libspeex-dev \
  libspeexdsp-dev \
  libsqlite3-dev \
  libsrtp2-dev \
  libssl-dev \
  libunbound-dev \
  liburiparser-dev \
  libvorbis-dev \
  libxml2-dev \
  libxslt1-dev \
  make \
  openssl \
  patch \
  portaudio19-dev \
  rsync \
  sqlite3 \
  unixodbc \
  unixodbc-dev \
  uuid \
  uuid-dev \
  wget \
> /dev/null

echo "Debian Packages Installed"
mkdir -p /usr/src/asterisk
cd /usr/src/asterisk

( \
curl -L \
-H "Accept: application/vnd.github+json" \
-H "Authorization: Bearer ${GITHUB_TOKEN}" \
-H "X-GitHub-Api-Version: 2022-11-28" \
https://api.github.com/repos/ryanwclark1/accent-asterisk/tarball/${ASTERISK_VERSION}-patch | \
tar --strip-components 1 -xz
) &>/dev/null

echo "Asterisk Source Downloaded"

# 1.5 jobs per core works out okay
: ${JOBS:=$(( $(nproc) + $(nproc) / 2 ))}

./configure --with-jansson-bundled > /dev/null

make menuselect.makeopts

menuselect/menuselect \
  --enable app_agent_pool menuselect.makeopts \
  --enable app_authenticate menuselect.makeopts \
  --enable app_bridgeaddchan menuselect.makeopts \
  --enable app_bridgewait menuselect.makeopts \
  --enable app_cdr menuselect.makeopts \
  --enable app_celgenuserevent menuselect.makeopts \
  --enable app_channelredirect menuselect.makeopts \
  --enable app_chanspy menuselect.makeopts \
  --enable app_confbridge menuselect.makeopts \
  --enable app_controlplayback menuselect.makeopts \
  --enable app_db menuselect.makeopts \
  --enable app_dial menuselect.makeopts \
  --enable app_directed_pickup menuselect.makeopts \
  --enable app_directory menuselect.makeopts \
  --enable app_disa menuselect.makeopts \
  --enable app_dumpchan menuselect.makeopts \
  --enable app_echo menuselect.makeopts \
  --enable app_exec menuselect.makeopts \
  --enable app_followme menuselect.makeopts \
  --enable app_forkcdr menuselect.makeopts \
  --enable app_milliwatt menuselect.makeopts \
  --enable app_mixmonitor menuselect.makeopts \
  --enable app_originate menuselect.makeopts \
  --enable app_page menuselect.makeopts \
  --enable app_playback menuselect.makeopts \
  --enable app_playtones menuselect.makeopts \
  --enable app_privacy menuselect.makeopts \
  --enable app_queue menuselect.makeopts \
  --enable app_read menuselect.makeopts \
  --enable app_readexten menuselect.makeopts \
  --enable app_record menuselect.makeopts \
  --enable app_sayunixtime menuselect.makeopts \
  --enable app_senddtmf menuselect.makeopts \
  --enable app_sendtext menuselect.makeopts \
  --enable app_softhangup menuselect.makeopts \
  --enable app_speech_utils menuselect.makeopts \
  --enable app_stack menuselect.makeopts \
  --enable app_stasis menuselect.makeopts \
  --enable app_stream_echo menuselect.makeopts \
  --enable app_system menuselect.makeopts \
  --enable app_talkdetect menuselect.makeopts \
  --enable app_transfer menuselect.makeopts \
  --enable app_userevent menuselect.makeopts \
  --enable app_verbose menuselect.makeopts \
  --enable app_voicemail menuselect.makeopts \
  --enable app_voicemail_imap menuselect.makeopts \
  --enable app_waituntil menuselect.makeopts \
  --enable app_while menuselect.makeopts \
  --enable app_alarmreceiver menuselect.makeopts \
  --enable app_amd menuselect.makeopts \
  --enable app_attended_transfer menuselect.makeopts \
  --enable app_audiosocket menuselect.makeopts \
  --enable app_blind_transfer menuselect.makeopts \
  --enable app_broadcast menuselect.makeopts \
  --enable app_chanisavail menuselect.makeopts \
  --enable app_dictate menuselect.makeopts \
  --enable app_dtmfstore menuselect.makeopts \
  --enable app_externalivr menuselect.makeopts \
  --enable app_festival menuselect.makeopts \
  --enable app_if menuselect.makeopts \
  --enable app_jack menuselect.makeopts \
  --enable app_mf menuselect.makeopts \
  --enable app_minivm menuselect.makeopts \
  --enable app_morsecode menuselect.makeopts \
  --enable app_mp3 menuselect.makeopts \
  --enable app_reload menuselect.makeopts \
  --enable app_saycounted menuselect.makeopts \
  --enable app_sf menuselect.makeopts \
  --enable app_signal menuselect.makeopts \
  --enable app_sms menuselect.makeopts \
  --enable app_statsd menuselect.makeopts \
  --enable app_test menuselect.makeopts \
  --enable app_waitforcond menuselect.makeopts \
  --enable app_waitforring menuselect.makeopts \
  --enable app_waitforsilence menuselect.makeopts \
  --enable app_zapateller menuselect.makeopts \
  --enable bridge_builtin_features menuselect.makeopts \
  --enable bridge_builtin_interval_features menuselect.makeopts \
  --enable bridge_holding menuselect.makeopts \
  --enable bridge_native_rtp menuselect.makeopts \
  --enable bridge_simple menuselect.makeopts \
  --enable bridge_softmix menuselect.makeopts \
  --enable cdr_adaptive_odbc menuselect.makeopts \
  --enable cdr_custom menuselect.makeopts \
  --enable cdr_manager menuselect.makeopts \
  --enable cdr_csv menuselect.makeopts \
  --enable cdr_odbc menuselect.makeopts \
  --enable cdr_pgsql menuselect.makeopts \
  --enable cdr_radius menuselect.makeopts \
  --enable cdr_sqlite3_custom menuselect.makeopts \
  --enable cel_custom menuselect.makeopts \
  --enable cel_manager menuselect.makeopts \
  --enable cel_odbc menuselect.makeopts \
  --enable cel_pgsql menuselect.makeopts \
  --enable cel_radius menuselect.makeopts \
  --enable cel_sqlite3_custom menuselect.makeopts \
  --enable chan_bridge_media menuselect.makeopts \
  --enable chan_iax2 menuselect.makeopts \
  --enable chan_motif menuselect.makeopts \
  --enable chan_pjsip menuselect.makeopts \
  --enable chan_rtp menuselect.makeopts \
  --enable chan_audiosocket menuselect.makeopts \
  --enable chan_console menuselect.makeopts \
  --enable chan_unistim menuselect.makeopts \
  --enable codec_a_mu menuselect.makeopts \
  --enable codec_adpcm menuselect.makeopts \
  --enable codec_alaw menuselect.makeopts \
  --enable codec_codec2 menuselect.makeopts \
  --enable codec_g722 menuselect.makeopts \
  --enable codec_g726 menuselect.makeopts \
  --enable codec_gsm menuselect.makeopts \
  --enable codec_ilbc menuselect.makeopts \
  --enable codec_lpc10 menuselect.makeopts \
  --enable codec_resample menuselect.makeopts \
  --enable codec_speex menuselect.makeopts \
  --enable codec_ulaw menuselect.makeopts \
  --enable codec_opus menuselect.makeopts \
  --enable format_g719 menuselect.makeopts \
  --enable format_g723 menuselect.makeopts \
  --enable format_g726 menuselect.makeopts \
  --enable format_g729 menuselect.makeopts \
  --enable format_gsm menuselect.makeopts \
  --enable format_h263 menuselect.makeopts \
  --enable format_h264 menuselect.makeopts \
  --enable format_ilbc menuselect.makeopts \
  --enable format_ogg_vorbis menuselect.makeopts \
  --enable format_pcm menuselect.makeopts \
  --enable format_siren14 menuselect.makeopts \
  --enable format_siren7 menuselect.makeopts \
  --enable format_sln menuselect.makeopts \
  --enable format_wav menuselect.makeopts \
  --enable format_wav_gsm menuselect.makeopts \
  --enable format_ogg_speex menuselect.makeopts \
  --enable format_vox menuselect.makeopts \
  --enable func_aes menuselect.makeopts \
  --enable func_base64 menuselect.makeopts \
  --enable func_blacklist menuselect.makeopts \
  --enable func_callcompletion menuselect.makeopts \
  --enable func_callerid menuselect.makeopts \
  --enable func_cdr menuselect.makeopts \
  --enable func_channel menuselect.makeopts \
  --enable func_config menuselect.makeopts \
  --enable func_curl menuselect.makeopts \
  --enable func_cut menuselect.makeopts \
  --enable func_db menuselect.makeopts \
  --enable func_devstate menuselect.makeopts \
  --enable func_dialgroup menuselect.makeopts \
  --enable func_dialplan menuselect.makeopts \
  --enable func_enum menuselect.makeopts \
  --enable func_env menuselect.makeopts \
  --enable func_extstate menuselect.makeopts \
  --enable func_global menuselect.makeopts \
  --enable func_groupcount menuselect.makeopts \
  --enable func_hangupcause menuselect.makeopts \
  --enable func_holdintercept menuselect.makeopts \
  --enable func_iconv menuselect.makeopts \
  --enable func_jitterbuffer menuselect.makeopts \
  --enable func_lock menuselect.makeopts \
  --enable func_logic menuselect.makeopts \
  --enable func_math menuselect.makeopts \
  --enable func_md5 menuselect.makeopts \
  --enable func_module menuselect.makeopts \
  --enable func_odbc menuselect.makeopts \
  --enable func_periodic_hook menuselect.makeopts \
  --enable func_pjsip_aor menuselect.makeopts \
  --enable func_pjsip_contact menuselect.makeopts \
  --enable func_pjsip_endpoint menuselect.makeopts \
  --enable func_presencestate menuselect.makeopts \
  --enable func_rand menuselect.makeopts \
  --enable func_realtime menuselect.makeopts \
  --enable func_sha1 menuselect.makeopts \
  --enable func_shell menuselect.makeopts \
  --enable func_sorcery menuselect.makeopts \
  --enable func_speex menuselect.makeopts \
  --enable func_sprintf menuselect.makeopts \
  --enable func_srv menuselect.makeopts \
  --enable func_strings menuselect.makeopts \
  --enable func_sysinfo menuselect.makeopts \
  --enable func_talkdetect menuselect.makeopts \
  --enable func_timeout menuselect.makeopts \
  --enable func_uri menuselect.makeopts \
  --enable func_version menuselect.makeopts \
  --enable func_vmcount menuselect.makeopts \
  --enable func_volume menuselect.makeopts \
  --enable func_evalexten menuselect.makeopts \
  --enable func_export menuselect.makeopts \
  --enable func_frame_drop menuselect.makeopts \
  --enable func_frame_trace menuselect.makeopts \
  --enable func_json menuselect.makeopts \
  --enable func_pitchshift menuselect.makeopts \
  --enable func_sayfiles menuselect.makeopts \
  --enable func_scramble menuselect.makeopts \
  --enable pbx_config menuselect.makeopts \
  --enable pbx_loopback menuselect.makeopts \
  --enable pbx_spool menuselect.makeopts \
  --enable pbx_ael menuselect.makeopts \
  --enable pbx_dundi menuselect.makeopts \
  --enable pbx_lua menuselect.makeopts \
  --enable pbx_realtime menuselect.makeopts \
  --enable res_agi menuselect.makeopts \
  --enable res_ari menuselect.makeopts \
  --enable res_ari_applications menuselect.makeopts \
  --enable res_ari_asterisk menuselect.makeopts \
  --enable res_ari_bridges menuselect.makeopts \
  --enable res_ari_channels menuselect.makeopts \
  --enable res_ari_device_states menuselect.makeopts \
  --enable res_ari_endpoints menuselect.makeopts \
  --enable res_ari_events menuselect.makeopts \
  --enable res_ari_mailboxes menuselect.makeopts \
  --enable res_ari_model menuselect.makeopts \
  --enable res_ari_playbacks menuselect.makeopts \
  --enable res_ari_recordings menuselect.makeopts \
  --enable res_ari_sounds menuselect.makeopts \
  --enable res_clialiases menuselect.makeopts \
  --enable res_clioriginate menuselect.makeopts \
  --enable res_config_curl menuselect.makeopts \
  --enable res_config_odbc menuselect.makeopts \
  --enable res_config_sqlite3 menuselect.makeopts \
  --enable res_convert menuselect.makeopts \
  --enable res_crypto menuselect.makeopts \
  --enable res_curl menuselect.makeopts \
  --enable res_fax menuselect.makeopts \
  --enable res_format_attr_celt menuselect.makeopts \
  --enable res_format_attr_g729 menuselect.makeopts \
  --enable res_format_attr_h263 menuselect.makeopts \
  --enable res_format_attr_h264 menuselect.makeopts \
  --enable res_format_attr_ilbc menuselect.makeopts \
  --enable res_format_attr_opus menuselect.makeopts \
  --enable res_format_attr_silk menuselect.makeopts \
  --enable res_format_attr_siren14 menuselect.makeopts \
  --enable res_format_attr_siren7 menuselect.makeopts \
  --enable res_format_attr_vp8 menuselect.makeopts \
  --enable res_geolocation menuselect.makeopts \
  --enable res_http_media_cache menuselect.makeopts \
  --enable res_http_post menuselect.makeopts \
  --enable res_http_websocket menuselect.makeopts \
  --enable res_limit menuselect.makeopts \
  --enable res_manager_devicestate menuselect.makeopts \
  --enable res_manager_presencestate menuselect.makeopts \
  --enable res_musiconhold menuselect.makeopts \
  --enable res_mutestream menuselect.makeopts \
  --enable res_mwi_devstate menuselect.makeopts \
  --enable res_mwi_external menuselect.makeopts \
  --enable res_mwi_external_ami menuselect.makeopts \
  --enable res_odbc menuselect.makeopts \
  --enable res_odbc_transaction menuselect.makeopts \
  --enable res_parking menuselect.makeopts \
  --enable res_pjproject menuselect.makeopts \
  --enable res_pjsip menuselect.makeopts \
  --enable res_pjsip_acl menuselect.makeopts \
  --enable res_pjsip_authenticator_digest menuselect.makeopts \
  --enable res_pjsip_caller_id menuselect.makeopts \
  --enable res_pjsip_config_wizard menuselect.makeopts \
  --enable res_pjsip_dialog_info_body_generator menuselect.makeopts \
  --enable res_pjsip_diversion menuselect.makeopts \
  --enable res_pjsip_dlg_options menuselect.makeopts \
  --enable res_pjsip_dtmf_info menuselect.makeopts \
  --enable res_pjsip_empty_info menuselect.makeopts \
  --enable res_pjsip_endpoint_identifier_anonymous menuselect.makeopts \
  --enable res_pjsip_endpoint_identifier_ip menuselect.makeopts \
  --enable res_pjsip_endpoint_identifier_user menuselect.makeopts \
  --enable res_pjsip_exten_state menuselect.makeopts \
  --enable res_pjsip_geolocation menuselect.makeopts \
  --enable res_pjsip_header_funcs menuselect.makeopts \
  --enable res_pjsip_logger menuselect.makeopts \
  --enable res_pjsip_messaging menuselect.makeopts \
  --enable res_pjsip_mwi menuselect.makeopts \
  --enable res_pjsip_mwi_body_generator menuselect.makeopts \
  --enable res_pjsip_nat menuselect.makeopts \
  --enable res_pjsip_notify menuselect.makeopts \
  --enable res_pjsip_one_touch_record_info menuselect.makeopts \
  --enable res_pjsip_outbound_authenticator_digest menuselect.makeopts \
  --enable res_pjsip_outbound_publish menuselect.makeopts \
  --enable res_pjsip_outbound_registration menuselect.makeopts \
  --enable res_pjsip_path menuselect.makeopts \
  --enable res_pjsip_pidf_body_generator menuselect.makeopts \
  --enable res_pjsip_pidf_digium_body_supplement menuselect.makeopts \
  --enable res_pjsip_pidf_eyebeam_body_supplement menuselect.makeopts \
  --enable res_pjsip_publish_asterisk menuselect.makeopts \
  --enable res_pjsip_pubsub menuselect.makeopts \
  --enable res_pjsip_refer menuselect.makeopts \
  --enable res_pjsip_registrar menuselect.makeopts \
  --enable res_pjsip_rfc3326 menuselect.makeopts \
  --enable res_pjsip_rfc3329 menuselect.makeopts \
  --enable res_pjsip_sdp_rtp menuselect.makeopts \
  --enable res_pjsip_send_to_voicemail menuselect.makeopts \
  --enable res_pjsip_session menuselect.makeopts \
  --enable res_pjsip_sips_contact menuselect.makeopts \
  --enable res_pjsip_stir_shaken menuselect.makeopts \
  --enable res_pjsip_t38 menuselect.makeopts \
  --enable res_pjsip_transport_websocket menuselect.makeopts \
  --enable res_pjsip_xpidf_body_generator menuselect.makeopts \
  --enable res_realtime menuselect.makeopts \
  --enable res_resolver_unbound menuselect.makeopts \
  --enable res_rtp_asterisk menuselect.makeopts \
  --enable res_rtp_multicast menuselect.makeopts \
  --enable res_security_log menuselect.makeopts \
  --enable res_sorcery_astdb menuselect.makeopts \
  --enable res_sorcery_config menuselect.makeopts \
  --enable res_sorcery_memory menuselect.makeopts \
  --enable res_sorcery_memory_cache menuselect.makeopts \
  --enable res_sorcery_realtime menuselect.makeopts \
  --enable res_speech menuselect.makeopts \
  --enable res_srtp menuselect.makeopts \
  --enable res_stasis menuselect.makeopts \
  --enable res_stasis_answer menuselect.makeopts \
  --enable res_stasis_device_state menuselect.makeopts \
  --enable res_stasis_mailbox menuselect.makeopts \
  --enable res_stasis_playback menuselect.makeopts \
  --enable res_stasis_recording menuselect.makeopts \
  --enable res_stasis_snoop menuselect.makeopts \
  --enable res_stir_shaken menuselect.makeopts \
  --enable res_stun_monitor menuselect.makeopts \
  --enable res_timing_timerfd menuselect.makeopts \
  --enable res_xmpp menuselect.makeopts \
  --enable res_ael_share menuselect.makeopts \
  --enable res_audiosocket menuselect.makeopts \
  --enable res_calendar menuselect.makeopts \
  --enable res_calendar_caldav menuselect.makeopts \
  --enable res_calendar_ews menuselect.makeopts \
  --enable res_calendar_exchange menuselect.makeopts \
  --enable res_calendar_icalendar menuselect.makeopts \
  --enable res_chan_stats menuselect.makeopts \
  --enable res_cliexec menuselect.makeopts \
  --enable res_config_ldap menuselect.makeopts \
  --enable res_config_pgsql menuselect.makeopts \
  --enable res_corosync menuselect.makeopts \
  --enable res_endpoint_stats menuselect.makeopts \
  --enable res_fax_spandsp menuselect.makeopts \
  --enable res_hep menuselect.makeopts \
  --enable res_hep_pjsip menuselect.makeopts \
  --enable res_hep_rtcp menuselect.makeopts \
  --enable res_phoneprov menuselect.makeopts \
  --enable res_pjsip_aoc menuselect.makeopts \
  --enable res_pjsip_history menuselect.makeopts \
  --enable res_pjsip_phoneprov_provider menuselect.makeopts \
  --enable res_prometheus menuselect.makeopts \
  --enable res_smdi menuselect.makeopts \
  --enable res_snmp menuselect.makeopts \
  --enable res_statsd menuselect.makeopts \
  --enable res_timing_pthread menuselect.makeopts \
  --enable res_tonedetect menuselect.makeopts \
  --enable astcanary menuselect.makeopts \
  --enable astdb2sqlite3 menuselect.makeopts \
  --enable astdb2bdb menuselect.makeopts \
  --enable check_expr menuselect.makeopts \
  --enable smsq menuselect.makeopts \
  --enable CORE-SOUNDS-EN-GSM menuselect.makeopts \
  --enable EXTRA-SOUNDS-EN-GSM menuselect.makeopts \
  --enable MOH-OPSOUND-GSM menuselect.makeopts \
  --enable OPTIONAL_API menuselect.makeopts \
  --disable res_speech_aeap menuselect.makeopts \
  --disable res_aeap menuselect.makeopts \
  --disable app_voicemail_odbc menuselect.makeopts \
  --disable chan_dahdi menuselect.makeopts\
  --disable codec_dahdi menuselect.makeopts\
  --disable res_timing_dahdi menuselect.makeopts\
  --disable app_flash menuselect.makeopts\
  --disable cel_tds menuselect.makeopts \
  --disable cdr_tds menuselect.makeopts \
  --disable app_adsiprog menuselect.makeopts \
  --disable app_getcpeid menuselect.makeopts \
  --disable stereorize menuselect.makeopts \
  --disable streamplayer menuselect.makeopts \
  --disable res_adsi menuselect.makeopts \
  --disable check_expr2 menuselect.makeopts \
  --disable conf_bridge_binaural_hrir_importer menuselect.makeopts \
  --disable-category MENUSELECT_TESTS \
  --disable-category MENUSELECT_AGIS \


echo "Asterisk Configuration Selected"

make -j ${JOBS} all > /dev/null || make -j ${JOBS} all
make install

echo "Asterisk Installed"

make config
make samples

cp -r /usr/src/asterisk/include/* /usr/local/include

echo "Accent Asterisk Custom AMPQ"
cd /usr/src/accent-res-amqp
apt-get install --yes -qq --no-install-recommends \
  librabbitmq-dev \
  jq

cp /usr/src/accent-res-amqp/asterisk/* /usr/local/include/asterisk
cp /usr/src/accent-res-amqp/documentation/* /var/lib/asterisk/documentation/thirdparty

make DOCDIR=/var/lib/asterisk/documentation/thirdparty
make install
make samples

cd /usr/src/accent-res-stasis-amqp
cp /usr/src/accent-res-stasis-amqp/asterisk/* /usr/local/include/asterisk
cp /usr/src/accent-res-stasis-amqp/documentation/* /var/lib/asterisk/documentation/thirdparty

make DOCDIR=/var/lib/asterisk/documentation/thirdparty
make install
make samples


RESOURCES_FILENAME="/var/lib/asterisk/rest-api/resources.json"

if jq -r '.apis[] .path ' "${RESOURCES_FILENAME}" | grep -q '/api-docs/amqp'; then
    exit 0
fi

patched_resources_filename=$(mktemp)

jq '.apis[.apis | length] |= . + {"path": "/api-docs/amqp.{format}", "description": "AMQP resource"}' "${RESOURCES_FILENAME}" > "${patched_resources_filename}"
chmod 0644 "${patched_resources_filename}"
mv "${patched_resources_filename}" "${RESOURCES_FILENAME}"
cp amqp.json /var/lib/asterisk/rest-api

mkdir -p /usr/share/accent-res-stasis-amqp/
cp /usr/src/accent-res-stasis-amqp/bin/patch_ari_resources.sh /usr/share/accent-res-stasis-amqp/patch_ari_resources.sh


# Configure files and directories
mkdir -p /etc/asterisk/
mkdir -p /var/spool/asterisk/fax/
mkdir -p /usr/share/asterisk/conf/

chown -R asterisk:asterisk /etc/asterisk \
                           /var/*/asterisk \
                           /usr/*/asterisk

chmod -R 750 /var/spool/asterisk

mv /etc/asterisk/* /usr/share/asterisk/conf/
# mv /var/lib/asterisk/documentation /usr/share/asterisk/
mv /var/lib/asterisk/firmware /usr/share/asterisk/
mv /var/lib/asterisk/rest-api /usr/share/asterisk/
mv /var/lib/asterisk/static-http /usr/share/asterisk/
mv  /var/lib/asterisk/phoneprov /usr/share/asterisk/

cp -R --preserve=mode,ownership /var/lib/asterisk/documentation /usr/share/asterisk/
cp -R --preserve=mode,ownership /var/lib/asterisk/agi-bin /usr/share/asterisk/
cp -R --preserve=mode,ownership /var/lib/asterisk/keys /usr/share/asterisk/
cp -R --preserve=mode,ownership /var/lib/asterisk/sounds /usr/share/asterisk/
cp -Rrf --preserve=mode,ownership /etc/accent-asterisk-config/* /etc/asterisk

set runuser and rungroup
sed -i -E 's/^;(run)(user|group)/\1\2/' /etc/asterisk/asterisk.conf

ln -s /var/lib/asterisk/moh /usr/share/asterisk/

# ownerhip confirm for copy and ln
chown -R asterisk:asterisk /etc/asterisk \
                           /var/*/asterisk \
                           /usr/*/asterisk


echo "Cleaning Install"
cd /
rm -rf /usr/src/asterisk \
       /usr/src/codecs \
       /etc/accent-asterisk-config

# Remove all -dev Packages
DEVPKGS="$(dpkg -l | grep '\-dev' | awk '{print $2}' | xargs)"
apt-get --yes -qq purge \
  autoconf \
  build-essential \
  bzip2 \
  cpp \
  m4 \
  make \
  patch \
  perl \
  perl-modules \
  pkg-config \
  subversion \
  xz-utils \
  ${DEVPKGS} \
> /dev/null

# apt-get autoremove --yes > /dev/null
DEBIAN_FRONTEND=noninteractive \
apt-get purge --yes -qq > /dev/null
apt-get autoclean --yes > /dev/null
rm -rf /var/lib/apt/lists/*
rm tmp/*

echo "Finished Install"

exec rm -f /build-asterisk.sh
