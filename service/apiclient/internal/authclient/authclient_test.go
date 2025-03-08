package authclient

// import (
// 	"encoding/base64"
// 	"net/http"
// 	"net/http/httptest"
// 	"testing"
// )

// func TestAuthClientSessionWithCredentials(t *testing.T) {
// 	// Create a test server that checks for the Authorization header
// 	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
// 		auth := r.Header.Get("Authorization")
// 		expected := "Basic " + base64.StdEncoding.EncodeToString([]byte("user:pass"))

// 		if auth != expected {
// 			t.Errorf("Expected Authorization header %q, got %q", expected, auth)
// 		}
// 	}))
// 	defer ts.Close()

// 	// Initialize AuthClient with test credentials and proper arguments
// 	client, err := NewAuthClient(ts.URL, 443, "/api/auth", "v0.1", "user", "pass")
// 	if err != nil {
// 		t.Fatalf("Failed to create AuthClient: %v", err)
// 	}

// 	httpClient := client.Session()

// 	// Perform a request using the configured http.Client
// 	resp, err := httpClient.Get(ts.URL)
// 	if err != nil {
// 		t.Fatalf("Failed to make request: %v", err)
// 	}
// 	defer resp.Body.Close()
// }

// func TestAuthClientSessionWithoutCredentials(t *testing.T) {
// 	// Create a test server that checks the absence of the Authorization header
// 	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
// 		auth := r.Header.Get("Authorization")

// 		if auth != "" {
// 			t.Errorf("Expected no Authorization header, got %q", auth)
// 		}
// 	}))
// 	defer ts.Close()

// 	// Initialize AuthClient without credentials and proper arguments
// 	client, err := NewAuthClient(ts.URL, 443, "/api/auth", "v0.1", "", "")
// 	if err != nil {
// 		t.Fatalf("Failed to create AuthClient: %v", err)
// 	}

// 	httpClient := client.Session()

// 	// Perform a request using the configured http.Client
// 	resp, err := httpClient.Get(ts.URL)
// 	if err != nil {
// 		t.Fatalf("Failed to make request: %v", err)
// 	}
// 	defer resp.Body.Close()
// }
