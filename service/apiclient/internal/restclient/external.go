package restclient

import (
	"context"
	"fmt"
)

type ExternalService service

type ExternalConfig struct {
	ClientID         *string `json:"client_id,omitempty"`
	ClientSecret     *string `json:"client_secret,omitempty"`
	FCMApiKey				*string `json:"fcm_api_key,omitempty"`
	IOSAPNCertificate	*string `json:"ios_apn_certificate,omitempty"`
	IOSAPNPrivate		*string `json:"ios_apn_private,omitempty"`
	UseSandbox			*bool `json:"use_sandbox,omitempty"`
}


/*
  /external/{auth_type}/config:
    delete:
      description: '**Required ACL**: `auth.{auth_type}.external.config.delete`'
      parameters:
      - $ref: '#/parameters/tenantuuid'
      - $ref: '#/parameters/auth_type'
      responses:
        '204':
          description: Deletion confirmed
        '401':
          description: Unauthorized
          schema:
            $ref: '#/definitions/Error'
        '404':
          description: Not found
          schema:
            $ref: '#/definitions/Error'
      summary: Delete the client id and client secret
      tags:
      - external
    get:
      description: '**Required ACL**: `auth.{auth_type}.external.config.read`'
      parameters:
      - $ref: '#/parameters/tenantuuid'
      - $ref: '#/parameters/auth_type'
      responses:
        '200':
          description: The requested config
          schema:
            $ref: '#/definitions/ExternalConfig'
        '401':
          description: Unauthorized
          schema:
            $ref: '#/definitions/Error'
        '404':
          description: Not found
          schema:
            $ref: '#/definitions/Error'
      summary: Retrieve the client id and client secret
      tags:
      - external
    post:
      description: '**Required ACL**: `auth.{auth_type}.external.config.create`'
      parameters:
      - $ref: '#/parameters/tenantuuid'
      - $ref: '#/parameters/auth_type'
      - description: JSON object holding configuration for the given authentication
          type
        in: body
        name: config
        required: true
        schema:
          $ref: '#/definitions/ExternalConfig'
      responses:
        '201':
          description: Config created
        '401':
          description: Unauthorized
          schema:
            $ref: '#/definitions/Error'
        '404':
          description: Not found
          schema:
            $ref: '#/definitions/Error'
        '409':
          description: Duplicate config
          schema:
            $ref: '#/definitions/Error'
      summary: Add configuration for the given auth_type
      tags:
      - external
    put:
      description: '**Required ACL**: `auth.{auth_type}.external.config.edit`'
      parameters:
      - $ref: '#/parameters/tenantuuid'
      - $ref: '#/parameters/auth_type'
      - description: JSON object holding configuration for the given authentication
          type
        in: body
        name: config
        required: true
        schema:
          $ref: '#/definitions/ExternalConfig'
      responses:
        '201':
          description: Config created
        '401':
          description: Unauthorized
          schema:
            $ref: '#/definitions/Error'
        '404':
          description: Not found
          schema:
            $ref: '#/definitions/Error'
      summary: Update configuration for the given auth_type
      tags:
      - external

			  tenantuuid:
    description: The tenant's UUID, defining the ownership of a given resource.
    in: header
    name: Accent-Tenant
    required: false
    type: string

		  auth_type:
    description: External auth type name
    in: path
    name: auth_type
    required: true
    type: string

		  Error:
    properties:
      reason:
        items:
          type: string
        type: array
      status_code:
        type: integer
      timestamp:
        items:
          type: string
        type: array
    type: object


		  ExternalConfig:
    properties:
      client_id:
        description: 'Client ID for the given authentication type.

          Required only for `google` and `microsoft` authentication types.

          '
        example: a-client-id
        type: string
      client_secret:
        description: 'Client secret for the given authentication type.

          Required only for `google` and `microsoft` authentication types.

          '
        example: a-client-secret
        type: string
      fcm_api_key:
        description: The API key to use for Firebase Cloud Messaging
        type: string
      ios_apn_certificate:
        description: Public certificate to use for Apple Push Notification Service
        type: string
      ios_apn_private:
        description: Private key to use for Apple Push Notification Service
        type: boolean
      use_sandbox:
        description: Whether to use sandbox for Apple Push Notification Service
        type: boolean
    type: object




*/

func (s *ExternalService) ExternalConfigDelete(ctx context.Context, tenantUUID string, authType string) (*Response, error) {
	url := fmt.Sprintf("api/auth/0.1/external/%s/config", authType)
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

func (s *ExternalService) ExternalConfigGet(ctx context.Context, tenantUUID string, authType string) (*Response, error) {
	url := fmt.Sprintf("api/auth/0.1/external/%s/config", authType)
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

func (s *ExternalService) ExternalConfigPost(ctx context.Context, tenantUUID string, authType string, config ExternalConfig) (*Response, error) {
	url := fmt.Sprintf("api/auth/0.1/external/%s/config", authType)
	req, err := s.client.NewRequest("POST", url, config)
	if err != nil {
		return nil, err
	}

	resp, err := s.client.Do(ctx, req, nil)
	if err != nil {
		return resp, err
	}

	return resp, nil
}

func (s *ExternalService) ExternalConfigPut(ctx context.Context, tenantUUID string, authType string, config ExternalConfig) (*Response, error) {
	url := fmt.Sprintf("api/auth/0.1/external/%s/config", authType)
	req, err := s.client.NewRequest("PUT", url, config)
	if err != nil {
		return nil, err
	}

	resp, err := s.client.Do(ctx, req, nil)
	if err != nil {
		return resp, err
	}

	return resp, nil
}

/*

/external/{auth_type}/users:
    get:
      description: '**Required ACL**: `auth.{auth_type}.external.users`'
      parameters:
      - $ref: '#/parameters/tenantuuid'
      - $ref: '#/parameters/auth_type'
      - $ref: '#/parameters/recurse'
      - $ref: '#/parameters/limit'
      - $ref: '#/parameters/offset'
      responses:
        '200':
          description: The list of external auth connected users
          schema:
            $ref: '#/definitions/ExternalAuthUserList'
        '401':
          description: Unauthorized
          schema:
            $ref: '#/definitions/Error'
        '404':
          description: Not found
          schema:
            $ref: '#/definitions/Error'
      summary: Retrieves the list of connected users to this external source
      tags:
      - external

    ExternalAuthUserList:
    properties:
      filtered:
        description: The number of external auth matching the searched term.
        example: 3
        type: integer
      items:
        description: A paginated list of connected external auth users
        example:
        - user_uuid: 210ef281-4201-4f95-952f-5f8d5211e085
        - user_uuid: 28e6f253-a19d-458d-8b52-2ba6feb788bc
        - user_uuid: e72fe53d-3981-4c51-a488-e06ca94fcbb1
        items:
          $ref: '#/definitions/ExternalAuthUser'
        type: array
      total:
        description: The number of connected external auth users.
        example: 3
        type: integer
    required:
    - filtered
    - total
    - items
    type: object
*/

func (s *ExternalService) ExternalUsersGet(ctx context.Context, tenantUUID string, authType string, recurse bool, limit int, offset int) (*Response, error) {
  url := fmt.Sprintf("api/auth/0.1/external/%s/users", authType)
  req, err := s.client.NewRequest("GET", url, nil)
  if err != nil {
    return nil, err
  }

  q := req.URL.Query()
  q.Add("recurse", fmt.Sprintf("%v", recurse))
  q.Add("limit", fmt.Sprintf("%d", limit))
  q.Add("offset", fmt.Sprintf("%d", offset))
  req.URL.RawQuery = q.Encode()

  resp, err := s.client.Do(ctx, req, nil)
  if err != nil {
    return resp, err
  }

  return resp, nil
}


/*
/users/{user_uuid}/external:
    get:
      description: '**Required ACL**: `auth.users.{user_uuid}.external.read`


        This list should not contain any sensible information

        '
      parameters:
      - $ref: '#/parameters/user_uuid'
      - $ref: '#/parameters/order'
      - $ref: '#/parameters/direction'
      - $ref: '#/parameters/limit'
      - $ref: '#/parameters/offset'
      - $ref: '#/parameters/search'
      responses:
        '200':
          description: The list of external auth data
          schema:
            $ref: '#/definitions/ExternalAuthList'
      security:
      - accent_auth_token: []
      summary: Retrieves the list of the users external auth data
      tags:
      - users
      - external
*/

func (s *ExternalService) UserExternalGet(ctx context.Context, userUUID string, order string, direction string, limit int, offset int, search string) (*Response, error) {
  url := fmt.Sprintf("api/auth/0.1/users/%s/external", userUUID)
  req, err := s.client.NewRequest("GET", url, nil)
  if err != nil {
    return nil, err
  }

  q := req.URL.Query()
  q.Add("order", order)
  q.Add("direction", direction)
  q.Add("limit", fmt.Sprintf("%d", limit))
  q.Add("offset", fmt.Sprintf("%d", offset))
  q.Add("search", search)
  req.URL.RawQuery = q.Encode()

  resp, err := s.client.Do(ctx, req, nil)
  if err != nil {
    return resp, err
  }

  return resp, nil
}
