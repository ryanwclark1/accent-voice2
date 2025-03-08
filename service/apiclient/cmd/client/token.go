package main

import (
	"fmt"
	"net/http"
	"io"
	"strings"
	"time"
)

func token() {
	url := "https://api.accentvoice.io/api/auth/0.1/token"
	username := "root"
	password := "secret"
	method := "POST"
	payload := strings.NewReader(`{
		"access_type": "online",
		"backend": "accent_user",
		"expiration": 7200
	}`)


	timeout := time.Duration(2 * time.Second)

	client := &http.Client{
		Timeout: timeout,
	}
	req, err := http.NewRequest(method, url, payload)

	if err != nil {
		fmt.Println("Error creating request:", err)
		return
	}

	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Accept", "application/json")

	req.SetBasicAuth(username, password)

	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Error making request:", err)
		return
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
  if err != nil {
    fmt.Println(err)
    return
  }
  fmt.Println(string(body))
}
