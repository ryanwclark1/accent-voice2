# accent_applicationd_client.ApplicationApi

All URIs are relative to *<http://localhost>*

Method | HTTP request | Description
------------- | ------------- | -------------
[**call_answer10_applications_application_uuid_calls_call_id_answer_put**](ApplicationApi.md#call_answer10_applications_application_uuid_calls_call_id_answer_put) | **PUT** /1.0/applications/{application_uuid}/calls/{call_id}/answer | Call Answer
[**call_hangup10_applications_application_uuid_calls_call_id_delete**](ApplicationApi.md#call_hangup10_applications_application_uuid_calls_call_id_delete) | **DELETE** /1.0/applications/{application_uuid}/calls/{call_id} | Call Hangup
[**call_mute_start10_applications_application_uuid_calls_call_id_mute_start_post**](ApplicationApi.md#call_mute_start10_applications_application_uuid_calls_call_id_mute_start_post) | **POST** /1.0/applications/{application_uuid}/calls/{call_id}/mute/start | Call Mute Start
[**call_mute_stop10_applications_application_uuid_calls_call_id_mute_stop_post**](ApplicationApi.md#call_mute_stop10_applications_application_uuid_calls_call_id_mute_stop_post) | **POST** /1.0/applications/{application_uuid}/calls/{call_id}/mute/stop | Call Mute Stop
[**create_node_with_calls10_applications_application_uuid_nodes_node_name_post**](ApplicationApi.md#create_node_with_calls10_applications_application_uuid_nodes_node_name_post) | **POST** /1.0/applications/{application_uuid}/nodes/{node_name} | Create Node With Calls
[**register_application10_applications_application_name_post**](ApplicationApi.md#register_application10_applications_application_name_post) | **POST** /1.0/applications/{application_name} | Register Application

# **call_answer10_applications_application_uuid_calls_call_id_answer_put**
>
> object call_answer10_applications_application_uuid_calls_call_id_answer_put(application_uuid, call_id)

Call Answer

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
    api_instance = accent_applicationd_client.ApplicationApi(api_client)
    application_uuid = 'application_uuid_example' # str |
call_id = 'call_id_example' # str |

    try:
        # Call Answer
        api_response = api_instance.call_answer10_applications_application_uuid_calls_call_id_answer_put(application_uuid, call_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationApi->call_answer10_applications_application_uuid_calls_call_id_answer_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **application_uuid** | **str**|  |
 **call_id** | **str**|  |

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **call_hangup10_applications_application_uuid_calls_call_id_delete**
>
> object call_hangup10_applications_application_uuid_calls_call_id_delete(application_uuid, call_id)

Call Hangup

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
    api_instance = accent_applicationd_client.ApplicationApi(api_client)
    application_uuid = 'application_uuid_example' # str |
call_id = 'call_id_example' # str |

    try:
        # Call Hangup
        api_response = api_instance.call_hangup10_applications_application_uuid_calls_call_id_delete(application_uuid, call_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationApi->call_hangup10_applications_application_uuid_calls_call_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **application_uuid** | **str**|  |
 **call_id** | **str**|  |

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **call_mute_start10_applications_application_uuid_calls_call_id_mute_start_post**
>
> object call_mute_start10_applications_application_uuid_calls_call_id_mute_start_post(application_uuid, call_id)

Call Mute Start

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
    api_instance = accent_applicationd_client.ApplicationApi(api_client)
    application_uuid = 'application_uuid_example' # str |
call_id = 'call_id_example' # str |

    try:
        # Call Mute Start
        api_response = api_instance.call_mute_start10_applications_application_uuid_calls_call_id_mute_start_post(application_uuid, call_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationApi->call_mute_start10_applications_application_uuid_calls_call_id_mute_start_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **application_uuid** | **str**|  |
 **call_id** | **str**|  |

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **call_mute_stop10_applications_application_uuid_calls_call_id_mute_stop_post**
>
> object call_mute_stop10_applications_application_uuid_calls_call_id_mute_stop_post(application_uuid, call_id)

Call Mute Stop

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
    api_instance = accent_applicationd_client.ApplicationApi(api_client)
    application_uuid = 'application_uuid_example' # str |
call_id = 'call_id_example' # str |

    try:
        # Call Mute Stop
        api_response = api_instance.call_mute_stop10_applications_application_uuid_calls_call_id_mute_stop_post(application_uuid, call_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationApi->call_mute_stop10_applications_application_uuid_calls_call_id_mute_stop_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **application_uuid** | **str**|  |
 **call_id** | **str**|  |

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_node_with_calls10_applications_application_uuid_nodes_node_name_post**
>
> Node create_node_with_calls10_applications_application_uuid_nodes_node_name_post(application_uuid, node_name, request_body)

Create Node With Calls

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
    api_instance = accent_applicationd_client.ApplicationApi(api_client)
    application_uuid = 'application_uuid_example' # str |
node_name = 'node_name_example' # str |
request_body = ['request_body_example'] # list[str] |

    try:
        # Create Node With Calls
        api_response = api_instance.create_node_with_calls10_applications_application_uuid_nodes_node_name_post(application_uuid, node_name, request_body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationApi->create_node_with_calls10_applications_application_uuid_nodes_node_name_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **application_uuid** | **str**|  |
 **node_name** | **str**|  |
 **request_body** | [**list[str]**](str.md)|  |

### Return type

[**Node**](Node.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **register_application10_applications_application_name_post**
>
> Application register_application10_applications_application_name_post(application_name)

Register Application

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
    api_instance = accent_applicationd_client.ApplicationApi(api_client)
    application_name = 'application_name_example' # str |

    try:
        # Register Application
        api_response = api_instance.register_application10_applications_application_name_post(application_name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationApi->register_application10_applications_application_name_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **application_name** | **str**|  |

### Return type

[**Application**](Application.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
