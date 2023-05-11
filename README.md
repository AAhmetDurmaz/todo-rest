# Simple TO-DO Backend
The application built with the Django Rest Framework is an API that requires authentication and allows users to create lists and add tasks.
### Get the code 
* Clone the repository 
```bash
git clone https://github.com/AAhmetDurmaz/todo-rest.git
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Change todo/settings.py
```settings.py``` contains the default settings. These are normal and super users that are automatically added to the database. It is recommended to remove them.
Automatically created users:
| Username | e-Mail | Password | User Type |
| :------ | :------ | :------- | :-------- |
| ahmet | ahmet@ahmet.com | ahmet1413 | Normal User |
| admin | admin@admin.com | ahmet1413 | Super User |

### Generate database
```bash
python manage.py makemigrations
python manage.py migrate
```

### Run the server
`python manage.py runserver`
the application will be running on port 8000 http://localhost:8000/
## API Documentation
#### Authorization
| Header | Description     |
| :-------- | :------- |
| `Authorization` | `Bearer <access_token>` |

#### User registration
```http
  POST /auth/register
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. Unique Username. |
| `email` | `string` | **Required**. e-Mail. |
| `password` | `string` | **Required**. Password. |

#### User login
```http
  POST /auth/login
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `email` | `string` | **Required**. e-Mail. |
| `password` | `string` | **Required**. Password. |

#### Get user data - Authorization required
```http
  GET /auth/user
``` 
#### Get users TO-DO lists - Authorization required
```http
  GET /list
```

#### Create TO-DO list - Authorization required
```http
  POST /list
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name` | `string` | **Required**. Name of the list. |
| `completion_percentage` | `number` | **Optional**. Completion rate of the list. |

#### Get details of TO-DO list - Authorization required
```http
  GET /list/<LIST_ID>
```

#### Update TO-DO list - Authorization required
```http
  PUT /list/<LIST_ID>
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name` | `string` | **Optional**. Name of the list. |
| `completion_percentage` | `number` | **Optional**. Completion rate of the list. |

#### Delete TO-DO list - Authorization required
```http
  DELETE /list/<LIST_ID>
```
#### Create TO-DO task - Authorization required
```http
  POST /task
```
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `list_id` | `UUID` | **Required**. UUID of the list to add the task. |
| `content` | `string` | **Required**. Content of the task. |
| `completed` | `boolean` | **Optional**. Completion or non-completion of the task. |

#### Get details of TO-DO task - Authorization required
```http
  GET /task/<TASK_ID>
```
#### Update TO-DO task - Authorization required
```http
  PUT /task/<TASK_ID>
```
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `list_id` | `UUID` | **Optional**. UUID of the list to add the task. |
| `content` | `string` | **Optional**. Content of the task. |
| `completed` | `boolean` | **Optional**. Completion or non-completion of the task. |

#### Delete TO-DO task - Authorization required
```http
  DELETE /task/<TASK_ID>
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
