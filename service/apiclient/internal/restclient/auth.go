package restclient

import (
	"context"
	"fmt"
)

type AuthService service

type Auth struct{
	// Token *string `json:"data,token"`
}

func (u Auth) String() string {
	return Stringify(u)
}

//meta:operation GET /user
//meta:operation GET /users/{username}
func (s *AuthService) Post(ctx context.Context, token string) (*Auth, *Response, error) {
	var u string
	if token != "" {
		u = fmt.Sprintf("api/auth/0.1/token/%v", token)
	} else {
		u = "/api/auth/0.1/token"
	}
	req, err := s.client.NewRequest("POST", u, nil)
	if err != nil {
		return nil, nil, err
	}

	uResp := new(Auth)
	resp, err := s.client.Do(ctx, req, uResp)
	if err != nil {
		return nil, resp, err
	}

	return uResp, resp, nil
}
