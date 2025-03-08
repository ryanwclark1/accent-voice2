// package restclient

// import (
// 	"context"
// 	"fmt"
// )

// type TokenService service

// type TokenData struct {
// 	Data Token `json:"data,omitempty"`
// }

// type Token struct {
// 	Token          *string        `json:"token,omitempty"`
// 	AuthID         *string        `json:"auth_id,omitempty"`
// 	AccentUserUUID *string        `json:"accent_user_uuid,omitempty"`
// 	AccentUUID     *string        `json:"accent_uuid,omitempty"`
// 	IssuedAt       *string        `json:"issued_at,omitempty"`
// 	ExpiresAt      *string        `json:"expires_at,omitempty"`
// 	UTCIssuedAt    *string        `json:"utc_issued_at,omitempty"`
// 	UTCExpiresAt   *string        `json:"utc_expires_at,omitempty"`
// 	ACL            []*string      `json:"acl,omitempty"`
// 	SessionUUID    *string        `json:"session_uuid,omitempty"`
// 	RemoteAddr     *string        `json:"remote_addr,omitempty"`
// 	UserAgent      *string        `json:"user_agent,omitempty"`
// 	Metadata       *TokenMetadata `json:"metadata,omitempty"`
// }

// type TokenMetadata struct {
// 	UUID        *string `json:"uuid,omitempty"`
// 	TenantUUID  *string `json:"tenant_uuid,omitempty"`
// 	AuthID      *string `json:"auth_id,omitempty"`
// 	PBXUserUUID *string `json:"pbx_user_uuid,omitempty"`
// 	AccentUUID  *string `json:"accent_uuid,omitempty"`
// 	Purpose     *string `json:"purpose,omitempty"`
// 	Admin       *bool   `json:"admin,omitempty"`
// }

// type TokenBody struct {
// 	AccessType   *string `json:"access_type,omitempty"` // online or offline
// 	Backend      *string `json:"backend,omitempty"`
// 	Expiration   *int    `json:"expiration,omitempty"` // Maximum 315360000
// 	RefreshToken *string `json:"refresh_token,omitempty"`
// 	ClientID     *string `json:"client_id,omitempty"` // Required when offline refresh token
// }

// // Struct for a user's refresh token list
// type RefreshTokenList struct {
// 	Filtered *int
// 	Items 	[]*RefreshToken
// 	Total 	*int
// }

// // Struct for a user's refresh token
// type RefreshToken struct {
// 	ClientID 		*string
// 	CreatedAt 		*string
// 	Mobile 			*bool
// 	TenantUUID 		*string
// 	UserUUID 		*string
// }

// func (t TokenData) String() string {
// 	return Stringify(t)
// }

// func (t Token) String() string {
// 	return Stringify(t)
// }

// func (t TokenMetadata) String() string {
// 	return Stringify(t)
// }

// func (t TokenBody) String() string {
// 	return Stringify(t)
// }

// func (r RefreshTokenList) String() string {
// 	return Stringify(r)
// }

// func (r RefreshToken) String() string {
// 	return Stringify(r)
// }

// type QueryParams struct {
// 	Order     *string `url:"order,omitempty"`
// 	Direction *string `url:"direction,omitempty"`
// 	Limit     *int    `url:"limit,omitempty"`
// 	Offset    *int    `url:"offset,omitempty"`
// 	Search    *string `url:"search,omitempty"`
// 	Recurse   *bool   `url:"recurse,omitempty"`
// }

// type HeadParams struct {
// 	AccentTenant *string `url:"Accent-Tenant,omitempty"`
// }

// // TokenBasicAuth is a Token Service function utilizes the context username and password to authenticate and return a Token struct.
// // Can taken the TokenBody as body parameter to specify the access type, backend, and expiration.
// func (s *TokenService) TokenBasicAuth(ctx context.Context, username, password string, body *TokenBody) (*TokenData, *Response, error) {
// 	req, err := s.client.NewRequest("POST", "api/auth/0.1/token", body)
// 	if err != nil {
// 		return nil, nil, err
// 	}

// 	req.SetBasicAuth(username, password)

// 	tokendata := new(TokenData)
// 	resp, err := s.client.Do(ctx, req, tokendata)
// 	if err != nil {
// 		return nil, resp, err
// 	}

// 	return tokendata, resp, nil
// }

// // TokenDelete revokes a token.  Should use /0.1/token/{token}
// func (s *TokenService) TokenDelete(ctx context.Context, token string) (*Response, error) {
// 	url := fmt.Sprintf("api/auth/0.1/token/%s", token)
// 	req, err := s.client.NewRequest("DELETE", url, nil)
// 	if err != nil {
// 		return nil, err
// 	}

// 	resp, err := s.client.Do(ctx, req, nil)
// 	if err != nil {
// 		return resp, err
// 	}

// 	return resp, nil
// }

// // Check if a token is valid against given scopes.  Should use /0.1/token/{token}/scopes/check/  The body is requred to specify the scopes, as an array of strings.  The tenant_uuid is optional.  The responses are 200 with an array of objects the scopes and their check result, 400 if the provided scope list is invalud, with a reason (array of strings status_code integer and timestamp array of strings,  403 this token is not valid for the provided tenant  with a reason (array of strings status_code integer and timestamp array of strings, 404 if the token is not found with a reason (array of strings status_code integer and timestamp array of strings, 500 if an internal error occurs with a reason (array of strings status_code integer and timestamp array of strings, and lastly 500 if an internal error occurs with a reason (array of strings status_code integer and timestamp array of strings.

// func (s *TokenService) TokenScopesCheck(ctx context.Context, token string, body *TokenBody) (*Response, error) {
// 	url := fmt.Sprintf("api/auth/0.1/token/%s/scopes/check/", token)
// 	req, err := s.client.NewRequest("POST", url, body)
// 	if err != nil {
// 		return nil, err
// 	}

// 	resp, err := s.client.Do(ctx, req, nil)
// 	if err != nil {
// 		return resp, err
// 	}

// 	return resp, nil
// }

// // Checks if a token is valid in a given context. If a scope is given, the token must have the necessary permissions for the ACL. If a tenant is given, the token must have that tenant in its sub-tenant subtree.  Head request to /0.1/token/{token}  The responses are 200 if the token is valid, 403 if the token is not valid for the provided tenant, 404 if the token is not found, 500 if an internal error occurs.

// func (s *TokenService) TokenCheck(ctx context.Context, token string) (*Response, error) {
// 	url := fmt.Sprintf("api/auth/0.1/token/%s", token)
// 	req, err := s.client.NewRequest("HEAD", url, nil)
// 	if err != nil {
// 		return nil, err
// 	}

// 	resp, err := s.client.Do(ctx, req, nil)
// 	if err != nil {
// 		return resp, err
// 	}

// 	return resp, nil
// }

// // Finds all of a user's refresh token and return the list. Access tokens are not included in the result.
// //  Doing a query with the user_uuid me will result in the current user's token being used.
// // Query parameters are order, direction, limit, offset, and search
// // Head Parameters are Accent-Tenant which is the tenant_uuid

// func (s *TokenService) TokenRefreshList(ctx context.Context, user_uuid string, params *QueryParams, headParams *HeadParams) (*RefreshTokenList, *Response, error) {
// 	url := fmt.Sprintf("api/auth/0.1/token/users/%s/tokens", user_uuid)
// 	req, err := s.client.NewRequest("GET", url, nil)
// 	if err != nil {
// 		return nil, nil, err
// 	}

// 	if params != nil {
// 		req.URL.RawQuery = params.Values().Encode()
// 	}

// 	if headParams != nil {
// 		req.Header.Set("Accent-Tenant", *headParams.AccentTenant)
// 	}

// 	refreshTokenList := new(RefreshTokenList)
// 	resp, err := s.client.Do(ctx, req, refreshTokenList)
// 	if err != nil {
// 		return nil, resp, err
// 	}

// 	return refreshTokenList, resp, nil
// }

// //  inds all refresh tokens and return the list. Access tokens are not included in the result.
// // Query parameters are recurse, order, direction, limit, offset, and search
// // Head Parameters are Accent-Tenant which is the tenant_uuid

// func (s *TokenService) TokenRefreshListAll(ctx context.Context, params *QueryParams, headParams *HeadParams) (*RefreshTokenList, *Response, error) {
// 	url := fmt.Sprintf("api/auth/0.1/token/tokens")
// 	req, err := s.client.NewRequest("GET", url, nil)
// 	if err != nil {
// 		return nil, nil, err
// 	}

// 	if params != nil {
// 		req.URL.RawQuery = params.Values().Encode()
// 	}

// 	if headParams != nil {
// 		req.Header.Set("Accent-Tenant", *headParams.AccentTenant)
// 	}

// 	refreshTokenList := new(RefreshTokenList)
// 	resp, err := s.client.Do(ctx, req, refreshTokenList)
// 	if err != nil {
// 		return nil, resp, err
// 	}

// 	return refreshTokenList, resp, nil
// }
package restclient

