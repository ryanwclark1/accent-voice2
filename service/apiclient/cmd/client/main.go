package main

import (
	"context"
	// "encoding/json"
	"fmt"
	// "io"
	"net/http"
	// "strings"
	// "time"
	"apiclient/internal/restclient"
	// "github.com/zclconf/go-cty/cty/json"
)

func main() {
	username := "root"
	password := "secret"

	// url := "https://api.accentvoice.io/api/auth/0.1/token"
	// method := "POST"
	// payload := strings.NewReader(`{
	// "access_type": "online",
	// "backend": "accent_user",
	// "expiration": 7200
	// }`)

	// timeout := time.Duration(2 * time.Second)

	// client := &http.Client{
	// 	Timeout: timeout,
	// }
	// req, err := http.NewRequest(method, url, payload)
	// if err != nil {
	// 	fmt.Println("Error creating request:", err)
	// 	return
	// }

	// req.Header.Set("Content-Type", "application/json")
	// req.Header.Set("Accept", "application/json")

	// req.SetBasicAuth(username, password)

	// resp, err := client.Do(req)
	// if err != nil {
	// 	fmt.Println("Error making request:", err)
	// 	return
	// }
	// defer resp.Body.Close()

	// body, err := io.ReadAll(resp.Body)
	// if err != nil {
	// 	fmt.Println(err)
	// 	return
	// }
	// fmt.Println("Request Header: ", resp.Request.Header)
	// fmt.Println("Request URI: ", resp.Request.RequestURI)
	// fmt.Println("Response Body: ", string(body))

	// Using the restclient package using Token the TokenSerice use the TokenBasicAuth function to authenticate and return a Token struct.
	// will use the user name and password as well as the body parameters called TokenBody to specify the access type, backend, and expiration.



	// client := restclient.NewClient(nil)
	// // Create context?
	// ctx := context.Background()
	// tokendata, resp, err := client.Token.TokenBasicAuth(ctx, username, password, nil)
	// if err != nil {
	// 	fmt.Println("Request URL:", resp.Request.URL)
	// 	fmt.Println("Request Body:", resp.Request.Body)
	// 	fmt.Println("Request Header:", resp.Request.Header)
	// 	fmt.Println("Error making request:", err)
	// 	return
	// }
	// fmt.Println("Success, TokenData:", tokendata)
	// fmt.Printf("Type: %T\n", tokendata)
	// fmt.Println("Response: ", resp.Request.Header)



	// Initialize the client and token service
	client := restclient.NewClient(&http.Client{}) // Replace with the actual client initialization
	tokenService := client.Token

	// Set the username and password
	// username := "your-username"
	// password := "your-password"

	// Create the token request parameters
	params := &restclient.TokenRequestParams{
		Username: username,
		Password: password,
	}

	// Create the token
	tokenresponse, resp, err := tokenService.CreateToken(context.Background(), params)
	if err != nil {
		fmt.Println("Request URL:", resp.Request.URL)
		fmt.Println("Request Body:", resp.Request.Body)
		fmt.Println("Request Header:", resp.Request.Header)
		fmt.Println("Error making request:", err)
		// log.Fatal(err)
	}

	// Print the token
	fmt.Println("Token:", tokenresponse.Token)
	fmt.Println("Success, TokenData:", tokenresponse)
	fmt.Printf("Type: %T\n", tokenresponse)
	fmt.Println("Response: ", resp.Request.Header)


	// Get the data within the tokendata and within the Token struct


	// Using the restclient package using Token the TokenService use the TokenDelete function to revoke a token.
	// Should use /0.1/token/{token}
	// The token is
	// var responsedata restclient.TokenData

	// responsetoken := responsedata
	// fmt.Println("")
	// fmt.Println("Token:", responsetoken)

	// resp, err = client.Token.TokenDelete(ctx, responsetoken)
	// if err != nil {
	// 	fmt.Println("Error deleting token:", err)
	// 	return
	// }
	// fmt.Println("Token Deleted:", resp)



	// err = json.Unmarshal([]byte{tokendata}, &responsedata)
	// if err != nil {
	// 	fmt.Println("Error unmarshalling token data:", err)
	// 	return
	// }
	// fmt.Println("Token Data:", responsedata)

	// if responsedata.Token != nil {
	// 	token := responsedata.Token
	// }
	// token := responsedata.Token
	// if token != nil {

	// }
	// resp, err = client.Token.TokenDelete(ctx, token)
}
