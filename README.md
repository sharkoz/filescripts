# filescripts

Simple dockerized web server that displays you files and folders and allows you to run scripts on them

Example docker-compose.yml :

```
version: "3.8"
services:
  filescripts:
    restart: unless-stopped
    ports:
      - 5002:5000
    image: ghcr.io/sharkoz/filescripts:main
    volumes:
      - <path_to_your_files>:/files
      - <path_to_your_scripts>:/scripts
```

Mount in /files the folder you want to be able to browse

Mount in /scripts a folder containing python scripts you want to run on your files
Each "*.py" file will be displayed as an available action on your folders and files
