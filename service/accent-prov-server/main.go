package main

import (
	"flag"
	"io/fs"
	"log"
	"net/http"
	"strings"
	"fmt"
)

// Create a directory variable called directory that can use ENV variables or default to /files
var directory = "/files"

func containsDotFile(name string) bool {
	parts := strings.Split(name, "/")
	for _, part := range parts {
		if strings.HasPrefix(part, ".") {
			return true
		}
	}
	return false
}

type dotFileHidingFile struct {
	http.File
}

func (f dotFileHidingFile) Readdir(n int) (fis []fs.FileInfo, err error) {
	files, err := f.File.Readdir(n)
	for _, file := range files {
		if !strings.HasPrefix(file.Name(), ".") {
			fis = append(fis, file)
		}
	}
	return
}

type dotFileHidingFileSystem struct {
	http.FileSystem
}

func (fsys dotFileHidingFileSystem) Open(name string) (http.File, error) {
	if containsDotFile(name) { // If dot file, return 403 response
		return nil, fs.ErrPermission
	}

	file, err := fsys.FileSystem.Open(name)
	if err != nil {
		return nil, err
	}
	return dotFileHidingFile{file}, err
}


func main() {
	log.SetFlags(log.LstdFlags)
	port := flag.Int("port", 8021, "the port to listen on")
    flag.Parse()

	fsys := dotFileHidingFileSystem{http.Dir(directory)}
	fileServer := http.FileServer(fsys)
	http.Handle("/", fileServer)
	log.Printf("Starting Provisioning Server at port %d\n", *port)
	if err := http.ListenAndServe(fmt.Sprintf(":%d", *port), nil); err != nil {
		log.Fatalf("Failed to start Provisioning Server: %v", err)
	}
}