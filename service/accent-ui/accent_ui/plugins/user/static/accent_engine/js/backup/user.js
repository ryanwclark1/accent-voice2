$(document).ready(function() {
  create_list_table();
  init_add_available_extensions.call(this);
  init_toggle_template_disable.call(this);

  // Remove spaces in email
  var removeSpace = function() {
    $(this).val($(this).val().replace(/\s/g, ''));
  };
  $(".modal-content #email, #user #username").on("input", removeSpace);

  $('.row-template').on("row:cloned", function (e, row) {
    init_add_available_extensions.call(row);
    init_toggle_template_disable.call(row);
  });

  $('.row-line').each(function (e, row) {
    add_available_extensions.call(row);
    toggle_template_disable.call(row);
  });

  toggle_busy_destination_validator();
  $('#forwards-busy-enabled').change(toggle_busy_destination_validator);
  toggle_noanswer_destination_validator();
  $('#forwards-noanswer-enabled').change(toggle_noanswer_destination_validator);
  toggle_unconditional_destination_validator();
  $('#forwards-unconditional-enabled').change(toggle_unconditional_destination_validator);

  // Handle destination selects
  $('select[data-listing-href]').each(function () {
    const $select = $(this);
    const listingUrl = $select.data('listing-href');
    const id = $select.val();

    if (!listingUrl) return;

    $.ajax({ url: listingUrl }).done(function (data) {
      $select.empty();
      data.results.forEach(result => {
        $select.append(new Option(result.text, result.id));
      });
      $select.val(id);
    });
  });
});

function create_list_table() {
  const tableConfig = {
    columns: [
      { data: 'firstname' },
      { data: 'lastname' },
      { data: 'email' },
      { data: 'extension' },
      { data: 'provisioning_code' },
    ]
  };
  create_table_serverside(tableConfig);
}

function toggle_busy_destination_validator() {
  $('#forwards-busy-destination').prop('required', $('#forwards-busy-enabled').is(":checked"));
}

function toggle_noanswer_destination_validator() {
  $('#forwards-noanswer-destination').prop('required', $('#forwards-noanswer-enabled').is(":checked"));
}

function toggle_unconditional_destination_validator() {
  $('#forwards-unconditional-destination').prop('required', $('#forwards-unconditional-enabled').is(":checked"));
}

function init_add_available_extensions() {
  $('.line-context', this).on("select2:select", add_available_extensions);
  add_available_extensions();
}

function add_available_extensions() {
  const context = $(".line-context").val();
  const $extension = $(".line-extension");
  const ajaxUrl = $extension.data('listing-href');

  if (!ajaxUrl) return;

  $extension.select2({
    allowClear: true,
    placeholder: 'Select...',
    tags: true,
    ajax: {
      url: ajaxUrl,
      data: params => ({ term: params.term, context })
    }
  });
}

function init_toggle_template_disable() {
  $('.line-protocol', this).on("select2:select", toggle_template_disable);
  toggle_template_disable();
}

function toggle_template_disable() {
  const $protocol = $(".line-protocol");
  const $template = $(".line-template");

  $template.prop('disabled', $protocol.val() !== 'sip');
}