package restclient

import (
	"context"
	"fmt"
)

type BackendsService service

type LDAPBackendConfig struct {
	BindDN            *string `json:"bind_dn,omitempty"`
	Host              *string `json:"host,omitempty"`
	Port              *int    `json:"port,omitempty"`
	ProtocolSecurity  *string `json:"protocol_security,omitempty"`
	ProtocolVersion   *int    `json:"protocol_version,omitempty"`
	SearchFilters     *string `json:"search_filters,omitempty"`
	UserBaseDN        *string `json:"user_base_dn,omitempty"`
	UserEmailAttribute *string `json:"user_email_attribute,omitempty"`
	UserLoginAttribute *string `json:"user_login_attribute,omitempty"`
	BindPassword      *string `json:"bind_password,omitempty"`
}


// Delete current tenant's LDAP backend configuration
// Authorizations accent_auth_token
// Header Params Accent-Tenant The tenant's UUID, defining the ownership of a given resource.
// Response 204 The LDAP backend configuration has been deleted
/* Response 401 Unauthorized {
  "reason": [
    "string"
  ],
  "status_code": 0,
  "timestamp": [
    "string"
  ]
}
*/
func (s *BackendsService) DeleteLdap(ctx context.Context, tenantUUID string) (*Response, error) {
	url := fmt.Sprintf("api/auth/0.1/backends/ldap")
	req, err := s.client.NewRequest("DELETE", url, nil)
	if err != nil {
		return nil, err
	}

	resp, err := s.client.Do(ctx, req, nil)
	if err != nil {
		return resp, err
	}

	return resp, nil
}


// Get backends Retrieves the list of activated backends
// No parameters
// Response 200 The list of activated backends
/*
{
  "data": [
    "string"
  ]
}
*/
func (s *BackendsService) GetBackends(ctx context.Context) (*Response, error) {
	url := fmt.Sprintf("api/auth/0.1/backends")
	req, err := s.client.NewRequest("GET", url, nil)
	if err != nil {
		return nil, err
	}

	resp, err := s.client.Do(ctx, req, nil)
	if err != nil {
		return resp, err
	}

	return resp, nil
}


// Get current tenant's LDAP backend configuration.  If there is no configuration
// all the fields will be 'null'
// Parameters Accent-Tenant The tenant's UUID, defining the ownership of a given resource.
/*
Response 200
{
  "bind_dn": "CN=accent-auth,DC=accent-platform,DC=org",
  "host": "string",
  "port": 389,
  "protocol_security": "",
  "protocol_version": 3,
  "search_filters": "{user_login_attribute}={username}",
  "tenant_uuid": "string",
  "user_base_dn": "OU=people,DC=accent-platform,DC=org",
  "user_email_attribute": "mail",
  "user_login_attribute": "uid"
}
*/
/*
Response 401 Unauthorized
{
  "reason": [
    "string"
  ],
  "status_code": 0,
  "timestamp": [
    "string"
  ]
}
*/
func (s *BackendsService) GetLdap(ctx context.Context, tenantUUID string) (*Response, error) {
	url := fmt.Sprintf("api/auth/0.1/backends/ldap")
	req, err := s.client.NewRequest("GET", url, nil)
	if err != nil {
		return nil, err
	}

	resp, err := s.client.Do(ctx, req, nil)
	if err != nil {
		return resp, err
	}

	return resp, nil
}

// Put /backends/ldap
// Update current tenant's LDAP backend configuration
// Authorizations Accent-Tenant The tenant's UUID, defining the ownership of a given resource.
// The LDAP backend configuration body is required to specify the configuration
// Response 200 The LDAP backend configuration has been updated response with the updated configuration
/*
{
  "bind_dn": "CN=accent-auth,DC=accent-platform,DC=org",
  "host": "string",
  "port": 389,
  "protocol_security": "",
  "protocol_version": 3,
  "search_filters": "{user_login_attribute}={username}",
  "tenant_uuid": "string",
  "user_base_dn": "OU=people,DC=accent-platform,DC=org",
  "user_email_attribute": "mail",
  "user_login_attribute": "uid"
}
*/

/* Response 401 Unauthorized {
	"reason": [
		"string"
	],
	"status_code": 0,
	"timestamp": [
		"string"
	]
}
*/
func (s *BackendsService) PutLdap(ctx context.Context, tenantUUID string, body *LDAPBackendConfig) (*Response, error) {
	url := fmt.Sprintf("api/auth/0.1/backends/ldap")
	req, err := s.client.NewRequest("PUT", url, body)
	if err != nil {
		return nil, err
	}

	resp, err := s.client.Do(ctx, req, nil)
	if err != nil {
		return resp, err
	}

	return resp, nil
}

