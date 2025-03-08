package restclient


// import (
// 	"net/http"
// 	"net/http/httptest"
// 	"testing"
// )

// func TestHTTPCommandExecute(t *testing.T) {
// 	// Mock server that echoes back the request method
// 	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
// 		if r.Method != http.MethodGet {
// 			t.Errorf("Expected GET request, got %s", r.Method)
// 		}
// 	}))
// 	defer server.Close()

// 	// Update to use NewBaseClient with proper parameters
// 	baseClient, err := NewBaseClient(server.URL)
// 	if err != nil {
// 		t.Fatalf("Failed to create BaseClient: %v", err)
// 	}

// 	httpCmd := NewHTTPCommand(baseClient)
// 	_, err = httpCmd.Execute("GET", []string{"path", "to", "resource"}, map[string]string{}, nil)
// 	if err != nil {
// 		t.Fatalf("HTTPCommand.Execute() failed: %v", err)
// 	}
// }

// func TestRESTCommandWithHeaders(t *testing.T) {
// 	// Mock server that checks for a custom header
// 	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
// 		customHeader := r.Header.Get("X-Custom-Header")
// 		if customHeader != "Value" {
// 			t.Errorf("Expected X-Custom-Header to be 'Value', got '%s'", customHeader)
// 		}
// 	}))
// 	defer server.Close()

// 	// Update to use NewBaseClient with proper parameters
// 	baseClient, err := NewBaseClient(server.URL)
// 	if err != nil {
// 		t.Fatalf("Failed to create BaseClient: %v", err)
// 	}

// 	restCmd := NewRESTCommand(baseClient)
// 	pathFragments := []string{"path", "to", "resource"}
// 	additionalHeaders := map[string]string{"X-Custom-Header": "Value"}

// 	_, err = restCmd.Get(pathFragments, additionalHeaders)
// 	if err != nil {
// 		t.Fatalf("RESTCommand.Get() failed: %v", err)
// 	}
// }
