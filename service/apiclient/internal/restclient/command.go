package restclient

// import (
//     "bytes"
//     "fmt"
//     "io"
//     "net/http"
// )

// // HTTPCommand wraps the functionality for making HTTP requests.
// type HTTPCommand struct {
//     Client *BaseClient // Reference to the base client to use for requests
// }

// // NewHTTPCommand creates a new instance of HTTPCommand.
// func NewHTTPCommand(client *BaseClient) *HTTPCommand {
//     return &HTTPCommand{Client: client}
// }

// // Execute performs an HTTP request using the method, URL, headers, and body data provided.
// // It handles constructing the request, sending it, and processing the response.
// func (cmd *HTTPCommand) Execute(method string, pathFragments []string, additionalHeaders map[string]string, data []byte) ([]byte, error) {
//     // Construct the complete URL using path fragments and the base client's URL method.
//     urlString, err := cmd.Client.URL(pathFragments...)
//     if err != nil {
//         return nil, fmt.Errorf("constructing request URL: %w", err)
//     }

//     req, err := http.NewRequest(method, urlString, bytes.NewBuffer(data))
//     if err != nil {
//         return nil, fmt.Errorf("creating request: %w", err)
//     }

//     // Set request headers.
//     headers := cmd.Client.GetHeaders(additionalHeaders)
//     for key, value := range headers {
//         req.Header.Set(key, value)
//     }

//     // Execute the request using the internal HTTP client.
//     resp, err := cmd.Client.httpClient.Do(req)
//     if err != nil {
//         return nil, fmt.Errorf("executing request: %w", err)
//     }
//     defer resp.Body.Close()

//     // Validate the response status code.
//     if resp.StatusCode < 200 || resp.StatusCode >= 300 {
//         return nil, fmt.Errorf("HTTP request error: %s", resp.Status)
//     }

//     // Read and return the response body.
//     body, err := io.ReadAll(resp.Body)
//     if err != nil {
//         return nil, fmt.Errorf("reading response body: %w", err)
//     }

//     return body, nil
// }

// // RESTCommand extends HTTPCommand to specialize for RESTful operations.
// type RESTCommand struct {
//     *HTTPCommand
// }

// // NewRESTCommand creates a RESTCommand with the provided BaseClient.
// func NewRESTCommand(client *BaseClient) *RESTCommand {
//     return &RESTCommand{
//         HTTPCommand: NewHTTPCommand(client),
//     }
// }

// // Helper functions for specific HTTP methods.
// // These methods utilize Execute to send requests.
// func (cmd *RESTCommand) Get(pathFragments []string, additionalHeaders map[string]string) ([]byte, error) {
//     return cmd.Execute(http.MethodGet, pathFragments, additionalHeaders, nil)
// }

// func (cmd *RESTCommand) Post(pathFragments []string, additionalHeaders map[string]string, bodyData []byte) ([]byte, error) {
//     return cmd.Execute(http.MethodPost, pathFragments, additionalHeaders, bodyData)
// }

// func (cmd *RESTCommand) Put(pathFragments []string, additionalHeaders map[string]string, bodyData []byte) ([]byte, error) {
//     return cmd.Execute(http.MethodPut, pathFragments, additionalHeaders, bodyData)
// }

// func (cmd *RESTCommand) Delete(pathFragments []string, additionalHeaders map[string]string) ([]byte, error) {
//     return cmd.Execute(http.MethodDelete, pathFragments, additionalHeaders, nil)
// }
