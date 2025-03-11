# accent-lib-rest-client

TODO:
client.py:
- Stevedore Testing: Add tests for plugin loading.
- __del__: Consider a close() method.
- kwargs Handling: Be more explicit about allowed/disallowed kwargs. (May be difficult)
- Asynchronous Plugin Loading: Consider if _load_plugins() should be async.
command.py:
- Consider renaming CommandResponseType and JSONResponseType to simply CommandResponseAlias and JSONResponseAlias.
- Type Hinting in _get_headers: Use typing.Mapping[str, Any].
example_cmd.py:
- Make this example more illustrative by showing how to handle parameters