{% extends 'base.tpl' -%}

{% block gui_fkey %}{% endblock %}

{% block settings_suffix %}
{% if XX_accent_phonebook_url -%}
<gui_fkey1 perm="R">keyevent F_NONE</gui_fkey1>
% else -%}
<gui_fkey1 perm="R">keyevent F_ADR_BOOK</gui_fkey1>
{% endif -%}
{% endblock %}
