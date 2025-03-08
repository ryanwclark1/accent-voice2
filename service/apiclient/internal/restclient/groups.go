package restclient

import (
	"context"
	"fmt"
)

type GroupsService service

type Group struct {
	Name         *string `json:"name,omitempty"`
	Slug         *string `json:"slug,omitempty"`
}


/*
/groups:
    get:
      description: '**Required ACL:** `auth.groups.read`'
      operationId: listGroups
      parameters:
      - $ref: '#/parameters/tenantuuid'
      - $ref: '#/parameters/recurse'
      - $ref: '#/parameters/order'
      - $ref: '#/parameters/direction'
      - $ref: '#/parameters/limit'
      - $ref: '#/parameters/offset'
      - $ref: '#/parameters/search'
      - $ref: '#/parameters/search_uuid'
      - $ref: '#/parameters/search_name'
      - $ref: '#/parameters/search_user_uuid'
      - $ref: '#/parameters/search_read_only'
      - $ref: '#/parameters/search_policy_slug'
      - $ref: '#/parameters/search_policy_uuid'
      produces:
      - application/json
      responses:
        '200':
          description: A list of group
          schema:
            $ref: '#/definitions/GetGroupsResult'
        '401':
          description: Unauthorized
          schema:
            $ref: '#/definitions/Error'
      security:
      - accent_auth_token: []
      summary: List groups
      tags:
      - groups
    post:
      consumes:
      - application/json
      description: '**Required ACL:** `auth.groups.create`'
      operationId: createGroups
      parameters:
      - $ref: '#/parameters/tenantuuid'
      - description: The group creation parameters
        in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/Group'
      produces:
      - application/json
      responses:
        '200':
          description: The created group's data
          schema:
            $ref: '#/definitions/GroupResult'
        '401':
          description: Invalid data has been supplied'
          schema:
            $ref: '#/definitions/Error'
        '409':
          description: Duplicate Group
          schema:
            $ref: '#/definitions/Error'
      security:
      - accent_auth_token: []
      summary: Create a new group
      tags:
      - groups

  GroupResult:
    properties:
      name:
        type: string
      read_only:
        type: boolean
      slug:
        type: string
      system_managed:
        description: '*Deprecated* Please use `read_only`'
        type: boolean
      tenant_uuid:
        type: string
      uuid:
        type: string
    type: object

		  Group:
    properties:
      name:
        type: string
      slug:
        default: <name>
        type: string
    required:
    - name
    type: object

*/
func (s *GroupsService) GroupList(ctx context.Context) (*Response, error) {
	url := fmt.Sprintf("api/auth/0.1/groups")
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


func (s *GroupsService) GroupCreate(ctx context.Context, body *Group) (*Response, error) {
	url := fmt.Sprintf("api/auth/0.1/groups")
	req, err := s.client.NewRequest("POST", url, body)
	if err != nil {
		return nil, err
	}

	resp, err := s.client.Do(ctx, req, nil)
	if err != nil {
		return resp, err
	}

	return resp, nil
}
