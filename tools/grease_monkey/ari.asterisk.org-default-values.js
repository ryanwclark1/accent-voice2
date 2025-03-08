// Copyright (C) 2023 Accent Communications


// ==UserScript==
// @name        ari.asterisk.org default values
// @namespace   http://accentservices.com
// @include     http://ari.asterisk.org/
// @version     1
// @grant       none
// ==/UserScript==

// Automatically set the URL and key for ari.asterisk.org
// You should change the URL and key below before using this script.

var my_key = 'accent:password';
var my_url = 'http://accent:5039/ari/api-docs/resources.json'

// We must change the values after Swagger is loaded, so register as a callback
// run when the page is done loading.
window.addEventListener ("load", loadSwaggerSpecs, false);

function loadSwaggerSpecs() {
    var url_input = document.getElementById('input_baseUrl');
    if (url_input.value == 'http://localhost:8088/ari/api-docs/resources.json') {
        url_input.value = my_url;
    }

    var key_input = document.getElementById('input_apiKey');
    if (key_input.value == '') {
        key_input.value = my_key;
    }

    // Force key input update

    // This also serves as a workaround a JS bug on ari.asterisk.org that does
    // not take into account the key if it was not input manually (e.g. by the
    // browser reloading the page. See
    // https://issues.asterisk.org/jira/browse/ASTERISK-26320.
    trigger_onchange(key_input);

    var explore_button = document.getElementById('explore');
    explore_button.click();
}

function trigger_onchange(element) {
    // Source: http://stackoverflow.com/questions/2856513/how-can-i-trigger-an-onchange-event-manually
    if ("createEvent" in document) {
        var evt = document.createEvent("HTMLEvents");
        evt.initEvent("change", false, true);
        element.dispatchEvent(evt);
    } else {
        element.fireEvent("onchange");
    }
}
