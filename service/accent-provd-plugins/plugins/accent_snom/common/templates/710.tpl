{% extends 'base.tpl' %}

{% block fkeys_prefix %}
{% if XX_accent_phonebook_url %}
<fkey idx="4" context="active" perm="R">url {{ XX_accent_phonebook_url|e }}</fkey>
{% endif %}
{% endblock %}
