<?xml version="1.0" standalone="yes"?>
<flat-profile>

{% if admin_password is defined -%}
<Web_Login_Admin_Name>admin</Web_Login_Admin_Name>
<Web_Login_Admin_Password>{{ admin_password|e }}</Web_Login_Admin_Password>
{% endif -%}
{% if user_password is defined -%}
<Web_Login_Guest_Name>cisco</Web_Login_Guest_Name>
<Web_Login_Guest_Password>{{ user_password|e }}</Web_Login_Guest_Password>
{% endif -%}

{% if dns_enabled -%}
<Primary_DNS>{{ dns_ip }}</Primary_DNS>
{% endif -%}

{% if ntp_enabled -%}
<Primary_NTP_Server>{{ ntp_ip }}</Primary_NTP_Server>
{% endif -%}

{% if syslog_enabled -%}
<Syslog_Server>{{ syslog_ip }}:{{ syslog_port }}</Syslog_Server>
{% endif -%}

{% if vlan_enabled -%}
<Enable_VLAN>Yes</Enable_VLAN>
<VLAN_ID>{{ vlan_id }}</VLAN_ID>
{% if vlan_pc_port_id is defined -%}
<Enable_PC_Port_VLAN_Tagging>Yes</Enable_PC_Port_VLAN_Tagging>
<PC_Port_VLAN_ID>{{ vlan_pc_port_id }}</PC_Port_VLAN_ID>
{% endif -%}
{% endif -%}

{% block upgrade_rule -%}
{% endblock -%}

{% if exten_voicemail is defined -%}
<Voice_Mail_Number>{{ exten_voicemail }}</Voice_Mail_Number>
{% endif -%}
{% if exten_pickup_call is defined -%}
<Call_Pickup_Code>{{ exten_pickup_call }}</Call_Pickup_Code>
{% endif -%}
{% if exten_pickup_group is defined -%}
<Group_Call_Pickup_Code>{{ exten_pickup_group }}</Group_Call_Pickup_Code>
{% endif -%}


{% if '1' in sip_lines -%}
<Station_Name>{{ sip_lines['1']['display_name']|e }}</Station_Name>
{% endif -%}

<Language_Selection>{{ XX_language }}</Language_Selection>
<Locale>{{ XX_locale }}</Locale>
{{ XX_timezone }}

{% for line_no, line in sip_lines.items() %}
<Line_Enable_{{ line_no }}_>Yes</Line_Enable_{{ line_no }}_>
<Proxy_{{ line_no }}_>{{ line['proxy_ip'] }}:{{ line['proxy_port'] or sip_proxy_port or 5060}}</Proxy_{{ line_no }}_>
<Use_DNS_SRV_{{ line_no }}_>Yes</Use_DNS_SRV_{{ line_no }}_>
<Proxy_Fallback_Intvl_{{ line_no }}_>120</Proxy_Fallback_Intvl_{{ line_no }}_>
<Display_Name_{{ line_no }}_>{{ line['display_name']|e }}</Display_Name_{{ line_no }}_>
<User_ID_{{ line_no }}_>{{ line['username']|e }}</User_ID_{{ line_no }}_>
<Password_{{ line_no }}_>{{ line['password']|e }}</Password_{{ line_no }}_>
<Auth_ID_{{ line_no }}_>{{ line['auth_username']|e }}</Auth_ID_{{ line_no }}_>
{% set dtmf_mode = line['dtmf_mode'] or sip_dtmf_mode -%}
{% if dtmf_mode == 'RTP-in-band' -%}
<DTMF_Tx_Method_{{ line_no }}_>InBand</DTMF_Tx_Method_{{ line_no }}_>
{% elif dtmf_mode == 'RTP-out-of-band' -%}
<DTMF_Tx_Method_{{ line_no }}_>AVT</DTMF_Tx_Method_{{ line_no }}_>
{% elif dtmf_mode == 'SIP-INFO' -%}
<DTMF_Tx_Method_{{ line_no }}_>INFO</DTMF_Tx_Method_{{ line_no }}_>
{% else -%}
<DTMF_Tx_Method_{{ line_no }}_>Auto</DTMF_Tx_Method_{{ line_no }}_>
{% endif -%}
{% endfor -%}

{% block suffix %}{% endblock %}

<!-- Function keys definition SHOULD go before the line key definition if we
     want the line key definition to override the function key definition -->
{{ XX_fkeys }}

{% for line_no, line in sip_lines.items() %}
<Extension_{{ line_no }}_>{{ line_no }}</Extension_{{ line_no }}_>
<Short_Name_{{ line_no }}_>{{ line['number']|d('$USER') }}</Short_Name_{{ line_no }}_>
<Extended_Function_{{ line_no }}_></Extended_Function_{{ line_no }}_>
{% endfor %}

{% if XX_accent_phonebook_url -%}
<XML_Directory_Service_Name>{{ XX_directory_name }}</XML_Directory_Service_Name>
<XML_Directory_Service_URL>{{ XX_accent_phonebook_url|e }}</XML_Directory_Service_URL>
{% endif -%}
</flat-profile>
