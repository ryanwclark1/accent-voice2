package restclient

import (
	"context"
	"fmt"
)

type AdminService service

type EmailAdress struct {
	Email   *string
}

type EmailAdressList struct {
	Emails []*EmailAdress `json:"emails,omitempty"`
}

// Update email addresses
// empty list will remove all addresses. If addresses are defined, one and only one address should be main. If the confirmed field is set to none or ommited the existing value will be reused if it exists, otherwise the address will not be confirmed.
// Authorization accent_auth_token
// Path Params user_uuid required String
// Request Body Schema EmailAdressList, emails required Array[EmailAdress]
// Resopnse 200 Schema EmailAdressList, the updated email list
// Response 404 Schema Error, user not found, reason (array of strings) status_code (integer) timestamp (array of strings)

func (s *AdminService) UpdateEmails(ctx context.Context, UserUUID string, emails []EmailAdress) (*Response, error) {
	url := fmt.Sprintf("api/auth/0.1/admin/%s/emails", UserUUID)
	req, err := s.client.NewRequest("PUT", url, emails)
	if err != nil {
		return nil, err
	}

	resp, err := s.client.Do(ctx, req, nil)
	if err != nil {
		return resp, err
	}

	return resp, nil
}
