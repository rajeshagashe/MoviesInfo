# Movies Search API


### Installation


```sh
$ git clone https://github.com/rajeshagashe/MoviesInfo.git
$ cd MoviesInfo
$ pipenv shell
$ pipenv install -r requirements.txt
Create database at localhost:5432/movies and update SQLALCHEMY_DATABASE_URI in env.example
$ mv env.example .env
$ export FLASK_APP=app

```


### DB Migration
```sh
$flask db init
$flask db migrate
$flask db upgrade
$flask populate_db
```

### run tests
```sh
$ pytest -v

```

### Run

```sh
$flask run
```

### End-Points

1. /user/register  
    method - POST  
    body - 
    ``` json
    {  
        "user_name" : "User Name",  
        "password" : "PassWord",  
        "user_role": "admin/user"  
    }  
    ```
  
2. /user/login  
    method - POST  
    body - 
    ``` json{  
        "user_name" : "User Name",  
        "password" : "PassWord",  
    }  
    ```
  
3. /crud/create  
    method - POST  
    body -
    ``` json
    {  
        "name" : "Movie Name",  
        "director" : "Director_Name",  
        "genre": ["Genre1", "Genre2"],  
        "99popularity" : 100.0,  
        "imdb_score" : 10.0  
    }  
    ```
  
4. /crud/read/<movie_id>  (for one movie)  
   /crud/read  (for all movies)  
    method - GET  
  
5. /crud/update/<movie_id>   
    method - PATCH  
    body - 
    ``` json
    {  
        "key" : "value"  
    }  
    ```
  
6. /crud/delete/<movie_id>  
    method - DELETE  
  
7. /search/movies?name=Oprah&director=John  
   /search/movies?name=Oprah  
   /search/movies?director=John  
    method - GET  
  
8. /user/logout  
    method = DELETE  
  
