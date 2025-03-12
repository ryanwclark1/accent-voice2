#!/usr/bin/env bash

# List of service names
services=(
    access_feature endpoint_iax incall phone_number user agent endpoint_sccp infos pjsip_transport
    user_call_permission application endpoint_sip ingress_http queue user_external_app asterisk_file
    extension ivr queue_general user_line call_filter external_app line register_iax user_voicemail
    call_permission feature_extension line_extension sccp_general utils call_pickup features meeting
    schedule voicemail conference func_key meeting_authorization skill voicemail_general configuration
    func_key_template moh skill_rule voicemail_zonemessages context group outcall switchboard
    directory_profile iax_callnumberlimits paging tenant endpoint_custom iax_general parking_lot trunk
)

# Iterate over each service and delete the tests directory
for service in "${services[@]}"; do
    src_dir="./accent_dao/resources/$service/tests"

    if [ -d "$src_dir" ]; then
        rm -rf "$src_dir"
        echo "Deleted $src_dir"
    else
        echo "Skipping $service: No tests folder to delete"
    fi
done

echo "Cleanup complete!"
