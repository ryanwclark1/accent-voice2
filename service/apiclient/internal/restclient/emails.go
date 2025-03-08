package restclient

import (
	"context"
	"fmt"
)

type EmailsService service

type UserEmail struct {
	Address string `json:"address"`
	Confirmned bool `json:"confirmed"`
	Main    bool   `json:"main"`
}

/*
  /emails/{email_uuid}/confirm:
    get:
      description: '**Required ACL**: `auth.emails.{email_uuid}.confirm.edit`


        The token should be in the URL instead of being in the HTTP headers

        '
      parameters:
      - $ref: '#/parameters/email_uuid'
      - $ref: '#/parameters/email_confirm_token'
      responses:
        '200':
          description: The email address has been confirmed
        '404':
          description: Email not found
          schema:
            $ref: '#/definitions/Error'
      summary: Confirm an email address
      tags:
      - emails
    put:
      description: '**Required ACL**: `auth.emails.{email_uuid}.confirm.edit`'
      parameters:
      - $ref: '#/parameters/email_uuid'
      responses:
        '204':
          description: The email address has been confirmed
        '404':
          description: Email not found
          schema:
            $ref: '#/definitions/Error'
      security:
      - accent_auth_token: []
      summary: Confirm an email address
      tags:
      - emails

			  email_uuid:
    description: The UUID of the email
    in: path
    name: email_uuid
    required: true
    type: string

		  email_confirm_token:
    description: The UUID of the token used to confirm the email address
    in: query
    name: token
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
*/
func (s *EmailsService) EmailConfirm(ctx context.Context, emailUUID string, token string) (*Response, error) {
	url := fmt.Sprintf("api/auth/0.1/emails/%s/confirm?token=%s", emailUUID, token)
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

func (s *EmailsService) EmailConfirmPut(ctx context.Context, emailUUID string) (*Response, error) {
	url := fmt.Sprintf("api/auth/0.1/emails/%s/confirm", emailUUID)
	req, err := s.client.NewRequest("PUT", url, nil)
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
  /users/{user_uuid}/emails:
    put:
      description: '**Required ACL**: `auth.users.{user_uuid}.emails.edit`

        Update all of the users email address at the same time.

        If an existing address is missing from the list, it will be removed. An empty
        list will remove all addresses. If addresses are defined, one and only one
        address should be main. All new address are created unconfirmed. '
      parameters:
      - $ref: '#/parameters/user_uuid'
      - description: EmailAddressList
        in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/UserEmailList'
      responses:
        '200':
          description: The updated email list
        '404':
          description: User not found
          schema:
            $ref: '#/definitions/Error'
      security:
      - accent_auth_token: []
      summary: Update email addresses
      tags:
      - users
      - emails


  /users/{user_uuid}/emails/{email_uuid}/confirm:
    get:
      description: '**Required ACL**: `auth.users.{user_uuid}.emails.{email_uuid}.confirm.read`'
      parameters:
      - $ref: '#/parameters/user_uuid'
      - $ref: '#/parameters/email_uuid'
      responses:
        '204':
          description: The new email confirmation email has been sent
        '404':
          description: User or Email not found
          schema:
            $ref: '#/definitions/Error'
        '409':
          description: Already confirmed
      security:
      - accent_auth_token: []
      summary: Ask a new confirmation email
      tags:
      - users
      - emails


			  user_uuid:
    description: The UUID of the user
    in: path
    name: user_uuid
    required: true
    type: string

		  UserEmailList:
    properties:
      emails:
        items:
          properties:
            address:
              type: string
            main:
              type: boolean
          required:
          - addresses
          - main
          type: object
        type: array
    type: object

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

			*/

func (s *EmailsService) UserEmailsPut(ctx context.Context, userUUID string, emails []UserEmail) (*Response, error) {
	url := fmt.Sprintf("api/auth/0.1/users/%s/emails", userUUID)
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

func (s *EmailsService) UserEmailConfirm(ctx context.Context, userUUID string, emailUUID string) (*Response, error) {
	url := fmt.Sprintf("api/auth/0.1/users/%s/emails/%s/confirm", userUUID, emailUUID)
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
