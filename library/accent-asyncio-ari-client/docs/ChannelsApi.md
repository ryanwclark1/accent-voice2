# accent_appgateway_client.ChannelsApi

All URIs are relative to *http://localhost:8088/ari*

Method | HTTP request | Description
------------- | ------------- | -------------
[**channels_channel_id_answer_post**](ChannelsApi.md#channels_channel_id_answer_post) | **POST** /channels/{channelId}/answer | Answer a channel.
[**channels_channel_id_continue_post**](ChannelsApi.md#channels_channel_id_continue_post) | **POST** /channels/{channelId}/continue | Exit application; continue execution in the dialplan.
[**channels_channel_id_delete**](ChannelsApi.md#channels_channel_id_delete) | **DELETE** /channels/{channelId} | Delete (i.e. hangup) a channel.
[**channels_channel_id_dial_post**](ChannelsApi.md#channels_channel_id_dial_post) | **POST** /channels/{channelId}/dial | Dial a created channel.
[**channels_channel_id_dtmf_post**](ChannelsApi.md#channels_channel_id_dtmf_post) | **POST** /channels/{channelId}/dtmf | Send provided DTMF to a given channel.
[**channels_channel_id_get**](ChannelsApi.md#channels_channel_id_get) | **GET** /channels/{channelId} | Channel details.
[**channels_channel_id_hold_delete**](ChannelsApi.md#channels_channel_id_hold_delete) | **DELETE** /channels/{channelId}/hold | Remove a channel from hold.
[**channels_channel_id_hold_post**](ChannelsApi.md#channels_channel_id_hold_post) | **POST** /channels/{channelId}/hold | Hold a channel.
[**channels_channel_id_moh_delete**](ChannelsApi.md#channels_channel_id_moh_delete) | **DELETE** /channels/{channelId}/moh | Stop playing music on hold to a channel.
[**channels_channel_id_moh_post**](ChannelsApi.md#channels_channel_id_moh_post) | **POST** /channels/{channelId}/moh | Play music on hold to a channel.
[**channels_channel_id_move_post**](ChannelsApi.md#channels_channel_id_move_post) | **POST** /channels/{channelId}/move | Move the channel from one Stasis application to another.
[**channels_channel_id_mute_delete**](ChannelsApi.md#channels_channel_id_mute_delete) | **DELETE** /channels/{channelId}/mute | Unmute a channel.
[**channels_channel_id_mute_post**](ChannelsApi.md#channels_channel_id_mute_post) | **POST** /channels/{channelId}/mute | Mute a channel.
[**channels_channel_id_play_playback_id_post**](ChannelsApi.md#channels_channel_id_play_playback_id_post) | **POST** /channels/{channelId}/play/{playbackId} | Start playback of media and specify the playbackId.
[**channels_channel_id_play_post**](ChannelsApi.md#channels_channel_id_play_post) | **POST** /channels/{channelId}/play | Start playback of media.
[**channels_channel_id_post**](ChannelsApi.md#channels_channel_id_post) | **POST** /channels/{channelId} | Create a new channel (originate with id).
[**channels_channel_id_record_post**](ChannelsApi.md#channels_channel_id_record_post) | **POST** /channels/{channelId}/record | Start a recording.
[**channels_channel_id_redirect_post**](ChannelsApi.md#channels_channel_id_redirect_post) | **POST** /channels/{channelId}/redirect | Redirect the channel to a different location.
[**channels_channel_id_ring_delete**](ChannelsApi.md#channels_channel_id_ring_delete) | **DELETE** /channels/{channelId}/ring | Stop ringing indication on a channel if locally generated.
[**channels_channel_id_ring_post**](ChannelsApi.md#channels_channel_id_ring_post) | **POST** /channels/{channelId}/ring | Indicate ringing to a channel.
[**channels_channel_id_rtp_statistics_get**](ChannelsApi.md#channels_channel_id_rtp_statistics_get) | **GET** /channels/{channelId}/rtp_statistics | RTP stats on a channel.
[**channels_channel_id_silence_delete**](ChannelsApi.md#channels_channel_id_silence_delete) | **DELETE** /channels/{channelId}/silence | Stop playing silence to a channel.
[**channels_channel_id_silence_post**](ChannelsApi.md#channels_channel_id_silence_post) | **POST** /channels/{channelId}/silence | Play silence to a channel.
[**channels_channel_id_snoop_post**](ChannelsApi.md#channels_channel_id_snoop_post) | **POST** /channels/{channelId}/snoop | Start snooping.
[**channels_channel_id_snoop_snoop_id_post**](ChannelsApi.md#channels_channel_id_snoop_snoop_id_post) | **POST** /channels/{channelId}/snoop/{snoopId} | Start snooping.
[**channels_channel_id_variable_get**](ChannelsApi.md#channels_channel_id_variable_get) | **GET** /channels/{channelId}/variable | Get the value of a channel variable or function.
[**channels_channel_id_variable_post**](ChannelsApi.md#channels_channel_id_variable_post) | **POST** /channels/{channelId}/variable | Set the value of a channel variable or function.
[**channels_create_post**](ChannelsApi.md#channels_create_post) | **POST** /channels/create | Create channel.
[**channels_external_media_post**](ChannelsApi.md#channels_external_media_post) | **POST** /channels/externalMedia | Start an External Media session.
[**channels_get**](ChannelsApi.md#channels_get) | **GET** /channels | List all active channels in Asterisk.
[**channels_post**](ChannelsApi.md#channels_post) | **POST** /channels | Create a new channel (originate).


# **channels_channel_id_answer_post**
> channels_channel_id_answer_post(channel_id, x_asterisk_id=x_asterisk_id)

Answer a channel.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    channel_id = 'channel_id_example' # str | Channel's id
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)

    try:
        # Answer a channel.
        api_instance.channels_channel_id_answer_post(channel_id, x_asterisk_id=x_asterisk_id)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_channel_id_answer_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **channel_id** | **str**| Channel&#39;s id |
 **x_asterisk_id** | **str**|  | [optional]

### Return type

void (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_channel_id_continue_post**
> channels_channel_id_continue_post(channel_id, context=context, extension=extension, priority=priority, label=label, x_asterisk_id=x_asterisk_id)

Exit application; continue execution in the dialplan.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    channel_id = 'channel_id_example' # str | Channel's id
context = 'context_example' # str | The context to continue to. (optional)
extension = 'extension_example' # str | The extension to continue to. (optional)
priority = 56 # int | The priority to continue to. (optional)
label = 'label_example' # str | The label to continue to - will supersede 'priority' if both are provided. (optional)
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)

    try:
        # Exit application; continue execution in the dialplan.
        api_instance.channels_channel_id_continue_post(channel_id, context=context, extension=extension, priority=priority, label=label, x_asterisk_id=x_asterisk_id)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_channel_id_continue_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **channel_id** | **str**| Channel&#39;s id |
 **context** | **str**| The context to continue to. | [optional]
 **extension** | **str**| The extension to continue to. | [optional]
 **priority** | **int**| The priority to continue to. | [optional]
 **label** | **str**| The label to continue to - will supersede &#39;priority&#39; if both are provided. | [optional]
 **x_asterisk_id** | **str**|  | [optional]

### Return type

void (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_channel_id_delete**
> channels_channel_id_delete(channel_id, reason_code=reason_code, reason=reason, x_asterisk_id=x_asterisk_id)

Delete (i.e. hangup) a channel.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    channel_id = 'channel_id_example' # str | Channel's id
reason_code = 'reason_code_example' # str | The reason code for hanging up the channel for detail use. Mutually exclusive with 'reason'. See detail hangup codes at here. https://wiki.asterisk.org/wiki/display/AST/Hangup+Cause+Mappings (optional)
reason = 'reason_example' # str | Reason for hanging up the channel for simple use. Mutually exclusive with 'reason_code'. (optional)
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)

    try:
        # Delete (i.e. hangup) a channel.
        api_instance.channels_channel_id_delete(channel_id, reason_code=reason_code, reason=reason, x_asterisk_id=x_asterisk_id)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_channel_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **channel_id** | **str**| Channel&#39;s id |
 **reason_code** | **str**| The reason code for hanging up the channel for detail use. Mutually exclusive with &#39;reason&#39;. See detail hangup codes at here. https://wiki.asterisk.org/wiki/display/AST/Hangup+Cause+Mappings | [optional]
 **reason** | **str**| Reason for hanging up the channel for simple use. Mutually exclusive with &#39;reason_code&#39;. | [optional]
 **x_asterisk_id** | **str**|  | [optional]

### Return type

void (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_channel_id_dial_post**
> channels_channel_id_dial_post(channel_id, caller=caller, timeout=timeout, x_asterisk_id=x_asterisk_id)

Dial a created channel.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    channel_id = 'channel_id_example' # str | Channel's id
caller = 'caller_example' # str | Channel ID of caller (optional)
timeout = 0 # int | Dial timeout (optional) (default to 0)
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)

    try:
        # Dial a created channel.
        api_instance.channels_channel_id_dial_post(channel_id, caller=caller, timeout=timeout, x_asterisk_id=x_asterisk_id)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_channel_id_dial_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **channel_id** | **str**| Channel&#39;s id |
 **caller** | **str**| Channel ID of caller | [optional]
 **timeout** | **int**| Dial timeout | [optional] [default to 0]
 **x_asterisk_id** | **str**|  | [optional]

### Return type

void (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_channel_id_dtmf_post**
> channels_channel_id_dtmf_post(channel_id, dtmf=dtmf, before=before, between=between, duration=duration, after=after, x_asterisk_id=x_asterisk_id)

Send provided DTMF to a given channel.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    channel_id = 'channel_id_example' # str | Channel's id
dtmf = 'dtmf_example' # str | DTMF To send. (optional)
before = 0 # int | Amount of time to wait before DTMF digits (specified in milliseconds) start. (optional) (default to 0)
between = 100 # int | Amount of time in between DTMF digits (specified in milliseconds). (optional) (default to 100)
duration = 100 # int | Length of each DTMF digit (specified in milliseconds). (optional) (default to 100)
after = 0 # int | Amount of time to wait after DTMF digits (specified in milliseconds) end. (optional) (default to 0)
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)

    try:
        # Send provided DTMF to a given channel.
        api_instance.channels_channel_id_dtmf_post(channel_id, dtmf=dtmf, before=before, between=between, duration=duration, after=after, x_asterisk_id=x_asterisk_id)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_channel_id_dtmf_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **channel_id** | **str**| Channel&#39;s id |
 **dtmf** | **str**| DTMF To send. | [optional]
 **before** | **int**| Amount of time to wait before DTMF digits (specified in milliseconds) start. | [optional] [default to 0]
 **between** | **int**| Amount of time in between DTMF digits (specified in milliseconds). | [optional] [default to 100]
 **duration** | **int**| Length of each DTMF digit (specified in milliseconds). | [optional] [default to 100]
 **after** | **int**| Amount of time to wait after DTMF digits (specified in milliseconds) end. | [optional] [default to 0]
 **x_asterisk_id** | **str**|  | [optional]

### Return type

void (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_channel_id_get**
> Channel channels_channel_id_get(channel_id, x_asterisk_id=x_asterisk_id)

Channel details.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    channel_id = 'channel_id_example' # str | Channel's id
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)

    try:
        # Channel details.
        api_response = api_instance.channels_channel_id_get(channel_id, x_asterisk_id=x_asterisk_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_channel_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **channel_id** | **str**| Channel&#39;s id |
 **x_asterisk_id** | **str**|  | [optional]

### Return type

[**Channel**](Channel.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_channel_id_hold_delete**
> channels_channel_id_hold_delete(channel_id, x_asterisk_id=x_asterisk_id)

Remove a channel from hold.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    channel_id = 'channel_id_example' # str | Channel's id
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)

    try:
        # Remove a channel from hold.
        api_instance.channels_channel_id_hold_delete(channel_id, x_asterisk_id=x_asterisk_id)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_channel_id_hold_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **channel_id** | **str**| Channel&#39;s id |
 **x_asterisk_id** | **str**|  | [optional]

### Return type

void (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_channel_id_hold_post**
> channels_channel_id_hold_post(channel_id, x_asterisk_id=x_asterisk_id)

Hold a channel.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    channel_id = 'channel_id_example' # str | Channel's id
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)

    try:
        # Hold a channel.
        api_instance.channels_channel_id_hold_post(channel_id, x_asterisk_id=x_asterisk_id)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_channel_id_hold_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **channel_id** | **str**| Channel&#39;s id |
 **x_asterisk_id** | **str**|  | [optional]

### Return type

void (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_channel_id_moh_delete**
> channels_channel_id_moh_delete(channel_id, x_asterisk_id=x_asterisk_id)

Stop playing music on hold to a channel.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    channel_id = 'channel_id_example' # str | Channel's id
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)

    try:
        # Stop playing music on hold to a channel.
        api_instance.channels_channel_id_moh_delete(channel_id, x_asterisk_id=x_asterisk_id)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_channel_id_moh_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **channel_id** | **str**| Channel&#39;s id |
 **x_asterisk_id** | **str**|  | [optional]

### Return type

void (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_channel_id_moh_post**
> channels_channel_id_moh_post(channel_id, moh_class=moh_class, x_asterisk_id=x_asterisk_id)

Play music on hold to a channel.

Using media operations such as /play on a channel playing MOH in this manner will suspend MOH without resuming automatically. If continuing music on hold is desired, the stasis application must reinitiate music on hold.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    channel_id = 'channel_id_example' # str | Channel's id
moh_class = 'moh_class_example' # str | Music on hold class to use (optional)
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)

    try:
        # Play music on hold to a channel.
        api_instance.channels_channel_id_moh_post(channel_id, moh_class=moh_class, x_asterisk_id=x_asterisk_id)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_channel_id_moh_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **channel_id** | **str**| Channel&#39;s id |
 **moh_class** | **str**| Music on hold class to use | [optional]
 **x_asterisk_id** | **str**|  | [optional]

### Return type

void (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_channel_id_move_post**
> channels_channel_id_move_post(channel_id, app, app_args=app_args, x_asterisk_id=x_asterisk_id)

Move the channel from one Stasis application to another.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    channel_id = 'channel_id_example' # str | Channel's id
app = 'app_example' # str | The channel will be passed to this Stasis application.
app_args = 'app_args_example' # str | The application arguments to pass to the Stasis application provided by 'app'. (optional)
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)

    try:
        # Move the channel from one Stasis application to another.
        api_instance.channels_channel_id_move_post(channel_id, app, app_args=app_args, x_asterisk_id=x_asterisk_id)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_channel_id_move_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **channel_id** | **str**| Channel&#39;s id |
 **app** | **str**| The channel will be passed to this Stasis application. |
 **app_args** | **str**| The application arguments to pass to the Stasis application provided by &#39;app&#39;. | [optional]
 **x_asterisk_id** | **str**|  | [optional]

### Return type

void (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_channel_id_mute_delete**
> channels_channel_id_mute_delete(channel_id, direction=direction, x_asterisk_id=x_asterisk_id)

Unmute a channel.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    channel_id = 'channel_id_example' # str | Channel's id
direction = 'both' # str | Direction in which to unmute audio (optional) (default to 'both')
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)

    try:
        # Unmute a channel.
        api_instance.channels_channel_id_mute_delete(channel_id, direction=direction, x_asterisk_id=x_asterisk_id)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_channel_id_mute_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **channel_id** | **str**| Channel&#39;s id |
 **direction** | **str**| Direction in which to unmute audio | [optional] [default to &#39;both&#39;]
 **x_asterisk_id** | **str**|  | [optional]

### Return type

void (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_channel_id_mute_post**
> channels_channel_id_mute_post(channel_id, direction=direction, x_asterisk_id=x_asterisk_id)

Mute a channel.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    channel_id = 'channel_id_example' # str | Channel's id
direction = 'both' # str | Direction in which to mute audio (optional) (default to 'both')
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)

    try:
        # Mute a channel.
        api_instance.channels_channel_id_mute_post(channel_id, direction=direction, x_asterisk_id=x_asterisk_id)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_channel_id_mute_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **channel_id** | **str**| Channel&#39;s id |
 **direction** | **str**| Direction in which to mute audio | [optional] [default to &#39;both&#39;]
 **x_asterisk_id** | **str**|  | [optional]

### Return type

void (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_channel_id_play_playback_id_post**
> Playback channels_channel_id_play_playback_id_post(channel_id, playback_id, media, lang=lang, offsetms=offsetms, skipms=skipms, x_asterisk_id=x_asterisk_id)

Start playback of media and specify the playbackId.

The media URI may be any of a number of URI's. Currently sound:, recording:, number:, digits:, characters:, and tone: URI's are supported. This operation creates a playback resource that can be used to control the playback of media (pause, rewind, fast forward, etc.)

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    channel_id = 'channel_id_example' # str | Channel's id
playback_id = 'playback_id_example' # str | Playback ID.
media = ['media_example'] # list[str] | Media URIs to play.
lang = 'lang_example' # str | For sounds, selects language for sound. (optional)
offsetms = 56 # int | Number of milliseconds to skip before playing. Only applies to the first URI if multiple media URIs are specified. (optional)
skipms = 3000 # int | Number of milliseconds to skip for forward/reverse operations. (optional) (default to 3000)
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)

    try:
        # Start playback of media and specify the playbackId.
        api_response = api_instance.channels_channel_id_play_playback_id_post(channel_id, playback_id, media, lang=lang, offsetms=offsetms, skipms=skipms, x_asterisk_id=x_asterisk_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_channel_id_play_playback_id_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **channel_id** | **str**| Channel&#39;s id |
 **playback_id** | **str**| Playback ID. |
 **media** | [**list[str]**](str.md)| Media URIs to play. |
 **lang** | **str**| For sounds, selects language for sound. | [optional]
 **offsetms** | **int**| Number of milliseconds to skip before playing. Only applies to the first URI if multiple media URIs are specified. | [optional]
 **skipms** | **int**| Number of milliseconds to skip for forward/reverse operations. | [optional] [default to 3000]
 **x_asterisk_id** | **str**|  | [optional]

### Return type

[**Playback**](Playback.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_channel_id_play_post**
> Playback channels_channel_id_play_post(channel_id, media, lang=lang, offsetms=offsetms, skipms=skipms, playback_id=playback_id, x_asterisk_id=x_asterisk_id)

Start playback of media.

The media URI may be any of a number of URI's. Currently sound:, recording:, number:, digits:, characters:, and tone: URI's are supported. This operation creates a playback resource that can be used to control the playback of media (pause, rewind, fast forward, etc.)

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    channel_id = 'channel_id_example' # str | Channel's id
media = ['media_example'] # list[str] | Media URIs to play.
lang = 'lang_example' # str | For sounds, selects language for sound. (optional)
offsetms = 56 # int | Number of milliseconds to skip before playing. Only applies to the first URI if multiple media URIs are specified. (optional)
skipms = 3000 # int | Number of milliseconds to skip for forward/reverse operations. (optional) (default to 3000)
playback_id = 'playback_id_example' # str | Playback ID. (optional)
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)

    try:
        # Start playback of media.
        api_response = api_instance.channels_channel_id_play_post(channel_id, media, lang=lang, offsetms=offsetms, skipms=skipms, playback_id=playback_id, x_asterisk_id=x_asterisk_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_channel_id_play_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **channel_id** | **str**| Channel&#39;s id |
 **media** | [**list[str]**](str.md)| Media URIs to play. |
 **lang** | **str**| For sounds, selects language for sound. | [optional]
 **offsetms** | **int**| Number of milliseconds to skip before playing. Only applies to the first URI if multiple media URIs are specified. | [optional]
 **skipms** | **int**| Number of milliseconds to skip for forward/reverse operations. | [optional] [default to 3000]
 **playback_id** | **str**| Playback ID. | [optional]
 **x_asterisk_id** | **str**|  | [optional]

### Return type

[**Playback**](Playback.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_channel_id_post**
> Channel channels_channel_id_post(channel_id, endpoint, extension=extension, context=context, priority=priority, label=label, app=app, app_args=app_args, caller_id=caller_id, timeout=timeout, other_channel_id=other_channel_id, originator=originator, formats=formats, x_asterisk_id=x_asterisk_id, containers=containers)

Create a new channel (originate with id).

The new channel is created immediately and a snapshot of it returned. If a Stasis application is provided it will be automatically subscribed to the originated channel for further events and updates.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    channel_id = 'channel_id_example' # str | The unique id to assign the channel on creation.
endpoint = 'endpoint_example' # str | Endpoint to call.
extension = 'extension_example' # str | The extension to dial after the endpoint answers. Mutually exclusive with 'app'. (optional)
context = 'context_example' # str | The context to dial after the endpoint answers. If omitted, uses 'default'. Mutually exclusive with 'app'. (optional)
priority = 56 # int | The priority to dial after the endpoint answers. If omitted, uses 1. Mutually exclusive with 'app'. (optional)
label = 'label_example' # str | The label to dial after the endpoint answers. Will supersede 'priority' if provided. Mutually exclusive with 'app'. (optional)
app = 'app_example' # str | The application that is subscribed to the originated channel. When the channel is answered, it will be passed to this Stasis application. Mutually exclusive with 'context', 'extension', 'priority', and 'label'. (optional)
app_args = 'app_args_example' # str | The application arguments to pass to the Stasis application provided by 'app'. Mutually exclusive with 'context', 'extension', 'priority', and 'label'. (optional)
caller_id = 'caller_id_example' # str | CallerID to use when dialing the endpoint or extension. (optional)
timeout = 30 # int | Timeout (in seconds) before giving up dialing, or -1 for no timeout. (optional) (default to 30)
other_channel_id = 'other_channel_id_example' # str | The unique id to assign the second channel when using local channels. (optional)
originator = 'originator_example' # str | The unique id of the channel which is originating this one. (optional)
formats = 'formats_example' # str | The format name capability list to use if originator is not specified. Ex. \"ulaw,slin16\".  Format names can be found with \"core show codecs\". (optional)
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)
containers = accent_appgateway_client.Containers() # Containers | The \"variables\" key in the body object holds variable key/value pairs to set on the channel on creation. Other keys in the body object are interpreted as query parameters. Ex. { \"endpoint\": \"SIP/Alice\", \"variables\": { \"CALLERID(name)\": \"Alice\" } } (optional)

    try:
        # Create a new channel (originate with id).
        api_response = api_instance.channels_channel_id_post(channel_id, endpoint, extension=extension, context=context, priority=priority, label=label, app=app, app_args=app_args, caller_id=caller_id, timeout=timeout, other_channel_id=other_channel_id, originator=originator, formats=formats, x_asterisk_id=x_asterisk_id, containers=containers)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_channel_id_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **channel_id** | **str**| The unique id to assign the channel on creation. |
 **endpoint** | **str**| Endpoint to call. |
 **extension** | **str**| The extension to dial after the endpoint answers. Mutually exclusive with &#39;app&#39;. | [optional]
 **context** | **str**| The context to dial after the endpoint answers. If omitted, uses &#39;default&#39;. Mutually exclusive with &#39;app&#39;. | [optional]
 **priority** | **int**| The priority to dial after the endpoint answers. If omitted, uses 1. Mutually exclusive with &#39;app&#39;. | [optional]
 **label** | **str**| The label to dial after the endpoint answers. Will supersede &#39;priority&#39; if provided. Mutually exclusive with &#39;app&#39;. | [optional]
 **app** | **str**| The application that is subscribed to the originated channel. When the channel is answered, it will be passed to this Stasis application. Mutually exclusive with &#39;context&#39;, &#39;extension&#39;, &#39;priority&#39;, and &#39;label&#39;. | [optional]
 **app_args** | **str**| The application arguments to pass to the Stasis application provided by &#39;app&#39;. Mutually exclusive with &#39;context&#39;, &#39;extension&#39;, &#39;priority&#39;, and &#39;label&#39;. | [optional]
 **caller_id** | **str**| CallerID to use when dialing the endpoint or extension. | [optional]
 **timeout** | **int**| Timeout (in seconds) before giving up dialing, or -1 for no timeout. | [optional] [default to 30]
 **other_channel_id** | **str**| The unique id to assign the second channel when using local channels. | [optional]
 **originator** | **str**| The unique id of the channel which is originating this one. | [optional]
 **formats** | **str**| The format name capability list to use if originator is not specified. Ex. \&quot;ulaw,slin16\&quot;.  Format names can be found with \&quot;core show codecs\&quot;. | [optional]
 **x_asterisk_id** | **str**|  | [optional]
 **containers** | [**Containers**](Containers.md)| The \&quot;variables\&quot; key in the body object holds variable key/value pairs to set on the channel on creation. Other keys in the body object are interpreted as query parameters. Ex. { \&quot;endpoint\&quot;: \&quot;SIP/Alice\&quot;, \&quot;variables\&quot;: { \&quot;CALLERID(name)\&quot;: \&quot;Alice\&quot; } } | [optional]

### Return type

[**Channel**](Channel.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_channel_id_record_post**
> LiveRecording channels_channel_id_record_post(channel_id, name, format, max_duration_seconds=max_duration_seconds, max_silence_seconds=max_silence_seconds, if_exists=if_exists, beep=beep, terminate_on=terminate_on, x_asterisk_id=x_asterisk_id)

Start a recording.

Record audio from a channel. Note that this will not capture audio sent to the channel. The bridge itself has a record feature if that's what you want.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    channel_id = 'channel_id_example' # str | Channel's id
name = 'name_example' # str | Recording's filename
format = 'format_example' # str | Format to encode audio in
max_duration_seconds = 0 # int | Maximum duration of the recording, in seconds. 0 for no limit (optional) (default to 0)
max_silence_seconds = 0 # int | Maximum duration of silence, in seconds. 0 for no limit (optional) (default to 0)
if_exists = 'fail' # str | Action to take if a recording with the same name already exists. (optional) (default to 'fail')
beep = False # bool | Play beep when recording begins (optional) (default to False)
terminate_on = 'none' # str | DTMF input to terminate recording (optional) (default to 'none')
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)

    try:
        # Start a recording.
        api_response = api_instance.channels_channel_id_record_post(channel_id, name, format, max_duration_seconds=max_duration_seconds, max_silence_seconds=max_silence_seconds, if_exists=if_exists, beep=beep, terminate_on=terminate_on, x_asterisk_id=x_asterisk_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_channel_id_record_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **channel_id** | **str**| Channel&#39;s id |
 **name** | **str**| Recording&#39;s filename |
 **format** | **str**| Format to encode audio in |
 **max_duration_seconds** | **int**| Maximum duration of the recording, in seconds. 0 for no limit | [optional] [default to 0]
 **max_silence_seconds** | **int**| Maximum duration of silence, in seconds. 0 for no limit | [optional] [default to 0]
 **if_exists** | **str**| Action to take if a recording with the same name already exists. | [optional] [default to &#39;fail&#39;]
 **beep** | **bool**| Play beep when recording begins | [optional] [default to False]
 **terminate_on** | **str**| DTMF input to terminate recording | [optional] [default to &#39;none&#39;]
 **x_asterisk_id** | **str**|  | [optional]

### Return type

[**LiveRecording**](LiveRecording.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_channel_id_redirect_post**
> channels_channel_id_redirect_post(channel_id, endpoint, x_asterisk_id=x_asterisk_id)

Redirect the channel to a different location.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    channel_id = 'channel_id_example' # str | Channel's id
endpoint = 'endpoint_example' # str | The endpoint to redirect the channel to
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)

    try:
        # Redirect the channel to a different location.
        api_instance.channels_channel_id_redirect_post(channel_id, endpoint, x_asterisk_id=x_asterisk_id)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_channel_id_redirect_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **channel_id** | **str**| Channel&#39;s id |
 **endpoint** | **str**| The endpoint to redirect the channel to |
 **x_asterisk_id** | **str**|  | [optional]

### Return type

void (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_channel_id_ring_delete**
> channels_channel_id_ring_delete(channel_id, x_asterisk_id=x_asterisk_id)

Stop ringing indication on a channel if locally generated.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    channel_id = 'channel_id_example' # str | Channel's id
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)

    try:
        # Stop ringing indication on a channel if locally generated.
        api_instance.channels_channel_id_ring_delete(channel_id, x_asterisk_id=x_asterisk_id)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_channel_id_ring_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **channel_id** | **str**| Channel&#39;s id |
 **x_asterisk_id** | **str**|  | [optional]

### Return type

void (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_channel_id_ring_post**
> channels_channel_id_ring_post(channel_id, x_asterisk_id=x_asterisk_id)

Indicate ringing to a channel.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    channel_id = 'channel_id_example' # str | Channel's id
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)

    try:
        # Indicate ringing to a channel.
        api_instance.channels_channel_id_ring_post(channel_id, x_asterisk_id=x_asterisk_id)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_channel_id_ring_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **channel_id** | **str**| Channel&#39;s id |
 **x_asterisk_id** | **str**|  | [optional]

### Return type

void (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_channel_id_rtp_statistics_get**
> RTPstat channels_channel_id_rtp_statistics_get(channel_id, x_asterisk_id=x_asterisk_id)

RTP stats on a channel.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    channel_id = 'channel_id_example' # str | Channel's id
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)

    try:
        # RTP stats on a channel.
        api_response = api_instance.channels_channel_id_rtp_statistics_get(channel_id, x_asterisk_id=x_asterisk_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_channel_id_rtp_statistics_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **channel_id** | **str**| Channel&#39;s id |
 **x_asterisk_id** | **str**|  | [optional]

### Return type

[**RTPstat**](RTPstat.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_channel_id_silence_delete**
> channels_channel_id_silence_delete(channel_id, x_asterisk_id=x_asterisk_id)

Stop playing silence to a channel.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    channel_id = 'channel_id_example' # str | Channel's id
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)

    try:
        # Stop playing silence to a channel.
        api_instance.channels_channel_id_silence_delete(channel_id, x_asterisk_id=x_asterisk_id)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_channel_id_silence_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **channel_id** | **str**| Channel&#39;s id |
 **x_asterisk_id** | **str**|  | [optional]

### Return type

void (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_channel_id_silence_post**
> channels_channel_id_silence_post(channel_id, x_asterisk_id=x_asterisk_id)

Play silence to a channel.

Using media operations such as /play on a channel playing silence in this manner will suspend silence without resuming automatically.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    channel_id = 'channel_id_example' # str | Channel's id
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)

    try:
        # Play silence to a channel.
        api_instance.channels_channel_id_silence_post(channel_id, x_asterisk_id=x_asterisk_id)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_channel_id_silence_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **channel_id** | **str**| Channel&#39;s id |
 **x_asterisk_id** | **str**|  | [optional]

### Return type

void (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_channel_id_snoop_post**
> Channel channels_channel_id_snoop_post(channel_id, app, spy=spy, whisper=whisper, app_args=app_args, snoop_id=snoop_id, x_asterisk_id=x_asterisk_id)

Start snooping.

Snoop (spy/whisper) on a specific channel.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    channel_id = 'channel_id_example' # str | Channel's id
app = 'app_example' # str | Application the snooping channel is placed into
spy = 'none' # str | Direction of audio to spy on (optional) (default to 'none')
whisper = 'none' # str | Direction of audio to whisper into (optional) (default to 'none')
app_args = 'app_args_example' # str | The application arguments to pass to the Stasis application (optional)
snoop_id = 'snoop_id_example' # str | Unique ID to assign to snooping channel (optional)
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)

    try:
        # Start snooping.
        api_response = api_instance.channels_channel_id_snoop_post(channel_id, app, spy=spy, whisper=whisper, app_args=app_args, snoop_id=snoop_id, x_asterisk_id=x_asterisk_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_channel_id_snoop_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **channel_id** | **str**| Channel&#39;s id |
 **app** | **str**| Application the snooping channel is placed into |
 **spy** | **str**| Direction of audio to spy on | [optional] [default to &#39;none&#39;]
 **whisper** | **str**| Direction of audio to whisper into | [optional] [default to &#39;none&#39;]
 **app_args** | **str**| The application arguments to pass to the Stasis application | [optional]
 **snoop_id** | **str**| Unique ID to assign to snooping channel | [optional]
 **x_asterisk_id** | **str**|  | [optional]

### Return type

[**Channel**](Channel.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_channel_id_snoop_snoop_id_post**
> Channel channels_channel_id_snoop_snoop_id_post(channel_id, snoop_id, app, spy=spy, whisper=whisper, app_args=app_args, x_asterisk_id=x_asterisk_id)

Start snooping.

Snoop (spy/whisper) on a specific channel.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    channel_id = 'channel_id_example' # str | Channel's id
snoop_id = 'snoop_id_example' # str | Unique ID to assign to snooping channel
app = 'app_example' # str | Application the snooping channel is placed into
spy = 'none' # str | Direction of audio to spy on (optional) (default to 'none')
whisper = 'none' # str | Direction of audio to whisper into (optional) (default to 'none')
app_args = 'app_args_example' # str | The application arguments to pass to the Stasis application (optional)
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)

    try:
        # Start snooping.
        api_response = api_instance.channels_channel_id_snoop_snoop_id_post(channel_id, snoop_id, app, spy=spy, whisper=whisper, app_args=app_args, x_asterisk_id=x_asterisk_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_channel_id_snoop_snoop_id_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **channel_id** | **str**| Channel&#39;s id |
 **snoop_id** | **str**| Unique ID to assign to snooping channel |
 **app** | **str**| Application the snooping channel is placed into |
 **spy** | **str**| Direction of audio to spy on | [optional] [default to &#39;none&#39;]
 **whisper** | **str**| Direction of audio to whisper into | [optional] [default to &#39;none&#39;]
 **app_args** | **str**| The application arguments to pass to the Stasis application | [optional]
 **x_asterisk_id** | **str**|  | [optional]

### Return type

[**Channel**](Channel.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_channel_id_variable_get**
> Variable channels_channel_id_variable_get(channel_id, variable, x_asterisk_id=x_asterisk_id)

Get the value of a channel variable or function.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    channel_id = 'channel_id_example' # str | Channel's id
variable = 'variable_example' # str | The channel variable or function to get
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)

    try:
        # Get the value of a channel variable or function.
        api_response = api_instance.channels_channel_id_variable_get(channel_id, variable, x_asterisk_id=x_asterisk_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_channel_id_variable_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **channel_id** | **str**| Channel&#39;s id |
 **variable** | **str**| The channel variable or function to get |
 **x_asterisk_id** | **str**|  | [optional]

### Return type

[**Variable**](Variable.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_channel_id_variable_post**
> channels_channel_id_variable_post(channel_id, variable, value=value, x_asterisk_id=x_asterisk_id)

Set the value of a channel variable or function.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    channel_id = 'channel_id_example' # str | Channel's id
variable = 'variable_example' # str | The channel variable or function to set
value = 'value_example' # str | The value to set the variable to (optional)
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)

    try:
        # Set the value of a channel variable or function.
        api_instance.channels_channel_id_variable_post(channel_id, variable, value=value, x_asterisk_id=x_asterisk_id)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_channel_id_variable_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **channel_id** | **str**| Channel&#39;s id |
 **variable** | **str**| The channel variable or function to set |
 **value** | **str**| The value to set the variable to | [optional]
 **x_asterisk_id** | **str**|  | [optional]

### Return type

void (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_create_post**
> Channel channels_create_post(endpoint, app, app_args=app_args, channel_id=channel_id, other_channel_id=other_channel_id, originator=originator, formats=formats, x_asterisk_id=x_asterisk_id, containers=containers)

Create channel.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    endpoint = 'endpoint_example' # str | Endpoint for channel communication
app = 'app_example' # str | Stasis Application to place channel into
app_args = 'app_args_example' # str | The application arguments to pass to the Stasis application provided by 'app'. Mutually exclusive with 'context', 'extension', 'priority', and 'label'. (optional)
channel_id = 'channel_id_example' # str | The unique id to assign the channel on creation. (optional)
other_channel_id = 'other_channel_id_example' # str | The unique id to assign the second channel when using local channels. (optional)
originator = 'originator_example' # str | Unique ID of the calling channel (optional)
formats = 'formats_example' # str | The format name capability list to use if originator is not specified. Ex. \"ulaw,slin16\".  Format names can be found with \"core show codecs\". (optional)
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)
containers = accent_appgateway_client.Containers() # Containers | The \"variables\" key in the body object holds variable key/value pairs to set on the channel on creation. Other keys in the body object are interpreted as query parameters. Ex. { \"endpoint\": \"SIP/Alice\", \"variables\": { \"CALLERID(name)\": \"Alice\" } } (optional)

    try:
        # Create channel.
        api_response = api_instance.channels_create_post(endpoint, app, app_args=app_args, channel_id=channel_id, other_channel_id=other_channel_id, originator=originator, formats=formats, x_asterisk_id=x_asterisk_id, containers=containers)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_create_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **endpoint** | **str**| Endpoint for channel communication |
 **app** | **str**| Stasis Application to place channel into |
 **app_args** | **str**| The application arguments to pass to the Stasis application provided by &#39;app&#39;. Mutually exclusive with &#39;context&#39;, &#39;extension&#39;, &#39;priority&#39;, and &#39;label&#39;. | [optional]
 **channel_id** | **str**| The unique id to assign the channel on creation. | [optional]
 **other_channel_id** | **str**| The unique id to assign the second channel when using local channels. | [optional]
 **originator** | **str**| Unique ID of the calling channel | [optional]
 **formats** | **str**| The format name capability list to use if originator is not specified. Ex. \&quot;ulaw,slin16\&quot;.  Format names can be found with \&quot;core show codecs\&quot;. | [optional]
 **x_asterisk_id** | **str**|  | [optional]
 **containers** | [**Containers**](Containers.md)| The \&quot;variables\&quot; key in the body object holds variable key/value pairs to set on the channel on creation. Other keys in the body object are interpreted as query parameters. Ex. { \&quot;endpoint\&quot;: \&quot;SIP/Alice\&quot;, \&quot;variables\&quot;: { \&quot;CALLERID(name)\&quot;: \&quot;Alice\&quot; } } | [optional]

### Return type

[**Channel**](Channel.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_external_media_post**
> Channel channels_external_media_post(app, external_host, format, channel_id=channel_id, encapsulation=encapsulation, transport=transport, connection_type=connection_type, direction=direction, x_asterisk_id=x_asterisk_id, containers=containers)

Start an External Media session.

Create a channel to an External Media source/sink.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    app = 'app_example' # str | Stasis Application to place channel into
external_host = 'external_host_example' # str | Hostname/ip:port of external host
format = 'format_example' # str | Format to encode audio in
channel_id = 'channel_id_example' # str | The unique id to assign the channel on creation. (optional)
encapsulation = 'rtp' # str | Payload encapsulation protocol (optional) (default to 'rtp')
transport = 'udp' # str | Transport protocol (optional) (default to 'udp')
connection_type = 'client' # str | Connection type (client/server) (optional) (default to 'client')
direction = 'both' # str | External media direction (optional) (default to 'both')
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)
containers = accent_appgateway_client.Containers() # Containers | The \"variables\" key in the body object holds variable key/value pairs to set on the channel on creation. Other keys in the body object are interpreted as query parameters. Ex. { \"endpoint\": \"SIP/Alice\", \"variables\": { \"CALLERID(name)\": \"Alice\" } } (optional)

    try:
        # Start an External Media session.
        api_response = api_instance.channels_external_media_post(app, external_host, format, channel_id=channel_id, encapsulation=encapsulation, transport=transport, connection_type=connection_type, direction=direction, x_asterisk_id=x_asterisk_id, containers=containers)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_external_media_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app** | **str**| Stasis Application to place channel into |
 **external_host** | **str**| Hostname/ip:port of external host |
 **format** | **str**| Format to encode audio in |
 **channel_id** | **str**| The unique id to assign the channel on creation. | [optional]
 **encapsulation** | **str**| Payload encapsulation protocol | [optional] [default to &#39;rtp&#39;]
 **transport** | **str**| Transport protocol | [optional] [default to &#39;udp&#39;]
 **connection_type** | **str**| Connection type (client/server) | [optional] [default to &#39;client&#39;]
 **direction** | **str**| External media direction | [optional] [default to &#39;both&#39;]
 **x_asterisk_id** | **str**|  | [optional]
 **containers** | [**Containers**](Containers.md)| The \&quot;variables\&quot; key in the body object holds variable key/value pairs to set on the channel on creation. Other keys in the body object are interpreted as query parameters. Ex. { \&quot;endpoint\&quot;: \&quot;SIP/Alice\&quot;, \&quot;variables\&quot;: { \&quot;CALLERID(name)\&quot;: \&quot;Alice\&quot; } } | [optional]

### Return type

[**Channel**](Channel.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_get**
> list[Channel] channels_get(x_asterisk_id=x_asterisk_id)

List all active channels in Asterisk.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)

    try:
        # List all active channels in Asterisk.
        api_response = api_instance.channels_get(x_asterisk_id=x_asterisk_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_asterisk_id** | **str**|  | [optional]

### Return type

[**list[Channel]**](Channel.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **channels_post**
> Channel channels_post(endpoint, extension=extension, context=context, priority=priority, label=label, app=app, app_args=app_args, caller_id=caller_id, timeout=timeout, channel_id=channel_id, other_channel_id=other_channel_id, originator=originator, formats=formats, x_asterisk_id=x_asterisk_id, containers=containers)

Create a new channel (originate).

The new channel is created immediately and a snapshot of it returned. If a Stasis application is provided it will be automatically subscribed to the originated channel for further events and updates.

### Example

* Basic Authentication (basicAuth):
```python
from __future__ import print_function
import time
import accent_appgateway_client
from accent_appgateway_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8088/ari
# See configuration.py for a list of all supported configuration parameters.
configuration = accent_appgateway_client.Configuration(
    host = "http://localhost:8088/ari"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = accent_appgateway_client.Configuration(
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with accent_appgateway_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accent_appgateway_client.ChannelsApi(api_client)
    endpoint = 'endpoint_example' # str | Endpoint to call.
extension = 'extension_example' # str | The extension to dial after the endpoint answers. Mutually exclusive with 'app'. (optional)
context = 'context_example' # str | The context to dial after the endpoint answers. If omitted, uses 'default'. Mutually exclusive with 'app'. (optional)
priority = 56 # int | The priority to dial after the endpoint answers. If omitted, uses 1. Mutually exclusive with 'app'. (optional)
label = 'label_example' # str | The label to dial after the endpoint answers. Will supersede 'priority' if provided. Mutually exclusive with 'app'. (optional)
app = 'app_example' # str | The application that is subscribed to the originated channel. When the channel is answered, it will be passed to this Stasis application. Mutually exclusive with 'context', 'extension', 'priority', and 'label'. (optional)
app_args = 'app_args_example' # str | The application arguments to pass to the Stasis application provided by 'app'. Mutually exclusive with 'context', 'extension', 'priority', and 'label'. (optional)
caller_id = 'caller_id_example' # str | CallerID to use when dialing the endpoint or extension. (optional)
timeout = 30 # int | Timeout (in seconds) before giving up dialing, or -1 for no timeout. (optional) (default to 30)
channel_id = 'channel_id_example' # str | The unique id to assign the channel on creation. (optional)
other_channel_id = 'other_channel_id_example' # str | The unique id to assign the second channel when using local channels. (optional)
originator = 'originator_example' # str | The unique id of the channel which is originating this one. (optional)
formats = 'formats_example' # str | The format name capability list to use if originator is not specified. Ex. \"ulaw,slin16\".  Format names can be found with \"core show codecs\". (optional)
x_asterisk_id = 'x_asterisk_id_example' # str |  (optional)
containers = accent_appgateway_client.Containers() # Containers | The \"variables\" key in the body object holds variable key/value pairs to set on the channel on creation. Other keys in the body object are interpreted as query parameters. Ex. { \"endpoint\": \"SIP/Alice\", \"variables\": { \"CALLERID(name)\": \"Alice\" } } (optional)

    try:
        # Create a new channel (originate).
        api_response = api_instance.channels_post(endpoint, extension=extension, context=context, priority=priority, label=label, app=app, app_args=app_args, caller_id=caller_id, timeout=timeout, channel_id=channel_id, other_channel_id=other_channel_id, originator=originator, formats=formats, x_asterisk_id=x_asterisk_id, containers=containers)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ChannelsApi->channels_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **endpoint** | **str**| Endpoint to call. |
 **extension** | **str**| The extension to dial after the endpoint answers. Mutually exclusive with &#39;app&#39;. | [optional]
 **context** | **str**| The context to dial after the endpoint answers. If omitted, uses &#39;default&#39;. Mutually exclusive with &#39;app&#39;. | [optional]
 **priority** | **int**| The priority to dial after the endpoint answers. If omitted, uses 1. Mutually exclusive with &#39;app&#39;. | [optional]
 **label** | **str**| The label to dial after the endpoint answers. Will supersede &#39;priority&#39; if provided. Mutually exclusive with &#39;app&#39;. | [optional]
 **app** | **str**| The application that is subscribed to the originated channel. When the channel is answered, it will be passed to this Stasis application. Mutually exclusive with &#39;context&#39;, &#39;extension&#39;, &#39;priority&#39;, and &#39;label&#39;. | [optional]
 **app_args** | **str**| The application arguments to pass to the Stasis application provided by &#39;app&#39;. Mutually exclusive with &#39;context&#39;, &#39;extension&#39;, &#39;priority&#39;, and &#39;label&#39;. | [optional]
 **caller_id** | **str**| CallerID to use when dialing the endpoint or extension. | [optional]
 **timeout** | **int**| Timeout (in seconds) before giving up dialing, or -1 for no timeout. | [optional] [default to 30]
 **channel_id** | **str**| The unique id to assign the channel on creation. | [optional]
 **other_channel_id** | **str**| The unique id to assign the second channel when using local channels. | [optional]
 **originator** | **str**| The unique id of the channel which is originating this one. | [optional]
 **formats** | **str**| The format name capability list to use if originator is not specified. Ex. \&quot;ulaw,slin16\&quot;.  Format names can be found with \&quot;core show codecs\&quot;. | [optional]
 **x_asterisk_id** | **str**|  | [optional]
 **containers** | [**Containers**](Containers.md)| The \&quot;variables\&quot; key in the body object holds variable key/value pairs to set on the channel on creation. Other keys in the body object are interpreted as query parameters. Ex. { \&quot;endpoint\&quot;: \&quot;SIP/Alice\&quot;, \&quot;variables\&quot;: { \&quot;CALLERID(name)\&quot;: \&quot;Alice\&quot; } } | [optional]

### Return type

[**Channel**](Channel.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response was specified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
