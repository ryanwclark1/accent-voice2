{% if exten_voicemail -%}
prgkey1 type: speeddial
prgkey1 value: {{ exten_voicemail }}
{% endif -%}

{% if exten_fwd_unconditional -%}
prgkey2 type: speeddial
prgkey2 value: {{ exten_fwd_unconditional }}
{% endif -%}

{% if exten_dnd -%}
prgkey3 type: speeddial
prgkey3 value: {{ exten_dnd }}
{% endif -%}

{% if exten_pickup_call -%}
prgkey4 type: speeddial
prgkey4 value: {{ exten_pickup_call }}
{% endif -%}

prgkey5 type: services

prgkey6 type: none

prgkey7 type: none

{% if XX_accent_phonebook_url -%}
prgkey8 type: xml
prgkey8 value: {{ XX_accent_phonebook_url }}
{% endif -%}

{% include 'base.tpl' %}
