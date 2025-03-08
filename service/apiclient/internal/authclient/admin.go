package authclient

// import (
// 	"encoding/json"
// 	"fmt"
// 	"apiclient/internal/restclient"
// )

// // AdminCommand struct will hold necessary details to execute admin commands.
// type AdminCommand struct {
// 	Client *AuthClient // Embed AuthClient to leverage REST functionalities.
// }

// // NewAdminCommand creates a new instance of AdminCommand.
// func NewAdminCommand(client *AuthClient) *AdminCommand {
// 	return &AdminCommand{
// 		Client: client,
// 	}
// }

// // UpdateUserEmails updates emails for a given user identified by user_uuid.
// func (ac *AdminCommand) UpdateUserEmails(userUUID string, emails []string) (map[string]interface{}, error) {
// 	// Initialize RESTCommand with the base client from AuthClient.
// 	restCommand := restclient.NewRESTCommand(ac.Client.BaseClient)

// 	pathFragments := []string{"admin", "users", userUUID, "emails"}
// 	bodyData, err := json.Marshal(map[string][]string{"emails": emails})
// 	if err != nil {
// 		return nil, fmt.Errorf("error marshaling emails: %v", err)
// 	}

// 	// Prepare any additional headers if needed. This could include custom headers specific to the admin operation.
// 	additionalHeaders := make(map[string]string)

// 	// Use the PUT method provided by RESTCommand to update user emails.
// 	respBody, err := restCommand.Put(pathFragments, additionalHeaders, bodyData)
// 	if err != nil {
// 		return nil, fmt.Errorf("error executing update user emails command: %v", err)
// 	}

// 	var result map[string]interface{}
// 	if err := json.Unmarshal(respBody, &result); err != nil {
// 		return nil, fmt.Errorf("error unmarshaling response: %v", err)
// 	}

// 	return result, nil
// }
