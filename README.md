# tietoevry preeymployment assignment

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
http://127.0.0.1:8080/
(Port 8080 is used to avoid collisions on local machines)

## API endpoints
[GET, POST] /
[GET] /user
[GET] /users
[POST] /users
[POST] /users/token/generate
[GET] /movies
[GET] /movies/<int:movie_id>
[POST] /movies
[PUT] /movies/<int:movie_id>
[DELETE] /movies/<int:movie_id>

### /
[GET, POST]
Returns basic information about endpoints.

### /user
[GET]
Requires jwt token.
Returns information about current user.

### /users
[GET]
Index all registered users and get (public) information about them.

Supports pagination:
/users?page=<int:page_num>&per_page=<int:per_page>
(both are optional in the query; if omitted defaults are applied page=1 & per_page=20)

Returns headers (X-Total, X-Pages-Total, ...) with infomation about pagination.

### /users
[POST]
Adds user to the database.

Requires POST form data:
username
password

Returns information about success with code 200.

### /users/token/generate
[POST]
Returns jwt token to the coresponding user.

Requires POST form data:
username
password

Token is valid 30 minutes since request.

### /movies
[GET]
Index all movies.

Supports pagination:
/movies?page=<int:page_num>&per_page=<int:per_page>
(both are optional in the query; if omitted defaults are applied page=1 & per_page=20)

Returns headers (X-Total, X-Pages-Total, ...) with infomation about pagination.

### /movies/<int:movie_id>
[GET]
Returns information about movie specified by movie_id in the URL.

### /movies
[POST]
Requires jwt token.
Adds new movie to the database.

Requires POST form data:
title
release_year
description

Returns information about new movie with code 200.

### /movies/<int:movie_id>
[PUST]
Updates information about a movie in the database specified by movie_id in the URL.
Requires jwt token.
Only owner can change the attributes.

Requires POST form data:
title
release_year
description

Returns movie data with code 200.

### /movies/<int:movie_id>
[DELETE]
Deletes movie from the database specified by movie_id in the URL.
Requires jwt token.
Only owner can change the attributes.

Returns information about deleted movie with code 200.