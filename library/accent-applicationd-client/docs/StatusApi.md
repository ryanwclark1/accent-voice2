# accent_applicationd_client.StatusApi

All URIs are relative to *<http://localhost>*

Method | HTTP request | Description
------------- | ------------- | -------------
[**status_status_get**](StatusApi.md#status_status_get) | **GET** /status | Status

# **status_status_get**
>
> Status status_status_get()

Status

### Example

```python
from __future__ import print_function
import time
import accent_applicationd_client
from accent_applicationd_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_applicationd_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with accent_applicationd_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = accent_applicationd_client.StatusApi(api_client)

    try:
        # Status
        api_response = api_instance.status_status_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling StatusApi->status_status_get: %s\n" % e)
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**Status**](Status.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
