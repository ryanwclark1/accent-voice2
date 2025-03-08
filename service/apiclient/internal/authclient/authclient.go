package authclient

// import (
// 	"encoding/base64"
// 	"fmt"
// 	"net/http"
// 	"apiclient/internal/restclient"
// )

// type AuthClient struct {
// 	*restclient.BaseClient
// 	Username   string
// 	Password   string
// 	authClient *http.Client // Cached authenticated http.Client
// }

// // NewAuthClient creates a new instance of AuthClient with the provided parameters.
// // It initializes the BaseClient with the constructed URL from host, port, prefix, version, and sets the API prefix.
// // Default values are used for port (443), prefix ("/api/auth"), and version ("0.1") if not provided.
// func NewAuthClient(host string, port int, prefix, version, username, password string) (*AuthClient, error) {
// 	// Apply default values if necessary
// 	if port == 0 {
// 		port = 443 // Default HTTPS port
// 	}
// 	if prefix == "" {
// 		prefix = "/api/auth" // Default API prefix
// 	}
// 	if version == "" {
// 		version = "0.1" // Default API version
// 	}

// 	// Construct the full URL from the provided host, port, prefix, and version.
// 	scheme := "https"
// 	rawURL := fmt.Sprintf("%s://%s:%d%s/%s", scheme, host, port, prefix, version)

// 	baseClient, err := restclient.NewBaseClient(rawURL)
// 	if err != nil {
// 		return nil, fmt.Errorf("error creating base client: %v", err)
// 	}

// 	ac := &AuthClient{
// 		BaseClient: baseClient,
// 		Username:   username,
// 		Password:   password,
// 	}

// 	// Initialize the custom HTTP client with basic auth if credentials are provided.
// 	ac.initHTTPClient()

// 	return ac, nil
// }

// // initHTTPClient initializes the custom HTTP client with basic authentication.
// func (ac *AuthClient) initHTTPClient() {
//     if ac.Username != "" && ac.Password != "" {
// 		auth := base64.StdEncoding.EncodeToString([]byte(ac.Username + ":" + ac.Password))
// 		ac.authClient = &http.Client{
// 			Transport: &basicAuthTransport{
// 				Transport: http.DefaultTransport,
// 				AuthToken: auth,
// 			},
// 		}
// 	} else {
// 		// If no credentials are provided, use the base client's HTTP client.
// 		ac.authClient = ac.BaseClient.HttpClient()
// 	}
// }

// // Session returns a configured *http.Client with basic authentication set up.
// func (ac *AuthClient) Session() *http.Client {
// 	return ac.authClient
// }

// type basicAuthTransport struct {
// 	Transport http.RoundTripper
// 	AuthToken string
// }

// func (bat *basicAuthTransport) RoundTrip(req *http.Request) (*http.Response, error) {
// 	req.Header.Add("Authorization", "Basic "+bat.AuthToken)
// 	return bat.Transport.RoundTrip(req)
// }
