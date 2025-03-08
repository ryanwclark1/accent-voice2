package restclient

// import (
// 	"fmt"
// 	"log/slog"
// 	"net/http"
// 	"net/url"
// 	"path"
// 	"strconv"
// 	"time"
// )

// // BaseClient holds the configuration for the API client
// type BaseClient struct {
// 	Namespace         string        // Optional namespace for API endpoints
// 	Scheme            string        // URL format, including protocol (http or https)
// 	Host              string        // Hostname or IP address of the server
// 	Port              int           // Port on which the server is listening
// 	Version           string        // API version
// 	PathPrefix        string        // Optional path prefix for API endpoints
// 	Token             string        // Authentication token if required
// 	Tenant            string        // Tenant ID for multi-tenant applications
// 	HTTPS             bool          // Flag to use HTTPS; defaults to true
// 	Timeout           time.Duration // Client timeout
// 	VerifyCertificate bool          // Flag to verify server's SSL certificate
// 	// Prefix            string        // URL prefix for all requests
// 	UserAgent  string       // Custom user-agent string, if required
// 	httpClient *http.Client // Internal HTTP client instance
// 	Logger     *slog.Logger // Logger instance for logging
// }

// // NewBaseClient initializes a new instance of BaseClient.
// // It takes a rawURL as input and extracts the necessary components
// // to set up the BaseClient.
// func NewBaseClient(rawURL string) (*BaseClient, error) {
// 	parsedURL, err := url.Parse(rawURL)
// 	if err != nil {
// 		return nil, fmt.Errorf("parsing URL: %w", err)
// 	}

// 	// if parsedURL.Scheme != "http" && parsedURL.Scheme != "https" {
// 	// 	return nil, fmt.Errorf("unsupported scheme: %s", parsedURL.Scheme)
// 	// }

// 	// Ensure the scheme is correctly parsed and used
// 	scheme := parsedURL.Scheme
// 	if scheme != "http" && scheme != "https" {
// 		return nil, fmt.Errorf("unsupported scheme: %s", scheme)
// 	}

// 	if parsedURL.Hostname() == "" {
// 		return nil, fmt.Errorf("hostname cannot be empty")
// 	}

// 	port := parsedURL.Port()
// 	if port == "" {
// 		port = "80"
// 		if parsedURL.Scheme == "https" {
// 			port = "443"
// 		}
// 	}
// 	portInt, err := strconv.Atoi(port)
// 	if err != nil || portInt <= 0 || portInt > 65535 {
// 		return nil, fmt.Errorf("invalid port: %s", port)
// 	}

// 	// Set the default timeout if not provided
// 	var clientTimeout time.Duration = 10 * time.Second // Default timeout value

// 	// Set the default value for verifyCertificate
// 	var verifyCert bool = true // Default value for verifyCertificate

// 	return &BaseClient{
// 		Scheme:            parsedURL.Scheme,
// 		Host:              parsedURL.Hostname(),
// 		Port:              portInt,
// 		HTTPS:             parsedURL.Scheme == "https",
// 		Version:           "", // Set this as needed
// 		PathPrefix:        "", // Set this as needed
// 		Timeout:           clientTimeout,
// 		VerifyCertificate: verifyCert,
// 		httpClient:        &http.Client{Timeout: clientTimeout},
// 		Logger:            slog.Default(),
// 	}, nil
// }

// // URL constructs and returns a URL string based on the BaseClient configuration and
// // the provided path fragments. It dynamically includes the tenant as a query parameter
// // if it is set, and returns any error encountered.
// func (bc *BaseClient) URL(pathFragments ...string) (string, error) {
// 	// Construct the base URL from the client configuration.
// 	u := &url.URL{
// 		Scheme: bc.Scheme,
// 		Host:   bc.Host,
// 	}

// 	// Drop the port from the URL if it is 80.
// 	if bc.Port != 80 {
// 		u.Host = fmt.Sprintf("%s:%d", bc.Host, bc.Port)
// 	}

// 	// Use path.Join to concatenate the version, optional prefix, and additional fragments.
// 	// This approach ensures that double slashes are avoided.
// 	u.Path = path.Join(append([]string{bc.Version, bc.PathPrefix}, pathFragments...)...)

// 	// Initialize query parameters
// 	q := u.Query()

// 	// Include the tenant as a query parameter if it is set.
// 	if bc.Tenant != "" {
// 		q.Set("tenant", bc.Tenant)
// 	}

// 	u.RawQuery = q.Encode()

// 	// Check if the constructed URL is valid.
// 	finalURL := u.String()
// 	if _, err := url.ParseRequestURI(finalURL); err != nil {
// 		return "", fmt.Errorf("invalid URL constructed: %w", err)
// 	}

// 	return finalURL, nil
// }

// // GetHeaders generates and returns a map of default headers for HTTP requests,
// // including the Accept, Content-Type, and optionally the Authorization header
// // if a token is set, and the tenant header if a Tenant is specified.
// func (bc *BaseClient) GetHeaders(additionalHeaders map[string]string) map[string]string {
// 	headers := map[string]string{
// 		"Accept":       "application/json",
// 		"Content-Type": "application/json",
// 	}

// 	if bc.Token != "" {
// 		headers["Authorization"] = "Bearer " + bc.Token
// 	}
// 	if bc.Tenant != "" {
// 		headers["X-Tenant-ID"] = bc.Tenant
// 	}
// 	if bc.UserAgent != "" {
// 		headers["User-Agent"] = bc.UserAgent
// 	}

// 	// Merge any additional headers provided.
// 	for key, value := range additionalHeaders {
// 		headers[key] = value
// 	}

// 	return headers
// }

// func (bc *BaseClient) HttpClient() *http.Client {
// 	return bc.httpClient
// }
