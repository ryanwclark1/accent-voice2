package restclient

import (
	"context"
	"fmt"
)

type ConfigService service


type ConfigPatchItem struct {
	Op    *string `json:"op,omitempty"`
	Path  *string `json:"path,omitempty"`
	Value *string `json:"value,omitempty"`
}


/*
  /config:
    get:
      description: '**Required ACL:** `auth.config.read`'
      operationId: getConfig
      produces:
      - application/json
      responses:
        '200':
          description: The configuration of the service
      summary: Show the current configuration
      tags:
      - config
*/
func (s *ConfigService) Get(ctx context.Context) (*Response, error) {
	url := fmt.Sprintf("api/auth/0.1/config")
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

/*
    patch:
      description: '**Required ACL:** `auth.config.update`


        Changes are not persistent across service restart.

        '
      operationId: patchConfig
      parameters:
      - $ref: '#/parameters/ConfigPatch'
      produces:
      - application/json
      responses:
        '200':
          description: The updated configuration of the service
        '400':
          description: The given confiuration is invalid
      summary: Update the current configuration.
      tags:
      - config

			  ConfigPatch:
    description: See https://en.wikipedia.org/wiki/JSON_Patch.
    in: body
    name: ConfigPatch
    required: true
    schema:
      items:
        $ref: '#/definitions/ConfigPatchItem'
      type: array

			  ConfigPatchItem:
    properties:
      op:
        description: 'Patch operation. Supported operations: `replace`.'
        type: string
      path:
        description: 'JSON path to operate on. Supported paths: `/debug`.'
        type: string
      value:
        description: The new value for the operation. Type of value is dependent of
          `path`
        type: object
*/
func (s *ConfigService) Patch(ctx context.Context, configPatch []ConfigPatchItem) (*Response, error) {
	url := fmt.Sprintf("api/auth/0.1/config")
	req, err := s.client.NewRequest("PATCH", url, configPatch)
	if err != nil {
		return nil, err
	}

	resp, err := s.client.Do(ctx, req, nil)
	if err != nil {
		return resp, err
	}

	return resp, nil
}
