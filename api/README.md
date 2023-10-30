
# RESTful API Documentation

This documentation provides information on how to use the endpoints of the HBNB RESTful API. It includes details on each endpoint, request formats, response formats, and example usage.

## `/status` Endpoint

**Description**: This endpoint returns a JSON response with the status "OK."

**HTTP Method**: `GET`

**Endpoint**:
```
/status
```

### Request

No request parameters are required for this endpoint.

### Response

- **Response Format**: JSON
- **Status Code**: 200 (OK)

**Response Body**:
```json
{
    "status": "OK"
}
```

### Example

#### Python Requests Library

```python
import requests

url = "http://hbnb/api/v1/status"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("Status:", data.get("status"))
else:
    print("Error:", response.status_code)
```

## `/api/v1/stats` Endpoint

**Description**: This endpoint retrieves the number of each object by type.

**HTTP Method**: `GET`

**Endpoint**:
```
/api/v1/stats
```

### Request

No request parameters are required for this endpoint.

### Response

- **Response Format**: JSON
- **Status Code**: 200 (OK)

**Example Response Body**:
```json
{
  "amenities": 47,
  "cities": 36,
  "places": 154,
  "reviews": 718,
  "states": 27,
  "users": 31
}
```

### Example

#### Python Requests Library

```python
import requests

url = "http://your-api-url/api/v1/stats"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("Amenities:", data.get("amenities"))
else:
    print("Error:", response.status_code)
```

## Sample API action with a State Object

## State Endpoints

### Retrieve the list of all State objects

**Description**: Retrieves a list of all State objects.

**HTTP Method**: GET

**Endpoint**:
```
/api/v1/states
```

**Example Response Body**:
```json
[
  {
    "__class__": "State",
    "created_at": "2017-04-14T00:00:02",
    "id": "8f165686-c98d-46d9-87d9-d6059ade2d99",
    "name": "Louisiana",
    "updated_at": "2017-04-14T00:00:02"
  },
  {
    "__class__": "State",
    "created_at": "2017-04-14T16:21:42",
    "id": "1a9c29c7-e39c-4840-b5f9-74310b34f269",
    "name": "Arizona",
    "updated_at": "2017-04-14T16:21:42"
  },
  // ... (other State objects)
]
```

### Retrieve a State object

**Description**: Retrieves a single State object by its ID.

**HTTP Method**: GET

**Endpoint**:
```
/api/v1/states/<state_id>
```

**Example Response Body**:
```json
 {
  "__class__": "State",
  "created_at": "2017-04-14T00:00:02",
  "id": "8f165686-c98d-46d9-87d9-d6059ade2d99",
  "name": "Louisiana",
  "updated_at": "2017-04-14T00:00:02"
}
```

**Note**: If the `state_id` is not linked to any State object, a 404 error will be raised.

### Delete a State object

**Description**: Deletes a State object by its ID.

**HTTP Method**: DELETE

**Endpoint**:
```
/api/v1/states/<state_id>
```

**Example Response Body**:
```json
{}
```

**Note**:
- If the `state_id` is not linked to any State object, a 404 error will be raised.
- Returns an empty dictionary with the status code 200.

### Create a State

**Description**: Creates a new State object.

**HTTP Method**: POST

**Endpoint**:
```
/api/v1/states
```

**Request Body**:
```json
{
  "name": "California"
}
```

**Example Response Body**:
```json
{
  "__class__": "State",
  "created_at": "2017-04-15T01:30:27.557877",
  "id": "feadaa73-9e4b-4514-905b-8253f36b46f6",
  "name": "California",
  "updated_at": "2017-04-15T01:30:27.558081"
}
```

**Note**:
- If the HTTP request body is not valid JSON, a 400 error with the message "Not a JSON" will be raised.
- If the dictionary doesn’t contain the key `name`, a 400 error with the message "Missing name" will be raised.
- Returns the new State with the status code 201.

### Update a State object

**Description**: Updates an existing State object by its ID.

**HTTP Method**: PUT

**Endpoint**:
```
/api/v1/states/<state_id>
```

**Request Body**:
```json
{
  "name": "California Love"
}
```

**Example Response Body**:
```json
{
  "__class__": "State",
  "created_at": "2017-04-15T01:30:28",
  "id": "feadaa73-9e4b-4514-905b-8253f36b46f6",
  "name": "California is so cool",
  "updated_at": "2017-04-15T01:51:08.044996"
}
```

---

## Authentication

You do not need to provide an API key to access this API.
## Error Handling

The API may return error responses with appropriate status codes and error messages. Refer to the Errors section below for a list of common error codes and their meanings.

### 404 (Not Found) Error

**Description**: This endpoint returns a JSON-formatted 404 status code response when a resource is not found.

**HTTP Status Code**: 404 (Not Found)

**Example Response Body**:
```json
{
  "error": "Not found"
}
```

## Rate Limiting

This API currently has no rate limits in place.

## Changelog

- **Version 1.0.0** (October 30, 2023):
  - Initial release of the API.

## Contact
Victor Langat <provicml@gmail.com>
Winnie Wandia <winniewandia63@gmail.com>
