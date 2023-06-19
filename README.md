# tietoevry preemployment assignment

## Name
Python-based microservice

## Desc
REST API application written in Python using flask library to provide endpoints to manipulate data in the database.
Authentication for users, using jwt tokens prevents from updating/deleting movies by unauthorized users.
Support for pagination is implemented as well.

## Usage
Runs in docker container. Clone this repository and use the script run.sh to start the application.

Log in the console provides an IP address to access the API endpoints.

Basic configuration on the host is:<br />
http://127.0.0.1:8080/<br />
(Port 8080 is used to avoid collisions on local machines)

## API endpoints
[GET, POST] /<br />
[GET] /user<br />
[GET] /users<br />
[POST] /users<br />
[POST] /users/token/generate<br />
[GET] /movies<br />
[GET] /movies/\<int:movie_id\><br />
[POST] /movies<br />
[PUT] /movies/\<int:movie_id\><br />
[DELETE] /movies/\<int:movie_id\><br />

### /
[GET, POST]<br />
Returns basic information about endpoints.

```bash
curl --request GET \
    --url http://127.0.0.1:8080/ \
    --header 'Content-Type: multipart/form-data'
```
```json
{
  "api": {
    "auth": {
      "current": "http://127.0.0.1:8080/user",
      "generate_token": "http://127.0.0.1:8080/users/token/generate",
      "index": "http://127.0.0.1:8080/users",
      "register": "http://127.0.0.1:8080/users"
    },
    "movies": "http://127.0.0.1:8080/movies",
    "version": "1.0"
  }
}
```

### /user
[GET]<br />
Requires jwt token.<br />
Returns information about the current user.

```bash
curl --request GET \
  --url http://127.0.0.1:8080/user \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNfaWQiOiIxMjAyOWU1Mi03ZjgzLTRlMWEtYWQ2ZC1kOWJiOTllNzZkOGYiLCJleHBpcmF0ZXMiOiIyMDIzLTA2LTE5VDEyOjMxOjE1LjQxNDExOSJ9.8ls0UHrRlLPlt1hGFzZTMv1wL0pLe4NhTsV1388i95Q' \
  --header 'Content-Type: multipart/form-data'
```
```json
{
  "user_id": 1,
  "username": "john"
}
```

### /users
[GET]<br />
Index all registered users and get (public) information about them.

Supports pagination:<br />
```
/users?page=\<int:page_num\>&per_page=\<int:per_page\><br />
```
(both are optional in the query; if omitted defaults are applied page=1 & per_page=20)

Returns headers (X-Total, X-Pages-Total, ...) with infomation about pagination: (example)
```
X-Total: 2
X-Pages-Total: 1
X-Per-Page: 20
X-Prev-Page: 
X-Next-Page: 
X-Prev-Page-Url: 
X-Next-Page-Url: 
```

```bash
curl --request GET \
  --url http://127.0.0.1:8080/users \
  --header 'Content-Type: multipart/form-data'
```
```json
[
  {
    "user_id": 1,
    "username": "john"
  },
  {
    "user_id": 2,
    "username": "mark"
  }
]
```

### /users
[POST]<br />
Adds a user to the database.

Requires POST form data:<br />
username<br />
password

Returns information about the new user with code 201.

```bash
curl --request POST \
  --url http://127.0.0.1:8080/users \
  --header 'Content-Type: multipart/form-data' \
  --form username=franz \
  --form password=0000
```
```json
[
  {
    "password": "********",
    "public_id": "(hidden)",
    "user_id": 1,
    "username": "john"
  },
  {
    "password": "********",
    "public_id": "(hidden)",
    "user_id": 2,
    "username": "mark"
  }
]
```

### /users/token/generate
[POST]<br />
Returns a jwt token to the coresponding user.

Requires POST form data:<br />
username<br />
password

The token is valid 30 minutes since the request.

```bash
curl --request POST \
  --url http://127.0.0.1:8080/users/token/generate \
  --header 'Content-Type: multipart/form-data' \
  --form username=franz \
  --form password=0000
```
```json
{
  "expirates": "2023-06-19T12:31:15.414119",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNfaWQiOiIxMjAyOWU1Mi03ZjgzLTRlMWEtYWQ2ZC1kOWJiOTllNzZkOGYiLCJleHBpcmF0ZXMiOiIyMDIzLTA2LTE5VDEyOjMxOjE1LjQxNDExOSJ9.8ls0UHrRlLPlt1hGFzZTMv1wL0pLe4NhTsV1388i95Q"
}
```

### /movies
[GET]<br />
Index all movies stored in the database.

Supports pagination:<br />
```
/movies?page=\<int:page_num\>&per_page=\<int:per_page\><br />
```
(both are optional in query; if omitted defaults are applied page=1 & per_page=20)

Returns headers (X-Total, X-Pages-Total, ...) with infomation about pagination: (example)
```
X-Total: 42
X-Pages-Total: 3
X-Per-Page: 20
X-Prev-Page: 
X-Next-Page: 2
X-Prev-Page-Url: 
X-Next-Page-Url: http://127.0.0.1:8080/movies?page=2
```

```bash
curl --request GET \
  --url http://127.0.0.1:8080/movies \
  --header 'Content-Type: multipart/form-data'
```
```json
[
  {
    "description": "The Matrix is a computer-generated gream world...",
    "movie_id": 1,
    "release_year": 1999,
    "title": "The Matrix",
    "user_id": 1
  },
  {
    "description": "Continuation of the cult classic The Matrix...",
    "movie_id": 2,
    "release_year": 2003,
    "title": "The Matrix Reloaded",
    "user_id": 2
  },
  {
    "description": "Lorem ipsum dolor sit amet...",
    "movie_id": 3,
    "release_year": 2005,
    "title": "The Movie 0",
    "user_id": 1
  },
  {
    "description": "Lorem ipsum dolor sit amet...",
    "movie_id": 5,
    "release_year": 2005,
    "title": "The Movie 2",
    "user_id": 1
  }
]
```

### /movies/\<int:movie_id\>
[GET]<br />
Returns information about movie specified by movie_id in the URL.

```bash
curl --request GET \
  --url http://127.0.0.1:8080/movies/1 \
  --header 'Content-Type: multipart/form-data'
```
```json
{
  "description": "The Matrix is a computer-generated gream world...",
  "movie_id": 1,
  "release_year": 1999,
  "title": "The Matrix",
  "user_id": 1
}
```

### /movies
[POST]<br />
Requires a jwt token.<br />
Adds new movie to the database.

Requires POST form data:<br />
title<br />
release_year<br />
description

Returns information about new movie with code 201.

```bash
curl --request POST \
  --url http://127.0.0.1:8080/movies \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNfaWQiOiIxMjAyOWU1Mi03ZjgzLTRlMWEtYWQ2ZC1kOWJiOTllNzZkOGYiLCJleHBpcmF0ZXMiOiIyMDIzLTA2LTE5VDEyOjMxOjE1LjQxNDExOSJ9.8ls0UHrRlLPlt1hGFzZTMv1wL0pLe4NhTsV1388i95Q' \
  --header 'Content-Type: multipart/form-data' \
  --form 'title=The Movie X' \
  --form release_year=2015 \
  --form 'description=Lorem ipsum dolor sit amet...'
```
```json
{
  "description": "Lorem ipsum dolor sit amet...",
  "movie_id": 46,
  "release_year": 2015,
  "title": "The Movie X",
  "user_id": 6
}
```

### /movies/\<int:movie_id\>
[PUT]<br />
Updates information about a movie in the database specified by movie_id in the URL.<br />
Requires a jwt token.<br />
Attributes of a movie can be change only by the user that created the movie.

Requires POST form data:<br />
title<br />
release_year<br />
description

Returns movie data with code 200.

```bash
curl --request PUT \
  --url http://127.0.0.1:8080/movies/4 \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNfaWQiOiIxMjAyOWU1Mi03ZjgzLTRlMWEtYWQ2ZC1kOWJiOTllNzZkOGYiLCJleHBpcmF0ZXMiOiIyMDIzLTA2LTE5VDEyOjMxOjE1LjQxNDExOSJ9.8ls0UHrRlLPlt1hGFzZTMv1wL0pLe4NhTsV1388i95Q' \
  --header 'Content-Type: multipart/form-data' \
  --form 'title=The Movie X' \
  --form release_year=2015 \
  --form 'description=Lorem ipsum dolor sit amet...'
```
```json
{
  "description": "Lorem ipsum dolor sit amet...",
  "movie_id": 10,
  "release_year": 2015,
  "title": "The Movie X",
  "user_id": 1
}
```

### /movies/\<int:movie_id\>
[DELETE]<br />
Deletes movie from the database specified by movie_id in the URL.<br />
Requires jwt token.<br />
Only owner can change the attributes.

Returns information about deleted movie with code 200.

```bash
curl --request DELETE \
  --url http://127.0.0.1:8080/movies/4 \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNfaWQiOiIxMjAyOWU1Mi03ZjgzLTRlMWEtYWQ2ZC1kOWJiOTllNzZkOGYiLCJleHBpcmF0ZXMiOiIyMDIzLTA2LTE5VDEyOjMxOjE1LjQxNDExOSJ9.8ls0UHrRlLPlt1hGFzZTMv1wL0pLe4NhTsV1388i95Q' \
  --header 'Content-Type: multipart/form-data'
```
```json
{
  "description": "Lorem ipsum dolor sit amet...",
  "movie_id": 10,
  "release_year": 2015,
  "title": "The Movie X",
  "user_id": 1
}
```
