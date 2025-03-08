# accent-confd-cli
CLI tool to inspect and update accent-confd resources


## Example usage

### Listing resources

```shell
export TOKEN=$(accent-auth-cli token create --auth-username <username> --auth-password = <password>)
accent-confd-cli --token ${TOKEN} user list --tenant <tenant-uuid>
```


### Associating resources

```shell
accent-confd-cli --token ${TOKEN} endpoint sip add --template <template-uuid> <endpoint-uuid>
```
