# Sample commands for testing

Use the following commands the set the TOKEN and ACCENT_HOST environment variables before starting

    % export TOKEN="<your token>"
    % export ACCENT_HOST="<accent hostname>"


## Import

Use the following command to import the import.csv file.

    % curl -ki -X POST --header "X-Auth-Token: $TOKEN" --header 'Content-Type: text/csv; charset=utf-8' --header 'Accept: application/json' -d "$(cat import.csv)" "https://$ACCENT_HOST:9489/0.1/personal/import"

## Deleting all contacts

   % curl -ki -X DELETE --header "X-Auth-Token: $TOKEN" --header 'Accept: application/json' "https://$ACCENT_HOST:9489/0.1/personal"
