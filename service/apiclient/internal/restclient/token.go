package restclient

import (
	"context"
	"fmt"
	"net/url"
)

type TokenService service

type TokenResponse struct {
    Data Token `json:"data"`
}

type Token struct {
	Token          *string        `json:"token,omitempty"`
	AuthID         *string        `json:"auth_id,omitempty"`
	AccentUserUUID *string        `json:"accent_user_uuid,omitempty"`
	AccentUUID     *string        `json:"accent_uuid,omitempty"`
	IssuedAt       *string        `json:"issued_at,omitempty"`
	ExpiresAt      *string        `json:"expires_at,omitempty"`
	UTCIssuedAt    *string        `json:"utc_issued_at,omitempty"`
	UTCExpiresAt   *string        `json:"utc_expires_at,omitempty"`
	ACL            []*string      `json:"acl,omitempty"`
	SessionUUID    *string        `json:"session_uuid,omitempty"`
	RemoteAddr     *string        `json:"remote_addr,omitempty"`
	UserAgent      *string        `json:"user_agent,omitempty"`
	Metadata       *TokenMetadata `json:"metadata,omitempty"`
}

type TokenMetadata struct {
	UUID        *string `json:"uuid,omitempty"`
	TenantUUID  *string `json:"tenant_uuid,omitempty"`
	AuthID      *string `json:"auth_id,omitempty"`
	PBXUserUUID *string `json:"pbx_user_uuid,omitempty"`
	AccentUUID  *string `json:"accent_uuid,omitempty"`
	Purpose     *string `json:"purpose,omitempty"`
	Admin       *bool   `json:"admin,omitempty"`
}

// TokenRequestParams specifies the parameters for creating a new token.
type TokenRequestParams struct {
	AccessType    string `json:"access_type,omitempty"`
	Backend       string `json:"backend,omitempty"`
	ClientID      string `json:"client_id,omitempty"`
	DomainName    string `json:"domain_name,omitempty"`
	Expiration    int    `json:"expiration,omitempty"`
	RefreshToken  string `json:"refresh_token,omitempty"`
	Username      string `json:"username,omitempty"`
	Password      string `json:"password,omitempty"`
}

// func (t TokenResponse) String() string {
// 	return Stringify(t)
// }

func (t Token) String() string {
	return Stringify(t)
}

/*
  /token:
    post:
      consumes:
      - application/json
      description: 'Creates a valid token for the supplied username and password combination
        or refresh_token

        using the specified backend.


        The user''s email address can be used instead of the username if the email
        address is confirmed.


        The stock backends are: ``accent_user``, ``ldap_user``.


        Creating  a token with the `access_type` *offline* will also create a refresh
        token which can be used

        to create a new token without specifying the username and password.


        The username/password and refresh_token method of authentication are mutually
        exclusive


        For more details about the backends, see http://documentation.accent.community/en/latest/system/accent-auth/stock_plugins.html#backends-plugins

        '
      operationId: createToken
      parameters:
      - $ref: '#/parameters/accent_session_type'
      - description: The token creation parameters
        in: body
        name: body
        required: false
        schema:
          properties:
            access_type:
              default: online
              description: 'The `access_type` indicates whether your application can
                refresh the tokens when the user is not

                present at the browser. Valid parameter values are *online*, which
                is the default value, and *offline*


                Only one refresh token will be created for a given user with a given
                `client_id`. The old refresh

                for `client_id` will be revoken when creating a new one.


                The *client_id* field is required when using the `access_type` *offline*

                '
              enum:
              - online
              - offline
              type: string
            backend:
              default: accent_user
              type: string
            client_id:
              description: 'The `client_id` is used in conjunction with the `access_type`
                *offline* to known for which application

                a refresh token has been emitted.


                *Required when using `access_type: offline`*

                '
              type: string
            domain_name:
              description: 'The `domain_name` must match a tenant''s domain_name entry
                to find the appropriate ldap configuration.

                '
              type: string
            expiration:
              default: 7200
              description: Expiration time in seconds.
              maximum: 315360000
              type: integer
            refresh_token:
              description: 'The `refresh_token` can be used to get a new access token
                without using the username/password.

                This is useful for client application that should not store the username
                and password once the

                user has logged in a first time.

                '
              type: string
          type: object
      produces:
      - application/json
      responses:
        '200':
          description: The created token's data
          schema:
            $ref: '#/definitions/Token'
        '400':
          description: Invalid expiration or missing field
          schema:
            $ref: '#/definitions/Error'
        '500':
          description: System related token generation error
          schema:
            $ref: '#/definitions/Error'
      security:
      - accent_auth_basic: []
      summary: Creates a token
      tags:
      - token

			accent_session_type:
    description: The session type
    enum:
    - mobile
    - desktop
    in: header
    name: Accent-Session-Type
    required: false
    type: string


		Token:
    properties:
      data:
        properties:
          acl:
            description: The list of allowed accesses for this token
            items:
              type: string
            type: array
          auth_id:
            description: The unique identifier retrieved from the backend
            type: string
          expires_at:
            type: string
          issued_at:
            type: string
          metadata:
            description: Information owned by accent-auth about this user
            type: object
          session_uuid:
            type: string
          token:
            type: string
          utc_expires_at:
            type: string
          utc_issued_at:
            type: string
          accent_user_uuid:
            description: 'The UUID of the matching accent-confd user if there is one.
              This

              field can be null.


              This field should NOT be used anymore, the "pbx_user_uuid" in the

              metadata field is the prefered method to access this information.

              '
            type: string
          accent_uuid:
            type: string
        type: object
    type: object

			*/


// CreateToken creates a new token based on the provided parameters.
func (s *TokenService) CreateToken(ctx context.Context, params *TokenRequestParams) (*Token, *Response, error) {
	// Validate mutual exclusivity of Username/Password and RefreshToken
    if (params.Username != "" || params.Password != "") && params.RefreshToken != "" {
        return nil, nil, fmt.Errorf("username/password and refresh_token methods of authentication are mutually exclusive")
    }

    // If using Username and Password, ensure both are provided
    if (params.Username != "" || params.Password != "") && (params.Username == "" || params.Password == "") {
        return nil, nil, fmt.Errorf("both username and password must be provided for basic authentication")
    }

	prefix_path := "api/auth/0.1/"
	suffix_path := "token"
	u := fmt.Sprintf("%s%s", prefix_path, suffix_path)
	// Since this is a POST request, the body should be included.
	// Note: The API might require setting specific headers or other authentication methods.
	req, err := s.client.NewRequest("POST", u, params)
	if err != nil {
		return nil, nil, err
	}

	// Set any necessary headers here. For example, if session type is required:
	// req.Header.Set("Accent-Session-Type", "desktop")
	if params.Username != "" && params.Password != "" {
		req.SetBasicAuth(params.Username, params.Password)
  }

	tokenResp := new(TokenResponse)
	resp, err := s.client.Do(ctx, req, tokenResp)
	if err != nil {
		return nil, resp, err
	}

	return &tokenResp.Data, resp, nil
}



/*
  /token/{token}:
    delete:
      parameters:
      - $ref: '#/parameters/token'
      responses:
        '200':
          description: Success message
        '500':
          description: System related token error
          schema:
            $ref: '#/definitions/Error'
      security:
      - {}
      summary: Revoke a token
      tags:
      - token
    get:
      description: Checks if a token is valid in a given context and return the token
        data.  If a scope is given, the token must have the necessary permissions
        for the ACL. If a tenant is given, the token must have that tenant in its
        sub-tenant subtree.
      parameters:
      - $ref: '#/parameters/token'
      - $ref: '#/parameters/scope'
      - $ref: '#/parameters/tenant'
      responses:
        '200':
          description: The token's data
          schema:
            $ref: '#/definitions/Token'
        '403':
          description: This token cannot acces the required ACL
          schema:
            $ref: '#/definitions/Error'
        '404':
          description: Token not found
          schema:
            $ref: '#/definitions/Error'
        '500':
          description: System related token error
          schema:
            $ref: '#/definitions/Error'
      security:
      - {}
      summary: Retrieves token data
      tags:
      - token
    head:
      description: Checks if a token is valid in a given context.  If a scope is given,
        the token must have the necessary permissions for the ACL. If a tenant is
        given, the token must have that tenant in its sub-tenant subtree.
      parameters:
      - $ref: '#/parameters/token'
      - $ref: '#/parameters/scope'
      - $ref: '#/parameters/tenant'
      responses:
        '204':
          description: No data
        '403':
          description: This token cannot acces the required ACL
          schema:
            $ref: '#/definitions/Error'
        '404':
          description: Token not found
          schema:
            $ref: '#/definitions/Error'
        '500':
          description: System related token error
          schema:
            $ref: '#/definitions/Error'
      security:
      - {}
      summary: Checks if a token is valid
      tags:
      - token

  token:
    description: The token to query
    in: path
    name: token
    required: true
    type: string

  scope:
    description: The required ACL
    in: query
    name: scope
    required: false
    type: string

  tenant:
    description: A tenant UUID to check against
    in: query
    name: tenant
    required: false
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

		Token:
    properties:
      data:
        properties:
          acl:
            description: The list of allowed accesses for this token
            items:
              type: string
            type: array
          auth_id:
            description: The unique identifier retrieved from the backend
            type: string
          expires_at:
            type: string
          issued_at:
            type: string
          metadata:
            description: Information owned by accent-auth about this user
            type: object
          session_uuid:
            type: string
          token:
            type: string
          utc_expires_at:
            type: string
          utc_issued_at:
            type: string
          accent_user_uuid:
            description: 'The UUID of the matching accent-confd user if there is one.
              This

              field can be null.


              This field should NOT be used anymore, the "pbx_user_uuid" in the

              metadata field is the prefered method to access this information.

              '
            type: string
          accent_uuid:
            type: string
        type: object
    type: object
*/

// RevokeToken revokes an existing token.
func (s *TokenService) RevokeToken(ctx context.Context, token string) (*Response, error) {
	u := fmt.Sprintf("token/%s", token)
	req, err := s.client.NewRequest("DELETE", u, nil)
	if err != nil {
		return nil, err
	}

	return s.client.Do(ctx, req, nil)
}

// GetToken retrieves token data, checking its validity in a given context.
func (s *TokenService) GetToken(ctx context.Context, token, scope, tenant string) (*Token, *Response, error) {
	u := fmt.Sprintf("token/%s", token)
	// Add query parameters for scope and tenant if provided
	queryParams := url.Values{}
	if scope != "" {
		queryParams.Add("scope", scope)
	}
	if tenant != "" {
		queryParams.Add("tenant", tenant)
	}
	if len(queryParams) > 0 {
		u = fmt.Sprintf("%s?%s", u, queryParams.Encode())
	}

	req, err := s.client.NewRequest("GET", u, nil)
	if err != nil {
		return nil, nil, err
	}

	tokenResp := new(TokenResponse)
	resp, err := s.client.Do(ctx, req, tokenResp)
	if err != nil {
		return nil, resp, err
	}

	return &tokenResp.Data, resp, nil
}

// CheckTokenValidity checks if a token is valid in a given context.
func (s *TokenService) CheckTokenValidity(ctx context.Context, token, scope, tenant string) (*Response, error) {
	u := fmt.Sprintf("token/%s", token)
	// Add query parameters for scope and tenant if provided
	queryParams := url.Values{}
	if scope != "" {
		queryParams.Add("scope", scope)
	}
	if tenant != "" {
		queryParams.Add("tenant", tenant)
	}
	if len(queryParams) > 0 {
		u = fmt.Sprintf("%s?%s", u, queryParams.Encode())
	}

	req, err := s.client.NewRequest("HEAD", u, nil)
	if err != nil {
		return nil, err
	}

	return s.client.Do(ctx, req, nil)
}
