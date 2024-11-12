# App For Hiking In Finland 🇫🇮
 
Finnhike is a web application dedicated to showcasing hiking spots in Finland. Built with Django, it provides users with an interactive map, filtering capabilities, and detailed information on each hiking place.


### Built With
- Django
- JavaScript
- Leaflet
- PostgreSQL
- Nginx
- Gunicorn
- Docker
- AWS

<img src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExeHJwcjAwcGQ2YnMzMGw2NDZod2hnOTI5NHZydDN2aXJnN2k4bmZiZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/7p0qZOxUe5cIM/giphy.gif" width="300px" />

<hr>

### How To Run

#### You should have:

  - Running Docker

1. clone the repository
```bash
https://github.com/dariavarlamovaa/finnhike.git
```

2. navigate to cloned project
3. use Docker commands
```bash
docker compose -f docker-compose.dev.yml up --build
```
4. access the web interface at http://localhost:8000 or http://127.0.0.1:8000


### Environment Variables

Main configuration is located in files:
 - `.env.dev`
 - `.env.example`

