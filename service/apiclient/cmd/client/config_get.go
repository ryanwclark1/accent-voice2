package main

import (
  "fmt"
  "time"
  "net/http"
  "io"
)

func config_get() {

  url := "https://api.accentvoice.io/api/auth/0.1/config"
  method := "GET"

  timeout := time.Duration(2 * time.Second)
  client := &http.Client {
    Timeout: timeout,
  }
  req, err := http.NewRequest(method, url, nil)

  if err != nil {
    fmt.Println(err)
    return
  }
  req.Header.Add("X-Auth-Token", "502ba2f8-be62-4799-8fb5-fd47a9402ab3")

  res, err := client.Do(req)
  if err != nil {
    fmt.Println(err)
    return
  }
  defer res.Body.Close()

  body, err := io.ReadAll(res.Body)
  if err != nil {
    fmt.Println(err)
    return
  }
  fmt.Println(string(body))
}
