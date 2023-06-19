# tietoevry preemployment assignment

## Name
Python-based microservice

## Desc
REST API application written in Python using flask library to provide endpoints to manipulate data in the database.
Authentication for users, using jwt tokens prevents from updating/deleting movies by unauthorized users.
Support for pagination is implemented as well.

## Usage
Runs in docker container. Clone this repository and use the script run.sh to start the application.

Log will be in the console providing the IP address to access the API endpoints.

Basic configuration on the host is:

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

### /user
[GET]<br />
Requires jwt token.<br />
Returns information about current user.

```bash
curl --request GET \
  --url http://127.0.0.1:8080/user \
  --header 'Authorization: Bearer TOKEN' \
  --header 'Content-Type: multipart/form-data'
```

### /users
[GET]<br />
Index all registered users and get (public) information about them.

Supports pagination:<br />
/users?page=<int:page_num>&per_page=<int:per_page><br />
(both are optional in the query; if omitted defaults are applied page=1 & per_page=20)

Returns headers (X-Total, X-Pages-Total, ...) with infomation about pagination.

```bash
curl --request GET \
  --url http://127.0.0.1:8080/users \
  --header 'Content-Type: multipart/form-data'
```

### /users
[POST]<br />
Adds user to the database.

Requires POST form data:<br />
username<br />
password

Returns information about success with code 200.

```bash
curl --request POST \
  --url http://127.0.0.1:8080/users \
  --header 'Content-Type: multipart/form-data' \
  --form username=franz \
  --form password=0000
```

### /users/token/generate
[POST]<br />
Returns jwt token to the coresponding user.

Requires POST form data:<br />
username<br />
password

Token is valid 30 minutes since request.

```bash
curl --request POST \
  --url http://127.0.0.1:8080/users/token/generate \
  --header 'Content-Type: multipart/form-data' \
  --form username=franz \
  --form password=0000
```

### /movies
[GET]<br />
Index all movies.

Supports pagination:<br />
/movies?page=<int:page_num>&per_page=<int:per_page><br />
(both are optional in the query; if omitted defaults are applied page=1 & per_page=20)

Returns headers (X-Total, X-Pages-Total, ...) with infomation about pagination.

```bash
curl --request GET \
  --url http://127.0.0.1:8080/movies \
  --header 'Content-Type: multipart/form-data'
```

### /movies/\<int:movie_id\>
[GET]<br />
Returns information about movie specified by movie_id in the URL.

```bash
curl --request GET \
  --url http://127.0.0.1:8080/movies/1 \
  --header 'Content-Type: multipart/form-data'
```

### /movies
[POST]<br />
Requires jwt token.<br />
Adds new movie to the database.

Requires POST form data:<br />
title<br />
release_year<br />
description

Returns information about new movie with code 200.

```bash
curl --request POST \
  --url http://127.0.0.1:8080/movies \
  --header 'Authorization: Bearer TOKEN' \
  --header 'Content-Type: multipart/form-data' \
  --form 'title=The Movie X' \
  --form release_year=2015 \
  --form 'description=Lorem ipsum dolor sit amet...'
```

### /movies/\<int:movie_id\>
[PUT]<br />
Updates information about a movie in the database specified by movie_id in the URL.<br />
Requires jwt token.<br />
Only owner can change the attributes.

Requires POST form data:<br />
title<br />
release_year<br />
description

Returns movie data with code 200.

```bash
curl --request PUT \
  --url http://127.0.0.1:8080/movies/4 \
  --header 'Authorization: Bearer TOKEN' \
  --header 'Content-Type: multipart/form-data' \
  --form 'title=The Movie X' \
  --form release_year=2015 \
  --form 'description=Lorem ipsum dolor sit amet...'
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
  --header 'Authorization: Bearer TOKEN' \
  --header 'Content-Type: multipart/form-data'
```
