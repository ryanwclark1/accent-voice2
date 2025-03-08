# Administration

The oldest call logs are periodically removed by `accent-purge-db`.

## Manual Generation

Call logs can also be generated manually. To do so, log on to the target
Accent server and run:

    accent-call-logs

To avoid running for too long in one time, the call logs generation is
limited to the `n` last unprocessed CEL entries (default `20,000`). This
means that successive calls to `accent-call-logs` will process `n` more
CELs, making about `n/10` more calls available in call logs, going further
back in history, while processing new calls as well.

You can specify the number of CEL entries to consider. For example, to
generate calls using the `100,000` last unprocessed CEL entries:

    accent-call-logs -c 100000

## Regeneration of call logs

Since call logs are based on CEL, they can be deleted and generated
without problems. To regenerate the last month of call logs:

    accent-call-logs delete -d 30
    accent-call-logs generate -d 30  // the default behavior of accent-call-logs command is `generate`

## Technicals

Call logs are pre-generated from CEL entries. The generation is done
automatically by `accent-call-logd`. accent-call-logs is also run nightly to
generate call logs from CEL that were missed by `accent-call-logd`.
