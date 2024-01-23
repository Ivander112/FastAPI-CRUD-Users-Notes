# FastAPI + SQLAlchemy + Alembic Boilerplate

This is a sample project of Async Web API with FastAPI + SQLAlchemy 2.0 + Alembic.
It includes asynchronous DB access using asyncpg and test code.

See [reference](https://github.com/rhoboro/async-fastapi-sqlalchemy/tree/main).

Other References
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [SQL Alchemy](https://docs.sqlalchemy.org/en/20/orm/index.html)
- [SQL Alchemy - PostgreSQL](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

# Setup

## Install

```shell
$ python3 -m venv venv
$ . venv/bin/activate
(venv) $ pip3 install -r requirements.txt
```

## Setup a database and create tables

```shell
(venv) $ docker run -d --name db \
  -e POSTGRES_PASSWORD=root \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v pgdata:/var/lib/postgresql/data/pgdata \
  -p 5432:5432 \
  postgres:15.2-alpine

# Cleanup database
# $ docker stop db
# $ docker rm db
# $ docker volume rm pgdata

(venv) $ APP_CONFIG_FILE=local python3 app/main.py migrate
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> a8483365f505, initial_empty
INFO  [alembic.runtime.migration] Running upgrade a8483365f505 -> 24104b6e1e0c, add_tables
```

# Run

```shell
(venv) $ APP_CONFIG_FILE=local python3 app/main.py api
INFO:     Will watch for changes in these directories: ['...']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [92173] using WatchFiles
INFO:     Started server process [92181]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

You can now access [localhost:8000/docs](http://localhost:8000/docs) to see the API documentation.

# Test

```shell
(venv) $ python3 -m pytest
```

# Create Migration

```shell
(venv) $ cd app/migrations
(venv) alembic revision -m "<name_of_migration_file>"
```


# CRUD API Notes

Adding a method for notes endpoint with function:

-   Create new note with created_by from user_id in JWT token
    
-   Request all notes with pagination. Using filter by user_id in JWT token and notes that have not been deleted
    
-   Request One Notes with validated if user_id in JWT token was the one who created the note
    
-   Update existing note
    
-   Delete Notes (set deleted_at and deleted_By)

## Add Note

http://127.0.0.1:8000/api/v1/notes/add


### Request URL

-   Method: POST
    
-   URL: `http://127.0.0.1:8000/api/v1/notes/add`
    

### Example Request Body

        
    ```
      {
          "title": "test-APi",
          "content": "test-New"
      }
    ```
    

### Example Response

-   Status: 200 OK
    
-   Data:
    
    JSON
    
    ```json
          {
              "data": {
                  "content": "test-New",
                  "created_at": "Mon, 22 Jan 2024 15:23:21 GMT",
                  "created_by": 3,
                  "deleted_at": null,
                  "deleted_by": null,
                  "note_id": 64,
                  "title": "test-APi",
                  "updated_at": null,
                  "updated_by": null
              },
              "message": "success add new note",
              "status": "success"
          }
    ```


### Get All Note (Pagination)

http://127.0.0.1:8000/api/v1/notes/?page=2&item_per_page=1&filter_by_user_id=false

This endpoint makes an HTTP GET request to retrieve notes. It accepts query parameters including page number, items per page, and a filter by user ID flag. The last call to this request did not include a request body.

### Query Parameters

-   `page`: The page number for paginated results.
    
-   `item_per_page`: The number of items to be included per page.
    
-   `filter_by_user_id`: A flag to filter the notes by user ID.
    

### Response

The response will have JSON object with the `data`, `message`, and `status` fields. The `data` object contains `meta` information and an array of `records` representing the notes. Each record includes details such as content, title, creation and update timestamps, and user IDs.

Example Input:

http://localhost:8000/api/v1/notes/?page=1&item_per_page=5&filter_by_user_id=true

Query Params

page  1

item_per_page   5

filter_by_user_id   true

### Get one note

http://127.0.0.1:8000/api/v1/notes/34

This endpoint makes an HTTP GET request to retrieve the details of a specific note. The request should include the note ID in the URL path.

No request body is required for this endpoint.

Example response

```json
        {
          "status": "success",
          "message": "success read note",
          "data": {
              "note_id": 34,
              "title": "Fast Note",
              "content": "Fast content",
              "created_at": "2024-01-20T07:14:00.982207",
              "created_by": 1,
              "updated_at": null,
              "updated_by": null,
              "deleted_at": null,
              "deleted_by": null
          }
        }
```

### Update Note

http://127.0.0.1:8000/api/v1/notes/49

## Update Note

This endpoint allows the user to update a specific note by sending an HTTP PUT request to the specified URL.

### Example Request Body

-   The request should include a raw JSON payload in the request body with the following parameters:
    
    -   `title` (string, required): The updated title of the note.
        
    -   `content` (string, required): The updated content of the note.
        

Example Input:

```json
{
  "title": "Updated Title",
  "content": "Updated Content"
}
```
### Response
  
  Example Response:


```json
{
  "data": {
    "note_id": 123,
    "title": "Updated Title",
    "content": "Updated Content",
    "created_at": "2022-01-01T12:00:00Z",
    "updated_at": "2022-01-02T10:00:00Z",
    "created_by": 456,
    "updated_by": 456,
    "deleted_at": null,
    "deleted_by": null
  },
  "message": "Note updated successfully",
  "status": "success"
}
```

### Delete Note

http://127.0.0.1:8000/api/v1/notes/50

This endpoint sends an HTTP DELETE request to [http://127.0.0.1:8000/api/v1/notes/63](http://127.0.0.1:8000/api/v1/notes/63) to delete a specific note. The request does not contain any payload in the raw request body.

  Example Response:

```json
{
    "data": {
        "content": "test2fe5",
        "created_at": "Mon, 22 Jan 2024 12:20:39 GMT",
        "created_by": 3,
        "deleted_at": "Mon, 22 Jan 2024 15:27:15 GMT",
        "deleted_by": 1,
        "note_id": 63,
        "title": "test453",
        "updated_at": null,
        "updated_by": null
    },
    "message": "success delete user",
    "status": "success"
}
```
