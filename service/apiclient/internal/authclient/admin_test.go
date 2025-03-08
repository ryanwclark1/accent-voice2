package authclient

// import (
// 	"encoding/json"
// 	"net/http"
// 	"net/http/httptest"
// 	"testing"
// )

// func TestUpdateUserEmails(t *testing.T) {
// 	// Setup a mock server
// 	mockServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
// 		// Check correct URL path
// 		expectedPath := "/api/auth/admin/users/test-uuid/emails"
// 		if r.URL.Path != expectedPath {
// 			t.Errorf("Expected URL path to be %q, got %q", expectedPath, r.URL.Path)
// 		}

// 		// Check the request method
// 		if r.Method != http.MethodPut {
// 			t.Errorf("Expected request method PUT, got %q", r.Method)
// 		}

// 		// Respond
// 		w.WriteHeader(http.StatusOK)
// 		json.NewEncoder(w).Encode(map[string]interface{}{"status": "success"})
// 	}))
// 	defer mockServer.Close()

// 	// Create an AuthClient with mock server URL, using HTTPS by default and the correct port and prefix
// 	client, err := NewAuthClient(mockServer.URL, 443, "/api/auth", "v0.1", "user", "pass")
// 	if err != nil {
// 		t.Fatalf("Failed to create AuthClient: %v", err)
// 	}

// 	// Create an AdminCommand instance using the AuthClient
// 	adminCmd := NewAdminCommand(client)

// 	// Call UpdateUserEmails
// 	userUUID := "test-uuid"
// 	emails := []string{"user@example.com"}
// 	result, err := adminCmd.UpdateUserEmails(userUUID, emails)
// 	if err != nil {
// 		t.Fatalf("UpdateUserEmails returned an unexpected error: %v", err)
// 	}

// 	// Check the result
// 	if status, ok := result["status"].(string); !ok || status != "success" {
// 		t.Errorf("Expected result status to be 'success', got %v", result["status"])
// 	}
// }
